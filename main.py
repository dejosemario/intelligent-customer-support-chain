import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize the client (same as Colab)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

def call_llm(prompt_text, system_instructions="You are a helpful banking assistant"):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": prompt_text}
        ],
        model=os.environ.get("MODEL_NAME", "meta-llama/llama-3.2-3b-instruct:free"),
        max_tokens=300
    )
    return response.choices[0].message.content

def load_prompt(filename, **kwargs):
    with open(f"prompts/{filename}", "r") as prompt_file:
        template = prompt_file.read()
    
    for key, value in kwargs.items():
        template = template.replace("{" + key + "}", value)
    
    return template

def run_prompt_chain(customer_query):

    print("\n" + "=" * 60)
    print(" BANK CUSTOMER SUPPORT - PROMPT CHAIN")
    print(f"\n Customer Query:\n {customer_query}")

    #STAGE 1 - read prompt1_intent.txt 
    prompt1 = load_prompt("prompt1_intent.txt", customer_query=customer_query)
    intent = call_llm(prompt1)
    print("=" * 60)
    print("Stage1 - What does the customer want?")
    print("=" * 60)
    print(intent)

    #STAGE 2 - reads prompt2_categories.txt
    # fills in {intent} placeholder
    prompt2 = load_prompt("prompt2_categories.txt", intent=intent)
    mapped_categories = call_llm(prompt2)
    print("\n" + "=" * 60)
    print("STAGE 2 - Possible categories:")
    print("=" * 60)
    print(mapped_categories)

    # STAGE 3 - reads prompt3_best_category.txt
    # fills in {intent}, {mapped_categories}, {customer_query}
    prompt3 = load_prompt(
        "prompt3_best_category.txt",
        intent=intent,
        mapped_categories=mapped_categories,
        customer_query=customer_query
    )
    chosen_category = call_llm(prompt3)
    print("\n" + "=" * 60)
    print("STAGE 3 - Best category:")
    print("=" * 60)
    print(chosen_category)

    # STAGE 4 - reads prompt4_extract_details.txt
    # fills in {chosen_category}, {customer_query}
    prompt4 = load_prompt(
        "prompt4_extract_details.txt",
        chosen_category=chosen_category,
        customer_query=customer_query
    )
    extracted_details = call_llm(prompt4)
    print("\n" + "=" * 60)
    print("STAGE 4 - Extracted details:")
    print("=" * 60)
    print(extracted_details)

    # STAGE 5 - reads prompt5_generate_response.txt
    # fills in {customer_query}, {chosen_category}, {extracted_details}
    prompt5 = load_prompt(
        "prompt5_generate_response.txt",
        customer_query=customer_query,
        chosen_category=chosen_category,
        extracted_details=extracted_details
    )
    final_response = call_llm(prompt5)
    print("\n" + "=" * 60)
    print("STAGE 5 - Final reply to customer:")
    print("=" * 60)
    print(final_response)

    print("\n" + "=" * 60)
    print("   FINAL RESPONSE")
    print("=" * 60)
    print(f"\n{final_response}\n")
    print("=" * 60)    


# ENTRY POINT
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(" Please provide a customer query.")
        print('Usage: python main.py "your query here"')
        sys.exit()
    
    customer_query = sys.argv[1]
    run_prompt_chain(customer_query)
