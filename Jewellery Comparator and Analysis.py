import base64

import cv2
import gradio as gr
import numpy as np
import requests
import urllib.request 
import base64
from PIL import Image 

MARKDOWN = """
# JEWELLERY IMAGE ATTRIBUTER
<p align="center">
    <img width="150" src="data:image/png;base64,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" alt="hotdog">
</p>
"""
API_URL = "https://api.openai.com/v1/chat/completions"
CLASSES = ["Floral Design Traditional Jewelry", "Animal Design Traditional Jewelry", "Floral Design Modern Jewelry","Animal Design Modern Jewelry","Flo"]

def encode_image_to_base64(image_url: str) -> str:
    urllib.request.urlretrieve( image_url) 
  
    #img = Image.open("gfg.png") 

    with open("gfg.png", "rb") as img_file:
        base64_string = base64.b64encode(img_file.read()).decode()
    return base64_string

def compose_payload(image_url: str, prompt: str) -> dict:
    base64_image = encode_image_to_base64(image_url)
    return {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url":  f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }


def compose_classification_prompt(classes: list) -> str:
    # return(f"Can you describe the jewelry, its design, etc")
    # return(f"Describe the design (floral/ geometric/ animal),style (Modern/Traditional), embeddings (precious stones-(also mention what stone it is -ruby/emerald/or any other that you can identify)/enamels-(also mention color of the enamel)/bead- (also mention color of the bead)/plain jewellery), metal color (yellow gold/antique/geru/white gold/rose gold/platinum/Red Antique). Give output for each attribute like a json. If multiple attributes are present, concatenate using a '-'. Summarise each point in one line.")
    return(f"You are examining Indian jewelry. Please describe the following attributes:"
           f"Design: Identify the design style as Floral, Geometric, Animal, or Generic. For instance, if the design features plants or plant-like motifs, categorize it as Floral. If it incorporates geometric shapes or patterns, classify it as Geometric. If it resembles animals, birds, or insects, mark it as Animal.If it has any religious markings, like indian gods or christian cross or somethingthat represents any religious sentiments, specify faith and belief. If none of these apply, label it as Generic,"
           f"Style: Determine whether the style is Modern or Traditional. If it looks edgy or contemporary, classify it as Modern. If it features traditional Indian designs, categorize it as Traditional,"
           f"Type: Determine if the jewelry is Heavy or Lightweight."
           f"Dominance: Indicate whether the jewelry is Gold Dominant or Stone Dominant. Gold Dominant suggests that gold plays a more significant role in the design, while Stone Dominant implies that gemstones are the central element."
           f"Provide the output for each attribute in a structured format like JSON. Use hyphens to concatenate multiple attributes (e.g., Floral-Traditional for a jewelry piece with a floral design and traditional style)."
           f"if the design is equally a combo of two, you can concatenate using '-' and give."
           f"However, give designs and design combos among floral/geometric/animal/generic only"
           f"For style, return only Modern/Traditional - what will suit the product the most. Dont give a concatenated result"
           f"Polki jewellery usually has raw and uncut stones with absolutely no processing while Kundan jewellery is made of glass stones. Gold and diamond content in polki jewellery is more than that in Kundan jewellery."
           f"Polki jewellery is much heavier than Kundan jewellery. The shine of polki jewellery is much more lustrous than Kundan jewellery's shine.The undersides of Kundan jewellery is enamelled while polki jewellery is made with a gold foil at the back."
           f"If the primary focus or prominent feature of the jewelry is the gold component, return gold dominant. It suggests that gold plays a more significant role in the overall design or visual impact."
           f"If the primary emphasis of the jewelry is on the gemstones, return stone dominant. It implies that the stones, whether they are diamonds, pearls, or other gems, are the central and most noticeable element of the piece."
           f"Make it in a structured format.")

def compose_headers(api_key: str) -> dict:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }


def prompt_image(api_key: str, image_url: str, prompt: str) -> str:
    headers = compose_headers(api_key=api_key)
    payload = compose_payload(image_url=image_url, prompt=prompt)
    response = requests.post(url=API_URL, headers=headers, json=payload).json()

    if 'error' in response:
        raise ValueError(response['error']['message'])
    return response['choices'][0]['message']['content']


def classify_image(image_url: str) -> str:
    prompt = compose_classification_prompt(classes=CLASSES)
    response = prompt_image(api_key="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", image_url=image_url, prompt=prompt)
    return response


with gr.Blocks() as demo:
    gr.Markdown(MARKDOWN)
    with gr.TabItem("Basic"):
        with gr.Column():
            input_image_url = gr.TextArea(label="Image URL")
            output_text = gr.Textbox(
                label="Output")
            submit_button = gr.Button("Submit")

        submit_button.click(
            fn=classify_image,
            inputs=[input_image_url],
            outputs=output_text)
demo.launch(debug=False, show_error=True, share=True)
