import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.title("Credit Co-Pilot 🤖")

# st.markdown("<h4 style='text-align: justify; color: orange'>Problem Statement:</h4>", unsafe_allow_html=True)
# st.markdown("Traditional credit and loan origination processes for high-net-worth and ultra-high-net-worth clients in wealth management and private banking are slow, manual, documentation-heavy and expensive. These processes often lack the sophistication needed for a comprehensive analysis and fast response and decision times.")

# st.markdown("<h4 style='text-align: justify; color: orange'>Solution:</h4>", unsafe_allow_html=True)
# st.markdown("Our startup leverages Large Language Models (LLMs) and AI to streamline and enhance the credit origination process. We provide an automated, data-driven platform that accelerates decision times, adapts to new data sources, and offers deeper insights into clients' financial health.")

# st.markdown("<h4 style='text-align: justify; color: orange'>Mission:</h4>", unsafe_allow_html=True)
# st.markdown("To equip underwriters and financial institutions with AI-driven tools that improve client discovery, financial and legal analysis, credit recommendations, credit decisioning and post-origination portfolio management. Our goal is to make the credit process more efficient, accurate, and client-focused.")

# st.markdown("<h4 style='text-align: justify; color: orange'>Vision:</h4>", unsafe_allow_html=True)
# st.markdown("To revolutionize the credit and loan origination landscape for wealth management and private banking institutions by setting a new standard in personalized, efficient, and sophisticated credit analysis and portfolio management. We aspire to drive the industry towards a more agile, efficient, and client-centric future through the application of advanced AI technologies.")


st.image("process.png", use_column_width=True, caption='Random image for sizing')
st.image("intro.png", use_column_width=True, caption='Random image for sizing')

# Footer
st.markdown("---")
st.text("© 2024 Credit Co-Pilot")