import streamlit as st
import os
import multiprocessing
import tkinter as tk
from tkinter import filedialog
from gitingest_local import main
import tempfile
from pathlib import Path

def select_folder_process(queue):
    """Run tkinter folder picker in a separate process and put the result in the queue."""
    try:
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(
            initialdir=os.path.expanduser("~"),
            title="Select Repository Folder"
        )
        root.destroy()
        queue.put(folder_path)
    except Exception as e:
        queue.put(None)  # Return None if an error occurs

def get_folder_path():
    """Get folder path using multiprocessing to avoid conflicts with Streamlit."""
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=select_folder_process, args=(queue,))
    p.start()
    p.join()
    folder_path = queue.get()
    return folder_path

st.set_page_config(
    page_title="Git Ingest",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        margin-top: 10px;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .main {
        padding: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("📚 Git Ingest")
st.markdown("""
    Convert your private/local repository into a context-friendly format for LLM context.
    This tool will generate a comprehensive markdown summary of your repository, including
    directory structure and file contents.
""")

# Create two columns for the main content
col1, col2 = st.columns([2, 1])

with col1:
    # Repository path selection
    st.subheader("Select Repository")
    
    # Add both folder picker and manual input
    col1a, col1b = st.columns([1, 1])
    
    with col1a:
        if st.button("Browse for Repository Folder"):
            folder_path = get_folder_path()
            if folder_path:
                st.session_state.repo_path = folder_path
                st.success(f"Selected repository: `{folder_path}`")
            else:
                st.warning("No folder selected or an error occurred.")
    
    with col1b:
        # Manual path input as fallback
        manual_path = st.text_input(
            "Or enter path manually",
            value=st.session_state.get('repo_path', ''),
            help="Enter the full path to your repository folder (e.g., /Users/username/projects/my-repo)"
        )
        if manual_path:
            st.session_state.repo_path = manual_path
            if os.path.isdir(manual_path):
                st.success(f"Valid repository path: `{manual_path}`")
            else:
                st.error(f"Invalid path: `{manual_path}`")

    # File type selection
    st.subheader("File Types to Include")
    file_types = {
        "Python (.py)": ".py",
        "JavaScript (.js)": ".js",
        "Java (.java)": ".java",
        "Markdown (.md)": ".md",
        "Text (.txt)": ".txt",
        "C/C++ (.c, .cpp, .h)": [".c", ".cpp", ".h"],
        "HTML (.html)": ".html",
        "CSS (.css)": ".css",
        "Swift (.swift)": ".swift"
    }
    
    selected_types = []
    for file_type, extension in file_types.items():
        if st.checkbox(file_type, value=True):
            if isinstance(extension, list):
                selected_types.extend(extension)
            else:
                selected_types.append(extension)

with col2:
    # Features list
    st.subheader("Features")
    features = [
        "📝 Extracts README.md content",
        "📁 Generates directory structure",
        "📄 Includes file contents",
        "🎨 Syntax highlighting",
        "📋 Automatic clipboard copy"
    ]
    for feature in features:
        st.markdown(f"- {feature}")

    # Excluded directories info
    st.subheader("Excluded Directories")
    excluded = [
        ".git",
        "node_modules",
        "__pycache__",
        ".venv",
        "build",
        "dist"
    ]
    for directory in excluded:
        st.markdown(f"- `{directory}`")

# Generate button
if st.button("Generate Repository Summary", type="primary"):
    repo_path = st.session_state.get('repo_path')
    if not repo_path:
        st.error("Please select a repository folder or enter a path")
    elif not os.path.isdir(repo_path):
        st.error("Please enter a valid directory path")
    else:
        with st.spinner("Generating repository summary..."):
            try:
                # Create a temporary directory for the output
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Change to the temporary directory
                    original_dir = os.getcwd()
                    os.chdir(temp_dir)
                    
                    # Run the main function
                    main(repo_path)
                    
                    # Read the generated markdown
                    with open('repo_summary.md', 'r', encoding='utf-8') as f:
                        markdown_content = f.read()
                    
                    # Change back to original directory
                    os.chdir(original_dir)
                    
                    # Display the markdown content in separate collapsible sections
                    with st.expander("Repository Structure", expanded=False):
                        # Extract and display repository structure section
                        structure_start = markdown_content.find("## Repository Structure")
                        readme_start = markdown_content.find("## README.md")
                        structure_content = markdown_content[structure_start:readme_start].strip()
                        st.markdown(structure_content)
                    
                    with st.expander("README.md", expanded=False):
                        # Extract and display README section
                        readme_end = markdown_content.find("## File Contents")
                        readme_content = markdown_content[readme_start:readme_end].strip()
                        st.markdown(readme_content)
                    
                    with st.expander("File Contents", expanded=False):
                        # Extract and display file contents section as a single code block
                        file_contents_start = markdown_content.find("## File Contents")
                        file_contents = markdown_content[file_contents_start:].strip()
                        st.code(file_contents, language="markdown")
                        
                        # Add download button at the bottom
                        st.download_button(
                            label="Download Markdown File",
                            data=markdown_content,
                            file_name="repo_summary.md",
                            mime="text/markdown"
                        )
                    
                    st.success("Summary generated successfully! The content has been copied to your clipboard.")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Made with ❤️ for LLM context generation</p>
        <p>Licensed under Apache License 2.0</p>
    </div>
""", unsafe_allow_html=True)