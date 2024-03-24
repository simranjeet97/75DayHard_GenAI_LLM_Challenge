import streamlit as st
import requests
import PIL
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import google.generativeai as genai

GOOGLE_API_KEY='AIzaSyC9GQWuQIEmB1t9R0bk4PPElx3Y6eucbZ8'
genai.configure(api_key=GOOGLE_API_KEY)
vision_model = genai.GenerativeModel('gemini-pro-vision')

# Function to fetch image from URL
@st.cache_data
def fetch_image(image_url):
    result = requests.get(image_url)
    try:
        image = PIL.Image.open(BytesIO(result.content))
        return image
    except PIL.UnidentifiedImageError:
        st.error("Error: Unidentified image format.")
        return None

# Main function for the Streamlit app
def main():
    # Input field for Image URL
    st.sidebar.subheader("Enter Image URL:")
    image_url = st.sidebar.text_input("")

    # Fetch and display image if URL is provided
    if image_url:
        image = fetch_image(image_url)
        if image:
            st.sidebar.image(image, caption='Image', use_column_width=True)

            # Vision model processing
            st.title("Chat with Graphs")
            st.write("Ask any query about the image:")

            # Input field for user query
            user_input = st.text_input("Your Query:")

            # Submit button for user query
            if st.button("Submit"):
                if user_input:
                    # Generate response from vision model
                    response = vision_model.generate_content([user_input, image])
                    st.text_area("Model's Response:", value=response.text, height=150, max_chars=None)






if __name__ == "__main__":
    main()