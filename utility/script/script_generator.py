import os
from openai import OpenAI
import json
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_KEY')
model = "gpt-4o-mini"

def generate_script(topic):
    prompt = (
        """You are a creative storyteller who specializes in crafting very short, impactful moral stories for all ages based on user input, which will be given in Sanskrit.\n\nIf the input is in Sanskrit, you must first translate or interpret it to understand the intended topic, and then write a short fiction story or folktale (<140 words) with a clear moral.\n\nEach story should have a clear beginning, middle, and end, and end with a 1-line moral or lesson explicitly stated.\n\n# Output Format\nStrictly respond with a single valid JSON object like this: {\"script\": \"Story... Moral: ...\" }\n\nOnly return this object and nothing else.\n\n# Example\nInput: \n\"सत्यं वद\" ("Speak the truth")\n\nOutput:\n{\"script\": \"Once there was a boy who always spoke the truth, even when it was hard. His honesty earned everyone’s trust. One day, his truthfulness saved his village from danger. Moral: Always speak the truth.\"}\n\nNow, using the given Sanskrit input, generate a brief, engaging, and unique story with a clear moral, in the above JSON format.\n\n--\n"""
    )
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": topic}
        ]
    )
    content = response.choices[0].message.content.strip()
    # Try to parse JSON directly
    try:
        script = json.loads(content)["script"]
    except Exception:
        # Attempt to extract JSON substring if extra text is present
        json_start_index = content.find('{')
        json_end_index = content.rfind('}')
        if json_start_index != -1 and json_end_index != -1:
            json_str = content[json_start_index:json_end_index+1]
            script = json.loads(json_str)["script"]
        else:
            raise ValueError("Could not find valid JSON in response:\n" + content)
    return script
