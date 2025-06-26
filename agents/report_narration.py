import os
import pyttsx3
import markdown2
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime


def read_markdown_file(filepath):
    """
    Reads a markdown (.md) file and returns its content as a string.

    Args:
        filepath (str): The path to the markdown file.

    Returns:
        str: The content of the markdown file.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there's an issue reading the file.
    """
    if not filepath.lower().endswith(".md"):
        raise ValueError("File must be a markdown (.md) file.")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"Markdown file not found: {filepath}")
    except IOError as e:
        raise IOError(f"Error reading file {filepath}: {e}")


def narrate_cricket_report(markdown_report):
    """
    Reads a cricket report in markdown format, converts it to a narrative speech,
    speaks it using a voice agent with sports spirit, and saves the audio to a file.
    
    Args:
        markdown_report (str): The markdown content of the cricket report.
    
    Returns:
        str: The filename of the saved audio file.
    """
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    client = Groq(api_key=GROQ_API_KEY)
    plain_text = markdown2.markdown(markdown_report)
    plain_text = plain_text.replace("\n", " ")
    
    prompt = f"""
    You are an expert in creating dynamic and engaging narrative speech for cricket reports on player(s) or match(es), with a focus on embodying the vibrant sports spirit. I have provided a markdown file containing a cricket match report or player(s) performance details report. Your task is to:

    Analyze the markdown file and extract key details such as the match outcome, key moments, player performances, scores, and any notable events.
    Convert the extracted information into a concise, high-energy, and conversational narrative speech suitable for a voice agent to deliver. The speech should:
    Exude sports spirit, with an enthusiastic, passionate, and spirited tone that captures the thrill and excitement of cricket, inspiring listeners as if they're reliving the match or player's performance.
    Make sure you include all the numbers present in the markdown content, such as scores, statistics, and any other relevant figures, but present them in a way that enhances the narrative flow rather than overwhelming the listener with data.
    Include a lively introduction, vivid highlights of key moments, and a rousing conclusion summarizing the match or player's contribution.
    Avoid overly technical jargon, keeping it accessible and captivating for a general sports audience.
    Be structured for spoken delivery, with a tone that mirrors the energy of live sports commentary or a spirited post-match summary.
    Keep the duration suitable for a 1-2 minute speech, unless specified otherwise.
    Ensure the narrative flows smoothly, emphasizing dramatic moments, standout performances, and the overall context of the match or player's role, while infusing a sense of camaraderie, competition, and sportsmanship.
    Do not include markdown syntax or formatting in the final speech; output plain text ready for a voice agent to read aloud.
    Here is the markdown content to process:

    {plain_text}

    Please provide the narrative speech as plain text, ready for my voice agent to use, with the sports spirit shining through in every line.
    """
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        narration = response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Failed to generate narration: {str(e)}")
    
    print("\nGenerated Narration:\n")
    print(narration)

    # Speak the narration
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)
    engine.setProperty('volume', 1.0)
    engine.say(narration)
    engine.runAndWait()

    # Save to audio file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_filename = f"cricket_narration_{timestamp}.mp3"
    engine.save_to_file(narration, audio_filename)
    engine.runAndWait()

    return audio_filename

if __name__ == "__main__":
    markdown_content = read_markdown_file("reports/Indian_Batsmen_Batting_Statistics_and_T20_Recommendation.md")
    audio_file = narrate_cricket_report(markdown_content)
    print(audio_file)
