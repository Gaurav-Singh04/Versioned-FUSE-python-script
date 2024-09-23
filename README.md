# Versioned Virtual Filesystem

This Python script implements a simple versioned virtual filesystem that keeps track of file versions in a specified directory. When you save a file, an older version is stored in a versioned directory, allowing you to retrieve previous versions.

## Features

- Saves multiple versions of files.
- Configurable maximum number of versions to keep.
- Easy to set up and use.

## Requirements

- Python 3.x
- Necessary permissions to read/write in specified directories.

## Setup

1. **Clone or Download the Repository:**

   Clone the repository or download the script file `versioned_filesystem.py`.

   ```bash
   git clone <https://github.com/Gaurav-Singh04/Versioned-FUSE-python-script.git>

Usage
Run the Script:

Open a terminal and navigate to the directory where you saved the script. Execute the script using Python:

```bash
python3 versioned_filesystem.py
```

The script creates a versions directory inside the specified base_directory. Check this directory to see the versioned files.

Repeat for Different Files:

You can change the original_file variable in the script to version different files and run the script again.

```bash
vfs = VersionedFileSystem("/home/user/folder", max_versions=5)
original_file = "/home/user/folder/example.txt"
```
