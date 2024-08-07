import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
from summarizer import summarize_text
from sassy_generator import generate_sassy_response

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

@bot.tree.command(name="summarize", description="Summarize the given text in a dick-ish tone")
@app_commands.describe(text="The text to summarize")
async def summarize(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    
    # Generate summary
    summary = summarize_text(text)

    # Generate sassy response
    sassy_summary = generate_sassy_response(summary)

    await interaction.followup.send(f"Here's your sassy summary:\n\n{sassy_summary}")

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

        await interaction.followup.send(f"TL;DR:\n\n{sassy_tldr}")
    except discord.errors.Forbidden:
        await interaction.followup.send("Oops! I don't have permission to read message history in this channel. Please ask an admin to grant me the 'Read Message History' permission.")
    except Exception as e:
        await interaction.followup.send(f"An error occurred while processing your request: {str(e)}")

@bot.tree.command(name="minutes", description="Generate satirical 'meeting minutes' from recent messages")
async def minutes(interaction: discord.Interaction):
    await interaction.response.defer()
    
    try:
        # Get the last 50 messages in the channel
        messages = []
        async for message in interaction.channel.history(limit=50):
            messages.append(f"{message.author.name}: {message.content}")
        
        if not messages:
            await interaction.followup.send("No recent messages found to summarize.")
            return

        text = "\n".join(messages)

        # Generate summary
        summary = summarize_text(text)

        # Generate sassy response
        sassy_minutes = generate_sassy_response(summary, style="minutes")

        await interaction.followup.send(f"Here are your 'professional' meeting minutes:\n\n{sassy_minutes}")
    except discord.errors.Forbidden:
        await interaction.followup.send("Oops! I don't have permission to read message history in this channel. Please ask an admin to grant me the 'Read Message History' permission.")
    except Exception as e:
        await interaction.followup.send(f"An error occurred while processing your request: {str(e)}")

if __name__ == "__main__":
    bot.run(TOKEN)