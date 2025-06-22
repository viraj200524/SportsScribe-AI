from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv
import assemblyai as aai
from SportsJournalist import SportsJournalistTeam
load_dotenv()

telegram_token = os.getenv("TELEGRAM_TOKEN")
groq_api_key = os.getenv("GROQ_API_KEY")
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=groq_api_key,
)

def handle_response(text: str) -> str:
    messages = [
        SystemMessage(content="You are a helpful assistant that answers user queries."),
        HumanMessage(content=text),
    ]
    ai_msg = llm.invoke(messages)
    return ai_msg.content

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    response = handle_response(user_message)
    await update.message.reply_text(response)

async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.voice:
        file = await update.message.voice.get_file()
        file_path = file.file_path
        config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)
        transcript = aai.Transcriber(config=config).transcribe(file_path)
        if transcript.status == "error":
            await update.message.reply_text(f"Transcription failed: {transcript.error}")
            return
        response = handle_response(transcript.text)
        await update.message.reply_text(response)

if __name__ == "__main__":
    print("Starting Bot...")
    application = ApplicationBuilder().token(telegram_token).build()

    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice_message))
    
    async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        print(f"Update {update} caused error {context.error}")
    application.add_error_handler(error_handler)
    
    print("Bot Polling...")
    application.run_polling(poll_interval=3)