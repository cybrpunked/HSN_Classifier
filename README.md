🧾 Product Classification Code Verifier

A smart, web-based code validation tool for verifying HSN and SAC product classification codes using a reference Excel dataset. Built with Python, Flask, and Streamlit, it applies intelligent agent principles and delivers real-time, responsive feedback.
🚀 Features

    ✅ Format validation for HSN/SAC codes (2, 4, 6, 8 digits only)

    📂 Excel dataset verification via pandas and openpyxl

    📊 Streamlit-powered alternate version for easy demo/testing

    🧠 Agent structure using concepts from Google's Agent Development Kit (ADK)

    💡 Real-time web UI and session history

🧠 Intelligent Agent Design (ADK-Inspired)
Component	Implementation
Intent	CodeValidationIntent on user submission
Entity	ProductCode extracted from input
Tool	CodeCheckUtility (Excel handler and validator)
Memory	session_log[] to track all validations
Reasoning	Optional – extendable for analytics or feedback
🛠️ Validation Strategy

    Acceptable Codes: Numeric, length of 2, 4, 6, or 8 digits (HSN), and 2–6 digits (SAC)

    Incorrect formats: e.g., X456, 12AB → ❌ Invalid

    Missing codes: e.g., 888888 → ⚠️ Not found in dataset

    Blank input → 🚫 Ignored

.
├── app.py                    # Flask web application
├── code_verifier.py          # Excel reading + validation engine
├── hsn_validator.py          # Streamlit-based alternate validator
├── templates/
│   ├── main.html             # Homepage input form
│   └── history.html          # Session history view
├── Product_Codes_Reference.xlsx  # Main dataset
├── requirements.txt          # Python dependencies
└── README.md
