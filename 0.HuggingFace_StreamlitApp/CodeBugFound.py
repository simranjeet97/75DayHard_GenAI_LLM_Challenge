import streamlit as st
from transformers import pipeline
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import black
import subprocess

# Function for code formatting (black for Python, prettier for JavaScript)
def format_code(input_code, language):
    if language == "python":
        try:
            formatted_code = black.format_str(input_code, mode=black.FileMode())
            return formatted_code
        except black.InvalidInput as e:
            return f"Error formatting code: {e}"

    elif language == "javascript":
        try:
            # Assuming that prettier is installed globally
            result = subprocess.run(["prettier", "--stdin"], input=input_code, text=True, capture_output=True)
            formatted_code = result.stdout.strip()
            return formatted_code
        except Exception as e:
            return f"Error formatting code: {e}"

    else:
        return input_code

# Function for code analysis using code transformer
def analyze_code(input_code):
    try:
        # Set up the code-analysis pipeline with the roberta-base model
        code_analyzer = pipeline("text2text-generation", model="facebook/bart-large-cnn")

        # Generate analysis using a prompt
        prompt = f"Find 'gini' in this Code :\n\n{input_code}\n\nAnalysis:"
        analysis = code_analyzer(prompt, max_length=200, min_length=50, length_penalty=2.0)[0]['generated_text']

        return analysis
    except Exception as e:
        return f"Error during analysis: {e}"

# Streamlit app layout
st.title("Code Bugs Finder using Transformers")

# Input code area
input_code = st.text_area("Enter Code:")

# Language selection
language = st.selectbox("Select Code Language:", ["python", "java", "javascript", "r", "sql"])


# Function to highlight code syntax
def highlight_code(code, language):
    lexer = get_lexer_by_name(language, stripall=True)
    formatter = HtmlFormatter(style="borland")
    return highlight(code, lexer, formatter)

# Analyze button
if st.button("Find Bugs") and input_code:
    st.subheader("Code Analysis:")
    result = analyze_code(input_code)
    formatted_code = format_code(input_code, language)
    st.code(formatted_code, language=language)
    result_2 = highlight_code(result, language)
    st.markdown(result_2, unsafe_allow_html=True)
