import os
from datetime import datetime

def gather_project_files(root_dir, output_file="program.txt", file_extensions=('.py', '.html', '.env', '.txt', '.js', '.css', '.ini')):
    """
    Recursively gather contents of specified file types from root_dir and its subdirectories
    into a single output file, excluding specified directories and files.
    
    Args:
        root_dir (str): Root directory to start searching from
        output_file (str): Name of the output file (default: program.txt)
        file_extensions (tuple): File extensions to include
    """
    # Directories to exclude
    EXCLUDE_DIRS = {'venv', '__pycache__', 'node_modules', '.git'}
    # Files to exclude
    EXCLUDE_FILES = {'combine.py', 'package-lock.json'}
    
    try:
        # Create or open the output file
        with open(output_file, 'w', encoding='utf-8') as outfile:
            # Write header with timestamp
            outfile.write(f"# Project Files Gathered on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            outfile.write("#" + "="*50 + "\n\n")
            
            # Priority files to handle first (if they exist)
            priority_files = {
                'requirements.txt': 'Python Dependencies',
                'package.json': 'Node.js Dependencies',
                '.env': 'Environment Variables',
            }
            
            # Handle priority files first
            for priority_file, description in priority_files.items():
                file_path = os.path.join(root_dir, priority_file)
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(f"# {description}\n")
                            outfile.write(f"# Filename: {priority_file}\n")
                            outfile.write(f"# Path: {priority_file}\n")
                            outfile.write("#" + "-"*50 + "\n\n")
                            outfile.write(infile.read())
                            outfile.write("\n\n")
                            outfile.write("="*50)
                            outfile.write("\n\n")
                    except Exception as e:
                        print(f"Error reading {priority_file}: {str(e)}")
            
            # Walk through directory tree
            for dirpath, dirnames, filenames in os.walk(root_dir):
                # Remove excluded directories
                dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
                
                # Sort directories for consistent output
                dirnames.sort()
                
                # Filter and sort files
                relevant_files = [
                    f for f in filenames 
                    if f.lower().endswith(file_extensions) 
                    and f not in EXCLUDE_FILES
                    and f not in priority_files  # Skip priority files as they're handled separately
                ]
                relevant_files.sort()  # Sort files for consistent output
                
                for filename in relevant_files:
                    file_path = os.path.join(dirpath, filename)
                    rel_path = os.path.relpath(file_path, root_dir)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            # Write file header with file type
                            file_type = os.path.splitext(filename)[1][1:].upper() or 'ENV'
                            outfile.write(f"# File Type: {file_type}\n")
                            outfile.write(f"# Filename: {filename}\n")
                            outfile.write(f"# Path: {rel_path}\n")
                            outfile.write("#" + "-"*50 + "\n\n")
                            
                            # Copy content
                            content = infile.read()
                            outfile.write(content)
                            
                            # Add separator between files
                            outfile.write("\n\n")
                            outfile.write("="*50)
                            outfile.write("\n\n")
                            
                    except Exception as e:
                        outfile.write(f"# Error reading file: {filename}\n")
                        outfile.write(f"# Path: {rel_path}\n")
                        outfile.write(f"# Error: {str(e)}\n")
                        outfile.write("#" + "-"*50 + "\n\n")
                        outfile.write("="*50)
                        outfile.write("\n\n")
        
        print(f"Successfully gathered project files into {output_file}")
        print(f"Note: Excluded directories: {', '.join(EXCLUDE_DIRS)}")
        print(f"Note: Excluded files: {', '.join(EXCLUDE_FILES)}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Get the current directory as root directory
    current_dir = os.getcwd()
    
    # You can modify these parameters as needed
    gather_project_files(
        root_dir=current_dir,
        output_file="program.txt",
        file_extensions=('.py', '.html', '.env', '.txt', '.js', '.css', '.ini')
    )