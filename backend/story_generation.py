import os
from dotenv import load_dotenv
from groq import Groq  # Import Groq's SDK
# from langchain_groq import ChatGroq
# from langchain import LLMChain
# from langchain.prompts import PromptTemplate
# from imagegeneration import generate_image
import json
import re
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(
    api_key= groq_api_key 
)

def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else None

def create_story_agent(topic):
    prompt = f"""Create an engaging educative comic story about {topic} with this structure:
    - 3-4 pages, each with exactly 7 panels
    - Pages should have:
      - Famous masked villain(Thanos) causing a problem related to {topic}
      - Famous Superheroes (spiderman, ironman) resolving it through educational content
      - Panel 7 on each page must feature Dr. Gyaan explaining concepts.
    - Format:
        Page 1:
        Panel 1: [Scene description] | [Character]: [Dialogue]
        Panel 2: [Scene description] | [Character]: [Dialogue]
        ...
        Panel 7: Dr. Gyaan: [Educational explanation]
    Make the scene description very long and detailed. The scene description should include all the characters present in the moment. 
    The scene should describe how the character looks every single time. We need to do image generation on these descriptions.
    Make dialogues clear and friendly for kids and the size of a dialogue should be maximum of 20 words.
    Dr. Gyaan should explain the concept in maximum 22 words. Make sure it does not exceed 150 text-characters.
    Focus on {topic} concepts.
    Include dramatic scenes, kid-friendly action, and clear educational content."""
    
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content

# Agent 2: JSON Formatter
def format_json_agent(story_text):
    prompt = """Convert this comic story into perfect JSON format:
    Use this structure:
    {
      "pages": [
        {
          "page_number": 1,
          "panels": [
            {
              "panel_number": 1,
              "scene": "scene description",
              "dialogue": { "speaker": "name", "text": "dialogue" }
            },
            // Panels 2-6...
            {
              "panel_number": 7,
              "scene": null,
              "dialogue": { "speaker": "Dr. Gyaan", "text": "explanation" }
            }
          ]
        }
      ]
    }
    
    Rules:
    - Maintain exact structure
    - Dr. Gyaan ONLY in panel 7
    - scene for panel 7 must be null
    - Keep dialogues under 20 words except Dr. Gyaan
    - Ensure valid JSON syntax
    - The scenes should be descriptive and write the physical characteristics of the characters in the scene.
    - The dialogues should be clear and friendly for kids. Focus on {topic} concepts.
    - Make sure the dialogues are all less than 150 text-characters in length. They should have a maximum of 20-25 words. 
    The story is :

    """
    prompt += story_text
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    json_output= response.choices[0].message.content
    parsed_json = json.loads(extract_json(json_output))
    return parsed_json

# # Main execution
# text_input = "Matter and phases of matter (solid, liquid and gas)"

# # Agent 1 creates story
# story = create_story_agent(text_input)
# print("Generated Story:\n", story)

# # Agent 2 formats to JSON

