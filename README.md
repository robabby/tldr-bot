To run the bot using Docker:

- Ensure you have Docker and Docker Compose installed on your system.
- Place all the files (bot.py, summarizer.py, sassy_generator.py, Dockerfile, docker-compose.yml, requirements.txt, and .env) in the same directory.
- Replace the placeholder values in the .env file with your actual Discord bot token and OpenAI API key.
- Open a terminal, navigate to the directory containing your files, and run:
```
docker-compose up --build
```