import requests
from dotenv import load_dotenv
import os
load_dotenv()
sd_api = os.getenv("sd_api")
def image_gen(prompt,image_path):
    # prompt='''The cityscape, once a backdrop for destruction, now begins to heal as the superheroes gain the upper hand against Thanos. Spider-Man, Iron Man, Captain America, and other heroes are spread across the panel, each engaged in their own fierce battle against Thanos. The Mad Titan, wielding the Infinity Gauntlet, towers over the heroes, his face a mixture of rage and desperation. The sky above is filled with the vibrant colors of sunset, but the atmosphere is tense, with lightning-like energy crackling from the Gauntlet, illuminating the darkening sky. In the foreground, Spider-Man leaps towards Thanos, his webs shooting out in all directions, while Iron Man flies in from the side, repulsor beams charging. Captain America stands firm, his shield glowing with a faint, golden light, ready to deflect any incoming attack. The heroes' costumes are vibrant, contrasting against the dark, shadowy figure of Thanos. The battle rages on, with debris and dust swirling around the combatants, dynamic lines and dramatic shading capturing the intensity and urgency of the moment. Spider-Man's speech bubble is prominent, 'We're almost there!' he exclaims, his determination and hope inspiring his fellow heroes to push forward. The art style is classic Marvel, with bold, expressive characters and dynamic action, drawing the viewer into the heart of the battle.'''
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "authorization": sd_api,
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": prompt,
            "output_format": "png",
            "model":"sd3.5-large-turbo",
            "aspect_ratio":"5:4"
        },
    )

    if response.status_code == 200:
        with open(f"./comics_generated_2/{image_path}.png", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))
#prompt='''Generate an image based on this scene description:Iron Man soars into the frame, his suit gleaming with a golden aura as he joins Spider-Man in the battle against Thanos. Spider-Man is seen web-slinging towards Thanos, who stands tall, his twisted device emitting a dark, corrupted energy that spreads across the city park, withering trees and plants. The device itself is a mass of dark, thorny vines and twisted metal, pulsing with an otherworldly power. The sky is a deep, foreboding grey, with clouds that seem to be twisted and corrupted by the device's influence. Iron Man's repulsor beams are charged and ready, illuminating the darkening landscape, while Spider-Man's webs glow with a faint, determined light. Thanos, towering over the heroes, his face a mask of relentless ambition, raises a hand to summon more dark energy. The scene is filled with dynamic movement, Iron Man's flight trail blazing behind him, Spider-Man's webs stretching across the panel, and Thanos's dark energy swirling around him. The art style is reminiscent of classic Marvel illustrations, with bold lines, dramatic shading, and an emphasis on capturing the intensity of the battle. The heroes are positioned in a way that showcases their determination and bravery, with Iron Man and Spider-Man forming a united front against the formidable villain.'''
#image_gen(prompt,'trial1')