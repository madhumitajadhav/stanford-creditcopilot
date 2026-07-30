
discovery_questions = {"Transaction and Borrower Overview":"""Generate detailed summary of the following sections: 
1. Borrower Name, Loan Amount, Loan Purpose
2. Summary of the proposed loan transaction (summarize terms in available Term Sheet)
3. Barbie's engagement with ABC Private Bank to date
4. Summary of borrower's professional, education and personal information
5. Evaluation of borrower's financial information (e.g. Net Worth, Assets, Liabilities, Income)
                        """,
    
                        "OProspect Data Transformation (JSON)": """Organize known information about Barbie in the following sections in JSON format (do not include proposed loan information and its pro forma impact): 
1. Personal Information,
2. Professional / Career Background (do not include any business income information),
3. Summary Financials, 
4. Barbie’s Primary Contacts at ABC Private Bank and their roles with whom has been working.""",

    "Prospect Opportunity Rating": """Rate Barbie based on the following criteria: "High Potential" for prospects seeking loans over $10MM or have net worth over $25MM, "Medium Potential" for prospects seeking loans between $5MM and <$10MM or net worth between $10MM and $25MM, and "Low Potential" for prospects seeking loans less than $5MM or have net worth less than $10MM. Provide summary rationale for your rating."""    
    }


analysis_questions = {
    "Borrower Financial Assessment" : """Summarize Barbie's financials in the following sections: 
1. Assets, 
2. Liabilities, 
3. Income, 
4. Credit Report (Including FICO Score), 
5. DTI and Reserve Coverage Ratios, 
6. Assessment of sections 1 through 5 in the context of Tailored Lending Underwriting Guidelines.
""",
    
    "Borrower's Financial Data Transformation (JSON)":"""Extract Barbie's financial data across the following categories: 
1. Assets, 
2. Liabilities,
3. Income, and 
4. Summary of Credit Report.
Return results in JSON format""",
    
    "Income Trends Analysis": """You are a CPA and skilled in analyzing tax returns. What is Barbie's AGI in 2023?""",
    
    "Trust Document Analysis": """Does Barbie's trust agreement allow her to pledge shares in mattel as additional collateral for the airplane loan? Please explain why. """}


proposal_questions = {
    "Loan Application Recommendation": """Generate a loan recommendation for Barbie's airplane loan application.
Provide detailed and "essay-like" assessment of Barbie's financial information in the context of the Tailored Lending Underwriting guidelines. 
Include discussion of areas of strength and weaknesses relative to the Tailored Lending Underwriting guidelines. 
Ensure that you apply the Pro Forma Contractual Reserves Based on Pro Forma DTI Ratios as per the Tailored Lending Underwriting guidelines. 
Use 3rd voice in your writing.""",
    
    "Assign Credit Risk Rating for the Borrower":"""Using CRR Matrix framework, assign CRR rating to this loan proposal."""
                     }

