# Local_Git_Ingest
Convert your private / local repo into a context-friendly format for LLM context
<img width="1815" alt="image" src="https://github.com/user-attachments/assets/82c5bfbd-17f4-48ef-a376-871eaa433019" />
## Features

- 📝 Extracts a summary from the repository's `README.md` if available
- 📁 Generates a directory structure of the repository, excluding common irrelevant directories
- 📄 Includes the contents of text-based files in Markdown code blocks
- 🎨 Automatic syntax highlighting for supported file types
- 📋 Automatically copies the generated markdown to your clipboard
- 🖥️ Modern, user-friendly Streamlit web interface with folder picker
- 📥 Download option for the generated markdown file

## Requirements

- Python 3.6 or higher
- Streamlit (for web interface)
- Dependencies listed in `requirements.txt`

## Usage

You can use this tool in two ways:

### 1. Command Line Interface

1. Save the script as `gitingest_local.py`
2. Run the script from the command line with the path to your local repository:

```bash
python gitingest_local.py /path/to/your/repo
```

### 2. Web Interface (Streamlit)

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Launch the Streamlit interface:
```bash
streamlit run streamlit_app.py
```

3. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)
4. Select your repository folder using the folder picker or enter the path manually
5. Choose which file types to include in the summary
6. Click "Generate Repository Summary"

## Output

The script generates a `repo_summary.md` file containing:

1. **Repository Structure**: A hierarchical view of the repository's files and folders
2. **README.md**: Content from the repository's README.md (if available)
3. **File Contents**: The contents of all selected text files, formatted in code blocks with appropriate language syntax highlighting

The generated content is displayed in collapsible sections in the web interface, and you can download the complete markdown file using the download button.

## Supported File Types

The script currently supports the following file types:
- Python (.py)
- JavaScript (.js)
- Java (.java)
- Markdown (.md)
- Text (.txt)
- C/C++ (.c, .cpp, .h)
- HTML (.html)
- CSS (.css)
- Swift (.swift)

You can select which file types to include in the summary through the web interface.

## Excluded Directories

The following directories are automatically excluded from the output:
- .git
- node_modules
- __pycache__
- .venv
- build
- dist

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.
