# Bank Customer Support Prompt Chain

An intelligent customer support system for a bank that processes customer queries through a 5-stage prompt chain to understand, classify, and respond to customer requests.

## Overview

Instead of sending a customer query directly to an AI model, this system breaks the process into 5 clearly defined stages — each building on the previous one — to produce a more accurate and structured response.

```
Customer Query
      ↓
Stage 1 → Interpret customer intent
      ↓
Stage 2 → Map to possible categories
      ↓
Stage 3 → Choose the best category
      ↓
Stage 4 → Extract relevant details
      ↓
Stage 5 → Generate a professional response
```

## Available Categories

All customer queries are classified into one of these categories:

- Account Opening
- Billing Issue
- Account Access
- Transaction Inquiry
- Card Services
- Account Statement
- Loan Inquiry
- General Information

## Project Structure

```
bank-support-prompt-chain/
│
├── main.py                               # Main script
├── requirements.txt                      # Python dependencies
├── .env                                  # API keys (not included in repo)
├── .env.example                          # API keys you clone from and update 
├── .gitignore                            # Files to ignore in git
│
└── prompts/
    ├── prompt1_intent.txt                # Stage 1 - Interpret intent
    ├── prompt2_categories.txt            # Stage 2 - Map categories
    ├── prompt3_best_category.txt         # Stage 3 - Choose best category
    ├── prompt4_extract_details.txt       # Stage 4 - Extract details
    └── prompt5_generate_response.txt     # Stage 5 - Generate response
```

## Requirements

- Python 3.10 or higher
- An OpenRouter API key (get one at openrouter.ai)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/bank-support-prompt-chain.git
cd bank-support-prompt-chain
```

### 2. Create a virtual environment

```bash
python -m venv myvenv
source myvenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your `.env` file

Create a file called `.env` in the root of the project:

```
OPENROUTER_API_KEY=your-api-key-here
MODEL_NAME=meta-llama/llama-3.2-3b-instruct:free
```

> Never share or commit your `.env` file. It is already listed in `.gitignore`.

## Usage

Run the script from the command line with a customer query as the first argument:

```bash
python main.py "I noticed a charge of $45 on my account that I did not authorize"
```

### Example Output

```
============================================================
 BANK CUSTOMER SUPPORT - PROMPT CHAIN
============================================================

📝 Customer Query:
   I noticed a charge of $45 on my account that I did not authorize

============================================================
STAGE 1 - What does the customer want?
============================================================
The customer is reporting an unauthorized charge of $45 on their
account and is requesting an investigation.

============================================================
STAGE 2 - Possible categories:
============================================================
1. Billing Issue - The customer is disputing an unrecognized charge.
2. Transaction Inquiry - The customer wants to investigate a transaction.

============================================================
STAGE 3 - Best category:
============================================================
Billing Issue

============================================================
STAGE 4 - Extracted details:
============================================================
MENTIONED: amount ($45)
MISSING: transaction date, merchant name, card type

============================================================
   FINAL RESPONSE
============================================================

Thank you for reaching out to us. We understand you are reporting
an unauthorized charge of $45 on your account and we take this
very seriously. Could you please provide the transaction date and
merchant name so we can investigate further?

============================================================
```

## How It Works

Each stage loads its prompt from a `.txt` file in the `prompts/` folder, fills in the placeholders with real values from the previous stage, and sends it to the AI model. The output of each stage becomes the input of the next.

```
prompt1_intent.txt
contains: {customer_query}
fills in: the real customer message

prompt2_categories.txt
contains: {intent}
fills in: output from stage 1

prompt3_best_category.txt
contains: {intent}, {mapped_categories}, {customer_query}
fills in: outputs from stages 1 and 2

prompt4_extract_details.txt
contains: {chosen_category}, {customer_query}
fills in: output from stage 3

prompt5_generate_response.txt
contains: {customer_query}, {chosen_category}, {extracted_details}
fills in: outputs from stages 3 and 4
```

## Dependencies

| Library | Purpose |
|---------|---------|
| `openai` | Communicates with OpenRouter API |
| `python-dotenv` | Loads API key from `.env` file |

## License

MIT License
