from story_generation import create_story_agent, format_json_agent
from image_prompt_generation import process_json2
from imagetopanel import convert_to_panel
from pagestopdf import convert_to_pdf
import json

def the_final(input_text):
    print("IT GOES IN")
    story_text=create_story_agent(input_text)
    json_output=format_json_agent(story_text)
    with open("generated_story.json", "w") as file:
        json.dump(json_output, file, indent=4) 
    image_gen=process_json2(json_output)
    convert_to_panel(json_output)
    convert_to_pdf()


