from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_meme_text(context):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a meme generator. Create a short, funny meme caption based on the given context."},
            {"role": "user", "content": f"Context: {context}\n\nGenerate a meme caption:"}
        ],
        max_tokens=30,
        n=1,
        temperature=0.8,
    )
    return response.choices[0].message.content.strip()

def generate_meme(context):
    # Generate meme text
    meme_text = generate_meme_text(context)

    # List of background images (you should have these in an 'images' folder)
    background_images = ['meme_bg_1.jpg', 'meme_bg_2.jpg', 'meme_bg_3.jpg']
    
    # Choose a random background
    background = Image.open(f'images/{random.choice(background_images)}')
    
    # Create a drawing object
    draw = ImageDraw.Draw(background)
    
    # Choose a font
    font = ImageFont.truetype("arial.ttf", 36)
    
    # Wrap the text
    wrapped_text = textwrap.wrap(meme_text, width=20)
    
    # Calculate the total height of the text
    text_height = len(wrapped_text) * 40
    
    # Calculate the starting Y position to center the text vertically
    y_text = (background.height - text_height) / 2
    
    # Draw each line of text
    for line in wrapped_text:
        line_width, line_height = draw.textsize(line, font=font)
        x_text = (background.width - line_width) / 2
        draw.text((x_text, y_text), line, font=font, fill="white", stroke_width=2, stroke_fill="black")
        y_text += line_height
    
    return background