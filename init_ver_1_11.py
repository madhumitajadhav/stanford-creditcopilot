# !pip install -q --upgrade streamlit langchain PyPDF4 pdfplumber google-generativeai langchain-google-genai faiss-cpu python-dotenv
# !pip install Pillow
# !pip install pypdf

import re
import os
import pdfplumber
import PyPDF4
import PIL.Image
import streamlit as st
import google.generativeai as genai
from google.generativeai import generative_models
from langchain.prompts import PromptTemplate #to create prompt templates
from langchain.chains.question_answering import load_qa_chain #to chain the prompts
from langchain.text_splitter import RecursiveCharacterTextSplitter #library to split pdf files
from langchain_community.vectorstores import FAISS #for vector embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings #to embed the text
from langchain_community.document_loaders import PyPDFDirectoryLoader # load all the docs in the dir
from langchain_google_genai import ChatGoogleGenerativeAI #langchain interface with google
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

st.session_state.discovery_flag = 0
st.session_state.analysis_flag = 0
st.session_state.proposal_flag = 0

# setting a high value for temperature, we can play with it to determine what works best for the prototype
generation_config = genai.GenerationConfig(
  stop_sequences = None,
  temperature=0.9,
  top_p=1.0,
  top_k=16,
  candidate_count=1,
  max_output_tokens=2047,
)

safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]


# will only pick up png, jpeg, jpg, tiff or bmp images in the directory
def vision_to_text(dir_path_images):
    txt = ""
    vis_model = genai.GenerativeModel('gemini-pro-vision') # create object of gemini-pro-vision for reading the images
    vis_prompt = "Capture all the text in this picture one row at a time and format it exactly the way it appears in this picture"
    directory = os.fsencode(dir_path_images)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith(".jpg") or filename.endswith(".tiff") or filename.endswith(".gif") or filename.endswith(".bmp"):
            image_file = dir_path_images + filename
            response = vis_model.generate_content([f"{vis_prompt}", PIL.Image.open(image_file)], safety_settings=safety_settings)
            for candidate in response.candidates:
                txt += str([part.text for part in candidate.content.parts])
            continue
        else:
            continue
    print("length of vision text: ", len(txt))
    return txt



def clean_text (unclean_txt):
    return re.sub('[!@#*]', '', unclean_txt)


def get_pdf_text(data):
    text = ""
    # iterate over all pages in a pdf
    for page in data:
      text += clean_text(str(page.page_content))

    print ("length of raw pdf text: ", len(text))
    return text


def get_text_chunks(text):
    # create an object of RecursiveCharacterTextSplitter with specific chunk size and overlap size
    # we may have to play around with the chunk size based on the queries that we plan to run for the prototype
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 10000, chunk_overlap = 1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001", google_api_key = GOOGLE_API_KEY) # google embeddings
    vector_store = FAISS.from_texts(text_chunks,embeddings) # use the embedding object on the splitted text of pdf docs
    vector_store.save_local("faiss_index") # save the embeddings in local
    return embeddings


def get_conversation_chain():
    # define the prompt
    prompt_template = """
    You are a credit underwriter who works for a Private Bank that works with High Net Worth clients. You task is to underwrite a loan for a client or a prospect.
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n
    Answer:
    """
    model = ChatGoogleGenerativeAI(model = "gemini-pro", temperatue = 0.3, google_api_key = GOOGLE_API_KEY) # create object of gemini-pro text
    prompt = PromptTemplate(template = prompt_template, input_variables= ["context","question"])
    chain = load_qa_chain(model,chain_type="stuff", prompt = prompt)
    return chain 



def get_db(embeddings):
    # user_question is the input question
    #embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001", google_api_key = GOOGLE_API_KEY)
    # load the local faiss db (it was treating the content as dangerous, so had to add this - allow_dangerous_deserialization=True)
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    return new_db


def user_input(user_question, new_db):
    # using similarity search, to get the relevant answer based on the user question
    docs = new_db.similarity_search(user_question)

    # will have to think through how we want to design the multi-turn chat
    chain = get_conversation_chain()

    response = chain.invoke(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    return response


def init():
# you can use the browse function to get the dir_paths for the docs and images
#   from google.colab import drive
#   drive.mount ('./mount')
  dir_path_docs = './docs'
  dir_path_images = './images/'

# this is the core functionality for processing the docs
  loader = PyPDFDirectoryLoader(dir_path_docs)
  data = loader.load()
  raw_text = get_pdf_text(data)
  raw_text += vision_to_text(dir_path_images)
  print ("length of total text: ", len(raw_text))
  text_chunks = get_text_chunks(raw_text)
  embeddings = get_vector_store(text_chunks)
  return get_db(embeddings)


if __name__ == "__main__":
  load_dotenv()
  # GOOGLE_API_KEY = os.getenv(GOOGLE_API_KEY)
  # print(GOOGLE_API_KEY)
  genai.configure(api_key=GOOGLE_API_KEY)
  
  new_db = init()

  #these 3 lines can be used for QnA
  query = input('Enter your question: ')
  responses = user_input(query, new_db)
  print(responses["output_text"])
