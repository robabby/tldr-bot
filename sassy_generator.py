from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_sassy_response(summary, style="default"):
    if style == "tldr":
        prompt = f"Act as the comedian Louis CK and generate a sassy and sarcastic TLDR version of this summary:\n\n{summary}\n\nTLDR:"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You act as the comedian Louis CK."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        n=1,
        temperature=0.8,
    )

    return response.choices[0].message.content.strip()