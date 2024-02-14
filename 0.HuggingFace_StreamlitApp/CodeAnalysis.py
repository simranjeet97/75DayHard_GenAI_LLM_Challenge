import streamlit as st
from transformers import pipeline

# Function for code analysis using code transformer
def analyze_code_transformer(input_code):
    try:
        # Set up the text2text-generation pipeline
        code_analyzer = pipeline("text2text-generation", model="openai/whisper-large")

        # Generate analysis using a prompt
        prompt = f"Analyze the following code and Explain:\n\n{input_code}\n\nAnalysis:"
        analysis = code_analyzer(prompt, max_length=200, min_length=50, length_penalty=2.0)[0]['generated_text']

        return analysis
    except Exception as e:
        return f"Error during analysis: {e}"

# Streamlit app layout
st.title("Code Analyzer using Transformers")

# Input code area
input_code = st.text_area("Enter Code:")

# Analyze button
if st.button("Analyze Code") and input_code:
    st.subheader("Code Analysis:")
    result = analyze_code_transformer(input_code)
    st.write(result)
