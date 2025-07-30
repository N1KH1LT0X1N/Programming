
import discord
import google.generativeai as genai
from config import DISCORD_TOKEN, GEMINI_API_KEY

# Configure the generative AI model
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Read the FAQ file
with open('FAQ.md', 'r') as f:
    faq_content = f.read()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        # Ignore messages from the bot itself
        if message.author == self.user:
            return

        # Check if the bot is mentioned
        if self.user.mentioned_in(message):
            # Extract the question from the message
            question = message.content.replace(f'<@!{self.user.id}>', '').strip()

            # Create the prompt for the generative model
            prompt = f"""
            You are a helpful Discord bot that answers questions based on the following FAQ content.
            If the answer is not in the FAQ, say that you cannot answer the question.

            FAQ Content:
            {faq_content}

            Question: {question}
            """

            # Generate the response
            response = model.generate_content(prompt)

            # Send the response
            await message.channel.send(response.text)

def run_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run(DISCORD_TOKEN)
