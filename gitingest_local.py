import os
import argparse
import subprocess

# Configuration
EXCLUDED_DIRS = ['.git', 'node_modules', '__pycache__', '.venv', 'build', 'dist']
INCLUDED_EXTENSIONS = ['.py', '.js', '.md', '.txt', '.java', '.c', '.cpp', '.h', '.html', '.css', '.swift']
EXTENSION_TO_LANGUAGE = {
    '.py': 'python',
    '.js': 'javascript',
    '.java': 'java',
    '.md': 'markdown',
    '.txt': 'text',
    '.c': 'c',
    '.cpp': 'cpp',
    '.h': 'c',
    '.html': 'html',
    '.css': 'css',
    '.swift': 'swift'
}

def generate_dir_structure(path, depth=0):
    """Generate a nested Markdown list of the directory structure with branch-like formatting."""
    lines = []
    indent = '  ' * depth
    for item in sorted(os.listdir(path)):  # Sort for consistency
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            if item not in EXCLUDED_DIRS:
                # Add branch-like formatting for directories
                if depth == 0:
                    lines.append(f"{indent}{item}")
                else:
                    prefix = "├── " if depth > 0 else "└── "
                    lines.append(f"{indent}{prefix}{item}")
                lines.extend(generate_dir_structure(item_path, depth + 1))
        else:
            # Add branch-like formatting for files
            prefix = "├── " if depth > 0 else "└── "
            lines.append(f"{indent}{prefix}{item}")
    return lines

def get_file_contents(repo_path):
    """Collect contents of text files and format them as Markdown sections."""
    contents = []
    for root, dirs, files in os.walk(repo_path):
        # Modify dirs in-place to exclude unwanted directories
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for file in sorted(files):  # Sort for consistency
            if any(file.endswith(ext) for ext in INCLUDED_EXTENSIONS):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, repo_path)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    ext = os.path.splitext(file)[1]
                    language = EXTENSION_TO_LANGUAGE.get(ext, 'text')
                    section = f"### File: {rel_path}\n\n```{language}\n{content}\n```"
                    contents.append(section)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return "\n\n".join(contents)

def main(repo_path):
    """Generate a Markdown summary of the local repository."""
    if not os.path.isdir(repo_path):
        print(f"Error: {repo_path} is not a valid directory.")
        return

    # Get summary from README.md or use a default
    print("Extracting repository summary...")
    readme_path = os.path.join(repo_path, 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
    else:
        readme_content = f"This is a local repository at {repo_path}."

    # Generate directory structure
    print("Generating directory structure...")
    dir_structure = generate_dir_structure(repo_path)
    dir_structure_md = "\n".join(dir_structure)

    # Collect file contents
    print("Reading file contents...")
    file_contents = get_file_contents(repo_path)
    
    # Filter out README.md content if present
    file_contents = "\n\n".join([section for section in file_contents.split("\n\n") 
                                if "README.md" not in section])

    # Combine into a single Markdown document with three distinct sections
    markdown = (
        f"# Repository Summary\n\n"
        f"## Repository Structure\n\n"
        f"```\n{dir_structure_md}\n```\n\n"
        f"## README.md\n\n{readme_content}\n\n"
        f"## File Contents\n\n```markdown\n{file_contents}\n```"
    )

    # Write to output file
    output_file = 'repo_summary.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown)

    # Copy to clipboard
    try:
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(markdown.encode('utf-8'))
        print(f"Markdown summary generated: {output_file}")
        print("Markdown summary copied to clipboard")
    except Exception as e:
        print(f"Markdown summary generated: {output_file}")
        print(f"Warning: Could not copy to clipboard: {e}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Generate a Markdown summary of a local repository for LLM context.')
    parser.add_argument('repo_path', help='Path to the local repository')
    args = parser.parse_args()

    main(args.repo_path)