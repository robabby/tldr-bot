import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
from summarizer import summarize_text
from sassy_generator import generate_sassy_response
from meme_generator import generate_meme
from io import BytesIO

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="tldr", description="Provide a shitty TL;DR of recent messages")
async def tldr(interaction: discord.Interaction):
    await interaction.response.defer()
    
    try:
        # Get the last 10 messages in the channel
        messages = []
        async for message in interaction.channel.history(limit=10):
            messages.append(message.content)
        
        if not messages:
            await interaction.followup.send("No recent messages found to summarize.")
            return

        text = "\n".join(messages)

        # Generate summary
        summary = summarize_text(text)

        # Generate sassy response
        sassy_tldr = generate_sassy_response(summary, style="tldr")

        await interaction.followup.send(f"TLDR:\n\n{sassy_tldr}")
    except discord.errors.Forbidden:
        await interaction.followup.send("Oops! I don't have permission to read message history in this channel. Please ask an admin to grant me the 'Read Message History' permission.")
    except Exception as e:
        await interaction.followup.send(f"An error occurred while processing your request: {str(e)}")

@bot.tree.command(name="meme", description="Generate a meme based on recent conversations")
async def meme(interaction: discord.Interaction):
    await interaction.response.defer()
    
    try:
        # Get the last 10 messages in the channel
        messages = []
        async for message in interaction.channel.history(limit=10):
            messages.append(message.content)
        
        if not messages:
            await interaction.followup.send("No recent messages found to generate a meme.")
            return

        text = "\n".join(messages)

        # Generate meme
        meme_image = generate_meme(text)

        # Convert PIL Image to bytes
        with BytesIO() as image_binary:
            meme_image.save(image_binary, 'PNG')
            image_binary.seek(0)
            
            # Send the meme as an attachment
            await interaction.followup.send("Here's your meme based on recent conversations:", file=discord.File(fp=image_binary, filename='meme.png'))
    except discord.errors.Forbidden:
        await interaction.followup.send("Oops! I don't have permission to read message history in this channel. Please ask an admin to grant me the 'Read Message History' permission.")
    except Exception as e:
        await interaction.followup.send(f"An error occurred while processing your request: {str(e)}")

if __name__ == "__main__":
    bot.run(TOKEN)