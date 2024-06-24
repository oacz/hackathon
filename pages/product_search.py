import os
import streamlit as st
from PIL import Image
import random
import time
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models


from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
    Part,
)

PROJECT_ID = os.environ.get("oacz-genai-es")  # Your Google Cloud Project ID
LOCATION = os.environ.get("europe-west3")  # Your Google Cloud Project Region
vertexai.init(project=PROJECT_ID, location=LOCATION)


#example loading multiple models in this case we load the same model
def load_models():
    """
    Load the generative models for text and multimodal generation.

    Returns:
        Tuple: A tuple containing the text model and multimodal model.
    """
    text_model_pro = GenerativeModel("gemini-1.5-pro-preview-0409")
    multimodal_model_pro = GenerativeModel("gemini-1.5-pro-preview-0409")
    return text_model_pro, multimodal_model_pro

# ... (your existing code for camera input, file upload, etc.)






def about_image(image, prompt): 
    tm, mm = load_models()
    image_part = Part.from_data(image, "image/jpeg")
    prompt_parts = [   
        image_part,
        prompt
    ]
    responses = mm.generate_content(prompt_parts)
    return responses.text

    



# Display Logo at the Top

    # Read and display the logo image
logo_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Google_Cloud_logo.svg/1280px-Google_Cloud_logo.svg.png"
st.image(logo_image, use_column_width=True) 


st.title("Product Search Tool")


# Input field for search bar with placeholder

image_info = st.text_input("", placeholder="Search:")

# Camera Input (Disabled by Default)
use_camera = st.checkbox("Enable Camera")
captured_image = None  # Initialize variable to store captured image

if use_camera:
    captured_image = st.camera_input("Take a picture") 

# Drag-and-Drop Image
img_file_buffer = st.file_uploader("Upload an image (or drag and drop)", type=["jpg", "jpeg", "png"])

# Input field for search bar with placeholder
st.markdown(
    """
    <style>
    .stTextInput > div > div > input {
        font-style: italic; /* Make the placeholder look like a label */
    }
    .stTextInput > div > div > input:focus {
        font-style: normal; /* Remove italic on focus */
    }
    </style>
    """,
    unsafe_allow_html=True,
)





# Display the Image (if available)
if img_file_buffer is not None:
    image = Image.open(img_file_buffer)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write("Image Information:", image_info)
    st.write("About the image:", about_image(img_file_buffer.getvalue(),image_info))

# ... (your existing code)

elif captured_image is not None:
    st.subheader("Captured Image")
    st.image(captured_image, use_column_width=True)
    st.write("Image Information:", image_info)
    st.write("About the image:", about_image(captured_image.getvalue(),image_info))
