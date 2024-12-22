import os
import random
import re
import subprocess
from pathlib import Path

import click
from tqdm import tqdm

# Define the extensions of audio files that we want to process
AUDIO_EXTENSIONS = ['.mp3', '.flac', '.m4a', '.wav', '.ogg']

CONSONANTS = "bcdfghjklmnpqrstvwxzy"
VOWELS = "aeiou"


def generate_random_word() -> str:
    nb_syllabe = random.randint(2, 8)
    word = "Z" + random.choice(VOWELS)
    for _ in range(nb_syllabe):
        conson = random.choice(CONSONANTS)
        vow = random.choice(VOWELS)
        word += conson + vow
        if random.random() >= 0.8:
            word += random.choice(CONSONANTS)
    return word


def remove_album_metadata(directory: str, folder_regex: str) -> None:
    """
    Function to recursively process music files and remove album name
    """
    # Compile the regular expression pattern
    any_folder = False
    if folder_regex is not None:
        folder_pattern = re.compile(folder_regex)
    else:
        any_folder = True

    # Gather all the files to be processed for progress tracking
    files_to_process: dict[str, list[Path]] = {}
    random_album_names: dict[str, set[str]] = {}
    for root, _, files in os.walk(directory):
        if any_folder or folder_pattern.search(os.path.basename(root)):

            selected_words: set[str] = set()
            while len(selected_words) < len(files):
                selected_words.add(generate_random_word())
            random_album_names[root] = selected_words

            files_to_process[root] = []
            for file in files:
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext in AUDIO_EXTENSIONS:
                    files_to_process[root].append(
                        Path(os.path.join(root, file)))

    # Create a tqdm progress bar
    with tqdm(total=sum((len(files) for files in files_to_process.values())),
              desc="Processing files",
              colour="#ff5733") as pbar:
        for folder, music_files in files_to_process.items():
            word_selection = random_album_names[folder]

            for filepath in music_files:
                temp_file = filepath.parent / f"temp_{filepath.name}"

                try:
                    word = word_selection.pop()
                    # Use ffmpeg to copy audio streams but remove the album metadata
                    subprocess.run([
                        'ffmpeg', '-i',
                        filepath.as_posix(), '-map', '0', '-c', 'copy',
                        '-metadata', f'album="{word}"', temp_file, '-y'
                    ],
                                   check=True,
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)

                    # Replace the original file with the processed file
                    os.replace(temp_file, filepath.as_posix())
                    random_album_names[folder] = word_selection

                except subprocess.CalledProcessError as e:
                    print(f"Error processing {filepath.as_posix()}: {e}")

                # Update the progress bar
                pbar.update(1)
    print("Process is now finished :)")


@click.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("-rf",
              "--regex-folder",
              "folder_regex",
              type=str,
              help="Regex pattern to match folders that should be processed.")
def main(directory: str, folder_regex: str) -> None:
    """
    Recursively processes music files in DIRECTORY, changing album names for files in
    directories matching the FOLDER_REGEX pattern, to display their correct thumbnail on Samsung Music.

    Requires ffmpeg binary to work.

    DIRECTORY: The top-level directory to start processing from.
    FOLDER_REGEX: The regex pattern to match folders that should be processed.
    """
    remove_album_metadata(directory, folder_regex)


# Entry point for the script
if __name__ == "__main__":
    main()
