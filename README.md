# Credit Co-Pilot 🤖

A proof-of-concept Streamlit app that automates parts of the credit/loan underwriting
workflow for private banking, combining an LLM-based document assistant with a
traditional ML loan-approval classifier.

Traditional credit origination for high-net-worth clients is slow, manual, and
document-heavy. Credit Co-Pilot explores how LLMs (Google Gemini via LangChain) and a
retrieval pipeline over a client's documents (tax returns, credit reports, trust
agreements, term sheets, etc.) can speed up discovery, financial analysis, proposal
drafting, credit memo generation, and the final credit decision — alongside a
scikit-learn classifier as a second, independent decisioning signal.

> The client used throughout the demo ("Barbie") and all supporting documents in
> `docs/` are synthetic/fictional data created for this proof of concept.

## How it works

The app walks through the underwriting process as a sequence of Streamlit tabs, each
one building on the previous stage's output:

1. **Discovery** — summarizes the borrower and proposed transaction from source documents
2. **Analysis** — assesses assets, liabilities, income, credit report, and DTI/reserve ratios
3. **Proposal** — drafts a loan recommendation and assigns a Credit Risk Rating (CRR)
4. **Credit Memo** — generates a full credit memorandum from the prior stages
5. **LLM Based Credit Decision** — critiques the credit memo and renders an approve/reject decision
6. **ML Based Credit Decision** — extracts structured borrower data via the LLM and runs it through a trained decision-tree loan classifier for comparison

Each stage's Q&A is persisted to a `.docx` file under `LLM_Response/`, and retrieval
over the source documents is powered by a FAISS vector index built from Google's text
embeddings.

## Tech stack

- **UI**: Streamlit
- **LLM / RAG**: LangChain, Google Generative AI (Gemini), FAISS
- **ML**: scikit-learn (decision tree loan classifier)
- **Document handling**: pdfplumber, PyPDF4/pypdf, python-docx

## Project structure

```
Demo_V2.py            Main Streamlit app (all 6 workflow tabs)
Intro.py               Landing/intro page
init_ver_1_11.py        RAG pipeline: PDF/image ingestion, chunking, embeddings, FAISS, QA chain
questions_v2.py         Prompt templates for each underwriting stage
docs/                   Synthetic borrower documents (tax returns, credit report, term sheet, etc.)
images/                 Synthetic borrower ID documents used for the vision-to-text step
dataset/                Loan approval training/test data for the ML classifier
loan_classifier_model.pkl  Trained decision-tree loan classifier
faiss_index/            Persisted FAISS vector index
LLM_Response/           Generated .docx outputs per workflow stage
```

## Setup

1. **Clone and create a virtual environment**

   ```bash
   git clone https://github.com/madhumitajadhav/CreditCoPilot.git
   cd CreditCoPilot
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Add your Google API key**

   Copy `.env.example` to `.env` and fill in a [Google AI Studio](https://aistudio.google.com/app/apikey) API key:

   ```bash
   cp .env.example .env
   ```

   ```
   GOOGLE_API_KEY=your-google-generativeai-api-key-here
   ```

3. **Run the app**

   ```bash
   streamlit run Demo_V2.py
   ```

   The first time you run a tab, the app builds a FAISS index from the documents in
   `docs/` and `images/`, so the first query in the Discovery tab will take longer.

## Notes

- Each tab depends on completing the previous stage in the same session (Discovery →
  Analysis → Proposal → Credit Memo → Credit Decision) — the app tracks this via
  Streamlit session state.
- The ML classifier tab (`ML Based Credit Decision`) requires the Discovery stage to
  have been run first, since it asks the LLM to extract structured fields from the
  Discovery response before scoring them.
