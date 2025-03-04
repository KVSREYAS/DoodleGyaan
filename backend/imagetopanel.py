from cpy_2 import make_panel
import json

# with open("generated_story.json", "r") as file:
#     json_output = json.load(file)
def create_dialogue(diag_dict):
    tempstr=diag_dict['speaker']+':'+diag_dict['text']
    return tempstr
def convert_to_panel(json_output):
    total_pages=len(json_output['pages'])
    print(total_pages)
    for i in range(1,total_pages+1):
        #print(create_dialogue(json_output['pages'][i]['panels'][0]['dialogue']))
        make_panel([
        [create_dialogue(json_output['pages'][i-1]['panels'][6]['dialogue'])],
        [f"comics_generated_2/page_{i}_panel_1.png", create_dialogue(json_output['pages'][i-1]['panels'][0]['dialogue'])],
        [f"comics_generated_2/page_{i}_panel_2.png", create_dialogue(json_output['pages'][i-1]['panels'][1]['dialogue'])],
        [f"comics_generated_2/page_{i}_panel_3.png", create_dialogue(json_output['pages'][i-1]['panels'][2]['dialogue'])],
        [f"comics_generated_2/page_{i}_panel_4.png", create_dialogue(json_output['pages'][i-1]['panels'][3]['dialogue'])],
        [f"comics_generated_2/page_{i}_panel_5.png", create_dialogue(json_output['pages'][i-1]['panels'][4]['dialogue'])],
        [f"comics_generated_2/page_{i}_panel_6.png", create_dialogue(json_output['pages'][i-1]['panels'][5]['dialogue'])]
        ],f"comic_pages/page_no_{i}.png")
# print(json_output)
# convert_to_panel(json_output)

# make_panel([
# ["hello"],
# ["page_1_panel_1.png", "hello"],
# ["page_1_panel_2.png", "hello"],
# ["page_1_panel_3.png", "hello"],
# ["page_1_panel_4.png", "hello"],
# ["page_1_panel_5.png", "hello"],
# ["page_1_panel_6.png","hello"]
# ])

# make_panel([
#     ["THE DAWN AWAKENS THE EPIC TALE OF HEROISM AND MYSTERY, SETTING THE STAGE FOR UNFORGETTABLE BATTLES."],
#     ["grok_sample.png", "THE SHADOW STRIKES SILENTLY, UNLEASHING A CASCADE OF CHAOS ON THE UNWARY."],
#     ["grok_sample2.png", "WITH THE MIGHT OF THE STARS, THE HERO RISES TO DEFY THE ODDS."],
#     ["grok_sample.png", "AN UNEXPECTED ALLIANCE IS FORMED UNDER THE SILVER GLEAM OF THE MOON."],
#     ["grok_sample2.png", "THE VILLAIN LAUGHS, NAIVELY THINKING DEFEAT IS UNAVOIDABLE."],
#     ["grok_sample.png", "A WHISPER OF HOPE ECHOES BRIEFLY THROUGH THE STARLIT NIGHT."],
#     ["grok_sample2.png", "IN THE FINAL MOMENT, DESTINY IS REWRITTEN WITH UNYIELDING COURAGE."]
# ])
