# Day 16/75 Hard GenAI

import streamlit as st
from transformers import pipeline

# Create separate functions for each NLP task
def summarize_text(input_text):
    summarizer = pipeline("summarization")
    summary = summarizer(input_text, max_length=150, min_length=50, length_penalty=2.0)[0]['summary_text']
    return summary

def classify_text(input_text):
    classifier = pipeline("sentiment-analysis")
    classification = classifier(input_text)[0]['label']
    return classification

def rephrase_text(input_text):
    rephraser = pipeline("text2text-generation", model="facebook/bart-large-cnn")
    rephrased_text = rephraser(input_text, max_length=100, min_length=20)[0]['generated_text']
    return rephrased_text

# Streamlit app layout
st.title("Hugging Face Transformers App")

# Sidebar with task selection
selected_task = st.sidebar.selectbox("Select NLP Task:", ["Summarization", "Text Classification", "Text Rephrasing"])

# Input text area
input_text = st.text_area("Enter Text:")

# Buttons to trigger tasks
if st.button("Process"):
    if selected_task == "Summarization" and input_text:
        st.subheader("Summary:")
        result = summarize_text(input_text)
        st.write(result)

    elif selected_task == "Text Classification" and input_text:
        st.subheader("Classification:")
        result = classify_text(input_text)
        st.write(f"The text is classified as: {result}")

    elif selected_task == "Text Rephrasing" and input_text:
        st.subheader("Rephrased Text:")
        result = rephrase_text(input_text)
        st.write(result)

    else:
        st.info("Please enter text and select a task from the sidebar.")
