import streamlit as st
from transformers import pipeline
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import black
import subprocess
import ast
import radon.metrics
import radon.complexity

# Function to highlight code syntax
def highlight_code(code, language):
    lexer = get_lexer_by_name(language, stripall=True)
    formatter = HtmlFormatter(style="borland")
    return highlight(code, lexer, formatter)

import ast
import radon.metrics

# Function for code analysis and optimization tips
def analyze_code(input_code):
    try:
        # Parse the code into an Abstract Syntax Tree (AST)
        parsed_code = ast.parse(input_code)

        # Calculate some basic metrics
        num_functions = sum(isinstance(node, ast.FunctionDef) for node in ast.walk(parsed_code))
        num_lines = len(input_code.splitlines())

        # Provide more detailed analysis and optimization tips
        analysis_summary = f"Code Analysis:\n"
        analysis_summary += f"Number of Functions: {num_functions}\n"
        analysis_summary += f"Number of Lines: {num_lines}\n\n"
        analysis_summary += "Optimization Tips:\n"

        # Add more detailed analysis and optimization tips based on your specific requirements
        # For example:
        if num_functions > 5:
            analysis_summary += "Consider refactoring complex functions into smaller ones for better maintainability.\n"

        # You can customize and extend this section based on your analysis logic
        # For example, checking for functions with high cyclomatic complexity:
        complexity_threshold = 10
        for node in ast.walk(parsed_code):
            if isinstance(node, ast.FunctionDef):
                function_code = ast.get_source_segment(input_code, node)
                # Check if the version of radon supports the multi parameter
                if 'multi' in radon.metrics.mi_visit.__code__.co_varnames:
                    complex = radon.metrics.mi_visit(function_code, multi=True)
                    if isinstance(complex, float):
                        complexity = complex  # Directly assign the float value
                    else:
                        complexity = complex[0]['mi']  # Access as expected
                else:
                    result = radon.metrics.mi_visit(function_code, multi=True)
                    if isinstance(result, float):
                        complexity = result  # Directly assign the float value
                    else:
                        complexity = result[0]['mi']  # Access as expected

                if complexity > complexity_threshold:
                    analysis_summary += f"Consider refactoring function '{node.name}' with high complexity ({complexity}) for better maintainability.\n"

        return analysis_summary
    except SyntaxError as e:
        return f"Syntax Error: {e}"

# Function for code formatting (black for Python, prettier for JavaScript)
def format_code(input_code, language):
    if language == "python":
        return black.format_str(input_code, mode=black.FileMode())
    elif language == "javascript":
        return subprocess.run(["prettier", "--stdin"], input=input_code, text=True, capture_output=True).stdout.strip()
    else:
        return input_code

# Streamlit app layout
st.title("Code Tools App")

# Sidebar with task selection
selected_task = st.sidebar.radio("Select Task:", ["Code Analysis"])

# Input code area
input_code = st.text_area("Enter Code:", height=200, key="input_code")

# Choose code language
language = st.selectbox("Select Code Language:", ["python", "javascript", "java", "csharp"])
formatted_code = format_code(input_code, language)
st.code(formatted_code, language=language)

# Section for Code Analysis
if selected_task == "Code Analysis":
    # Button to trigger code analysis
    if st.button("Analyze Code") and input_code:
        st.subheader("Code Analysis:")
        # Perform detailed code analysis and provide optimization tips
        result = analyze_code(input_code)
        st.write(result)
