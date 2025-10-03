Directory Content Combiner
A simple yet powerful Python script to recursively scan a directory, read the content of all files, and combine them into a series of numbered text files (1.txt, 2.txt, etc.).

This is particularly useful for consolidating large codebases or collections of text documents into a format that can be easily fed into Large Language Models (LLMs) or used for archival purposes.

Features
Recursive Traversal: Scans the entire directory tree from the specified root.

Contextual Headers: Prepends the relative path and filename to the content of each file, giving LLMs the full context of your project's structure.

Intelligent File Splitting: Combines content into output files of up to 20,000 characters.

Smart Breakpoints: Tries to avoid splitting a file across two output files if the current output file is already reasonably full (over 15,000 characters), leading to cleaner separation of contexts.

Continuation Headers: If a large file must be split, it's clearly marked with a (continued) notice in the header.

Safe Operation: The script is designed to ignore its own output files (1.txt, 2.txt, etc.), so you can run it in the same directory multiple times without issues.

Error Handling: Skips files it cannot read and prints a warning, rather than crashing.

Usage
The script is run from the command line and takes a single argument: the path to the directory you want to process.

Prerequisites
Python 3.x

Running the Script
Clone this repository or download the combine_files.py script.

Open your terminal or command prompt.

Execute the script using the following format:

python combine_files.py <path_to_your_directory>

Examples
To process a folder named my_project located in the same directory as the script:

python combine_files.py my_project

To process a folder using an absolute path:

python combine_files.py /Users/yourname/Documents/source_code

The output files (1.txt, 2.txt, etc.) will be saved directly into the <path_to_your_directory> you specified.

Configuration
You can adjust the character limits by modifying the following constants at the top of the combine_files.py script:

MAX_CHARS: The absolute maximum number of characters for an output file.

MIN_CHARS_FOR_BREAKPOINT: The threshold at which the script will prefer to start a new output file rather than adding a new source file to the current one.