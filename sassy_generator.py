from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_sassy_response(summary, style="default"):
    if style == "tldr":
        prompt = f"Generate a sassy and sarcastic TL;DR version of this summary:\n\n{summary}\n\nSassy TL;DR:"
    elif style == "minutes":
        prompt = f"Generate satirical 'meeting minutes' based on this summary, in a sassy and sarcastic tone:\n\n{summary}\n\nSatirical Meeting Minutes:"
    else:
        prompt = f"Rewrite this summary in a sassy and sarcastic tone:\n\n{summary}\n\nSassy Summary:"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a sassy and sarcastic assistant who acts like Louis CK."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        n=1,
        temperature=0.8,
    )

    return response.choices[0].message.content.strip()