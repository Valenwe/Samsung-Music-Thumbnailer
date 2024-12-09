# Samsung-Music-Thumbnailer

This tool is developped for Android users using the **Samsung Music** application. If there are music files with a different thumbnail inside the same folder, the application may choose to display the same thumbnail for both, despite them having a different one.
The program recursively processes music files in a specified directory, updating album names for files located in directories matching a defined regex pattern (facultative). This ensures that the correct thumbnails are displayed on the application.

## Features

- Recursively searches through directories.
- Updates album names (basically changes them for a generated Z starting word) based on folder names matching a specified regex pattern, or all of them.
- Requires the `ffmpeg` binary to function.
- This tool overwrites any album value already written on a music file! Be careful on which file you are using it.

## Requirements

- [ffmpeg](https://ffmpeg.org/download.html) - Ensure that ffmpeg is installed and available in your system's PATH.
- Python 3 (tested on **3.11.9**)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Valenwe/Samsung-Music-Thumbnailer.git
   cd Samsung-Music-Thumbnailer
   ```

2. Install Python module requirements:
    ```bash
    pip install .
    ```

3. Use the program from your root folder:
    ```bash
    # Will modify all album values inside that directory
    python -m samthumb.main "/path/to/my/music/folder"

    # Will modify music files contained in any folder having "Payday" inside their name
    python -m samthumb.main "/path/to/my/music/folder" -rf "Payday"

    # Will modify music files contained in any folder having "Payday" or "Hits" inside their name
    python -m samthumb.main "/path/to/my/music/folder" -rf "Payday|Hits"
    ```
