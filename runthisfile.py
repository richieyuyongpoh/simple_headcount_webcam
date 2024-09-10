

import streamlit as st
import openai
import base64
import requests


my_key = st.secrets["checkitout"]
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


st.title("Headcount Estimation")

# Initialize camera input
img_file_buffer = st.camera_input("Say CHEESE and take the photo. AI will do the rest.")



if img_file_buffer is not None:

    with open ('test.jpg','wb') as file:
      file.write(img_file_buffer.getbuffer())


    base64_image = encode_image('test.jpg')
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {my_key}"
    }

    payload = {
      "model": "gpt-4o-mini",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Count the number of heads visible in the image. Return only the number."
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)


    # Extract headcount from OpenAI response


    headcount = int(response.json()['choices'][0]['message']['content'])

    # Display headcount and volume recommendation
    st.write(f"Headcount: {headcount}")

    if headcount < 1:
      st.write("Small volume is needed.")
    elif 1 <= headcount < 2:
      st.write("Medium volume is needed.")
    else:
      st.write("Large volume is needed.")
