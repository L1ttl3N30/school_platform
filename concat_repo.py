import os

# Configuration
IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', 'venv', '.vscode', 'dist', 'build'}
INCLUDE_EXTENSIONS = {'.py', '.js', '.ts', '.tsx', '.html', '.css', '.json', '.md', '.sql'}
OUTPUT_FILE = "full_repository_context.txt"

def concat_repo(root_dir):
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        outfile.write("=== REPOSITORY STRUCTURE ===\n")
        
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            level = root.replace(root_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            outfile.write(indent + os.path.basename(root) + "/\n")
            sub_indent = ' ' * 4 * (level + 1)
            for f in files:
                if any(f.endswith(ext) for ext in INCLUDE_EXTENSIONS):
                    outfile.write(sub_indent + f + "\n")
        
        outfile.write("\n=== FILE CONTENTS ===\n")

        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for file in files:
                if any(file.endswith(ext) for ext in INCLUDE_EXTENSIONS):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, root_dir)
                    ext = file.split('.')[-1]
                    
                    # Using multi-line safe formatting
                    header = f"\n--- START FILE: {rel_path} ---\n```{ext}\n"
                    footer = f"\n```\n--- END FILE: {rel_path} ---\n"
                    
                    outfile.write(header)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                            outfile.write(infile.read())
                    except Exception as e:
                        outfile.write(f"// Error reading file: {str(e)}\n")
                    outfile.write(footer)
    
    print("Successfully created " + OUTPUT_FILE)

if __name__ == "__main__":
    concat_repo('.')