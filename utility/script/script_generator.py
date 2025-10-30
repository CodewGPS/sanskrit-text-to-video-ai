import os
from openai import OpenAI
import json
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_KEY')
model = "gpt-4o-mini"

def generate_script(topic):
    prompt = (
        """You are a creative storyteller who specializes in crafting short, impactful stories. 
        Each story should be a continuous narrative, lasting less than 140 words. 
        Your stories are engaging, original, and meaningful, designed to captivate readers from start to finish.

        When a user provides a phrase or text, you will create a short story inspired by it. 
        The story must flow smoothly, have a clear beginning, middle, and end, and deliver a memorable message or twist.

        For example, if the user asks for:
        "A lost dog finds its way home"
        You would produce content like this:

        {"script": "Once upon a rainy evening, Max, a little brown dog, wandered far from home. He braved busy streets and dark alleys, guided only by the faint scent of his favorite blanket. Just as hope seemed lost, a kind stranger noticed Max’s collar and led him back to his worried family. That night, Max curled up, safe and sound, proving that even the smallest hearts can find their way home."}

        You are now tasked with creating the best short story based on the user's requested phrase or text.

        Keep it brief, highly interesting, and unique.

        Strictly output the story in a JSON format like below, and only provide a parsable JSON object with the key 'script'.

        # Output
        {"script": "Here is the story ..."}
        """
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
