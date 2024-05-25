import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io

# Set up OpenAI API key
client = OpenAI()

st.title("Tech Support Chatbot with Vision")

# Function to encode the image to base64
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# User input
user_input = st.text_input("Ask your question here")

uploaded_file = st.file_uploader("Or upload a screenshot:", type=["png", "jpg", "jpeg"])

if st.button("Send"):
    messages = [{"role": "user", "content": [{"type": "text", "text": user_input}]}]
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Screenshot.', use_column_width=True)
        base64_image = encode_image(image)
        messages[0]["content"].append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
        })

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=300
    )

    answer = response.choices[0].message['content'] if 'content' in response.choices[0].message else response.choices[0].message
    st.write(answer)
