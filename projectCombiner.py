import os
import sys

# --- Configuration ---
# The maximum number of characters allowed in a single output file.
MAX_CHARS = 20000
# If the current combined text is larger than this, the script will prefer to
# start a new file rather than adding more content, creating better breakpoints.
MIN_CHARS_FOR_BREAKPOINT = 15000
# --- End Configuration ---

def write_output_file(directory, file_num, content):
    """
    Writes the provided content to a numbered text file in the specified directory.
    
    Args:
        directory (str): The directory where the output file will be saved.
        file_num (int): The number for the output file (e.g., 1 for 1.txt).
        content (str): The string content to write to the file.

    Returns:
        int: The next file number to be used. Returns None on a fatal write error.
    """
    # Don't create empty files if the buffer is empty for some reason.
    if not content.strip():
        return file_num

    output_path = os.path.join(directory, f"{file_num}.txt")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully created {output_path} ({len(content)} characters)")
        return file_num + 1
    except IOError as e:
        print(f"FATAL: Could not write to output file {output_path}. Error: {e}")
        return None # Signal a critical failure

def combine_files_in_directory(root_dir):
    """
    Crawls a directory and its subdirectories, combining all file contents into
    sequentially numbered text files, each up to the MAX_CHARS limit.
    
    Args:
        root_dir (str): The path to the root directory to process.
    """
    if not os.path.isdir(root_dir):
        print(f"Error: The specified path '{root_dir}' is not a valid directory.")
        sys.exit(1)

    print(f"Starting to process files in '{root_dir}'...")
    
    current_buffer = ""
    output_file_num = 1
    
    # First, get a list of all files to process. This prevents the script
    # from accidentally reading its own output files if run multiple times.
    files_to_process = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # A simple check to see if the file looks like one of our output files.
            is_output_file = filename.endswith('.txt') and filename[:-4].isdigit()
            if not is_output_file:
                 files_to_process.append(os.path.join(dirpath, filename))

    # Sort the list for a consistent and predictable processing order.
    files_to_process.sort()

    for file_path in files_to_process:
        relative_path = os.path.relpath(file_path, root_dir)
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                file_content = f.read()
        except Exception as e:
            print(f"Warning: Could not read file '{relative_path}'. Skipping. Error: {e}")
            continue
            
        if not file_content.strip():
            # Don't process files that are empty or contain only whitespace.
            print(f"Info: Skipping empty file '{relative_path}'.")
            continue

        is_first_chunk = True
        
        # This loop continues as long as there's content from the current file to process.
        # It will only loop more than once if the source file needs to be split.
        while file_content:
            # Determine the correct header for the current chunk of the file.
            if is_first_chunk:
                header = f"--- File: {relative_path} ---\n\n"
            else:
                header = f"--- File: {relative_path} (continued) ---\n\n"
            
            # --- Intelligent Breakpoint Logic ---
            # If the buffer is already reasonably full AND we are about to add a completely new file,
            # it's better to write the current buffer out to create a clean break.
            if len(current_buffer) >= MIN_CHARS_FOR_BREAKPOINT and is_first_chunk:
                output_file_num = write_output_file(root_dir, output_file_num, current_buffer)
                if output_file_num is None: return # Stop on write error
                current_buffer = ""

            # If the buffer is so full we can't even fit the next header, we must write it.
            if len(current_buffer) + len(header) > MAX_CHARS:
                output_file_num = write_output_file(root_dir, output_file_num, current_buffer)
                if output_file_num is None: return
                current_buffer = ""

            # --- Add Content to Buffer ---
            space_for_data = MAX_CHARS - len(current_buffer) - len(header)
            
            # Take a chunk of the file's content that will fit in the remaining space.
            chunk = file_content[:space_for_data]
            
            current_buffer += header + chunk
            
            # Update the remaining file content and flags for the next iteration.
            file_content = file_content[space_for_data:]
            is_first_chunk = False

    # After iterating through all files, write any final content left in the buffer.
    if current_buffer:
        write_output_file(root_dir, output_file_num, current_buffer)

    print("\nProcessing complete.")

def main():
    """The main function to handle command-line arguments and start the process."""
    if len(sys.argv) != 2:
        print("Usage: python combine_files.py <path_to_directory>")
        print("Example: python combine_files.py ./my_project_folder")
        sys.exit(1)
    
    target_directory = sys.argv[1]
    combine_files_in_directory(target_directory)

if __name__ == "__main__":
    main()
