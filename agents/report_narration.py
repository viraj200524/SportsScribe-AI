import os
import markdown2
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime
import asyncio
import edge_tts

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


async def generate_edge_tts(text, voice, output_file, rate="+15%"):
    communicate = edge_tts.Communicate(text, voice, rate=rate,pitch="-8Hz", volume="+20%")
    await communicate.save(output_file)

def narrate_cricket_report(markdown_report):
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables")

    client = Groq(api_key=GROQ_API_KEY)
    plain_text = markdown2.markdown(markdown_report).replace("\n", " ")

    prompt = f"""
You are a master of high-octane, emotionally-charged narrative speech tailored for cricket reports—whether it’s a thrilling match recap, an electrifying player performance, or a blend of both. Your mission is to transform the given markdown content into an exhilarating spoken story that brings the spirit of the game roaring to life.

**Input:** A markdown content containing a cricket match report or player performance summary.

**Your task:**
1. **Extract & analyze**: Identify all key elements—match outcome, turning points, player highlights, scores, milestones, and standout stats and other important things from the report.
2. **Narrate with flair**: Transform the information into a crisp, high-energy, and vivid sports commentary-style narrative. The delivery should feel like a professional voiceover for a cricket highlights reel or a post-match wrap-up on a major sports channel and it should also be suitable for a podcast or a sports radio show.

**Tone & Style:**
- The tone must be **conversational, passionate, and spirited**, bursting with enthusiasm as if the audience is reliving the highs and lows of the game.
- Absolutely **no generic intros** like “Here is the narration” or “This is the speech.” Jump straight into the energy of the moment with a **captivating opening line** that hooks the listener instantly.
- Structure it like an actual spoken commentary with **rising momentum**: start with an exciting intro, escalate through dramatic moments, and end with a punchy conclusion that celebrates the essence of the match or the player's performance.
- Use all numerical stats (scores, wickets, milestones, etc.) from the markdown, but **weave them seamlessly** into the narrative—**never data-dump**. They should elevate the excitement, not bog it down.
- Avoid technical jargon that might alienate casual fans. Make it accessible, engaging, and inclusive.

**Accent & Pronunciation:**
- The voiceover will be delivered in an **American accent**. Therefore, ensure all **Indian names (e.g., Virat Kohli, Rohit Sharma) and cricket-specific Indian terms** are written in a way that **sounds natural and respectful in an American accent**, while retaining their **Indian identity and essence**. Spell or format names phonetically if needed to guide correct Americanized pronunciation without distorting their meaning or cultural significance.

**Duration & Format:**
- Length should suit a **1-2 or 2-3 minute voiceover** (unless specified otherwise).
- Do not include any markdown syntax. Output the narrative as **plain text**, polished and ready for use in a voice agent or speech system.

**Deliver with impact**: The listener should feel the roar of the crowd, the pulse of the final over, the thrill of a boundary, and the pride of a match-winning spell. Make them feel like they were *right there*.

Here is the markdown content to convert into your electric narration speech:

{plain_text}
"""
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    narration = response.choices[0].message.content.strip()
    # print it if needed

    # Choose an Indian voice (e.g. en-IN-NeerjaNeural)
    voice = "en-IN-NeerjaNeural"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_filename = f"cricket_narration_{timestamp}.mp3"

    asyncio.run(generate_edge_tts(narration, voice, audio_filename))
    return audio_filename

if __name__ == "__main__":
    markdown_content = read_markdown_file("../reports/Jasprit_Bumrah_Bowling_Report.md")
    audio_file = narrate_cricket_report(markdown_content)
    print(audio_file)
