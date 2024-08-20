import os
import io
import streamlit as st
from PIL import Image
from typing import Dict
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI
PROJECT_ID = os.environ.get("your-project-id")  # Your Google Cloud Project ID
LOCATION = os.environ.get("europe-west3")  # Your Google Cloud Project Region
vertexai.init(project=PROJECT_ID, location=LOCATION)



# Streamlit app
st.title("Image Generation with Imagen 3")

# Prompt input
prompt = st.text_area("Enter your prompt:", "A photo of a cat")

# Number of images slider
num_images = st.slider("Number of images:", 1, 4, 1)

VISION_MODEL = "imagegeneration@006"
ASPECT_RATIOS_OPTIONS = ["1:1", "9:16", "16:9", "3:4", "4:3"]
GUIDANCE_SCALE = 90  # Controls the strength of the prompt. Suggested values are:* 0-9 (low strength) * 10-20 (medium strength)* 21+ (high strength)
SEED = 915

def generate_images(
    gemini_prompt: str, aspect_ratio_provided: str
) -> vertexai.preview.vision_models.ImageGenerationResponse:
    """Generates images using imagen@006."""
    image_model = ImageGenerationModel.from_pretrained(VISION_MODEL)

    prompt = gemini_prompt

    images = image_model.generate_images(
        prompt=prompt,
        number_of_images=num_images,
        guidance_scale=GUIDANCE_SCALE,
        aspect_ratio=aspect_ratio_provided,
        # You can't use a seed value and watermark at the same time.
        add_watermark=False,
        seed=SEED,
    )
    return images

# Generate images button
if st.button("Generate"):
    if prompt:
        with st.spinner("Generating images..."):
            # Generate images
            response = generate_images(prompt,"4:3")
            
            st.write("Generated Images:")
            
           # Display generated images as clickable thumbnails
            for i, img in enumerate(response.images):
                # Create columns for layout
                 
              
                    # Display thumbnail with click to expand
                    st.image(img._pil_image, use_column_width=True)
                
    else:
        st.warning("Please enter a prompt.")