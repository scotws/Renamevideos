#!/usr/bin/env python3

# Rename Videos
# Clean up video file names with local AI support
# Scot W. Stevenson <scot.stevenson@gmail.com> 
# First version: 2016-03-23
# This version: 2025-04-12

# Assumes ollama is running on target machine, with gemma2

import argparse
import json
import os
import re
import requests
import time

# Configuration

MODEL = "gemma2"  # Change this to any installed model
URL = "http://localhost:11434/api/generate"
VIDEO_EXTENSIONS = {".mkv", ".mp4", ".avi", ".mov"}  # Add more as needed
DIRECTORY = "."  # Change to the target directory


def get_video_files(directory):
    """Scan the directory and return a list of video file names."""

    return [f for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in VIDEO_EXTENSIONS]


def generate_prompt(file_list):
    """Generate a prompt for Ollama based on the file list."""

    prompt = """Given a list of file names of video files in a format such as
    'Zepernick_2016-03-15_other_go_game.mkv' or 'Berlin.Kids.lama.spitting.2013.03.14.mp4',
    please convert them into a standardized format '<LOCATION> - <DATE>.<EXTENSION>'
    such as 'Zepernick 2016-03-15.mkv' and 'Berlin 2013-03-14.mp4'. If the file
    is already in this format, ignore it. Please return the files that need to be
    changed with their old and new names in JSON format as 'old' and 'new'. Do not
    print any commentary or explanations.
    
    Here are the file names:
    """
    prompt += "\n".join(file_list)
    return prompt


def send_to_ollama(prompt, max_retries=3, delay=2):
    """Send the prompt to Ollama and return the parsed JSON response, with retries."""

    data = {"model": MODEL, "prompt": prompt, "stream": False}

    for attempt in range(max_retries):
        try:
            response = requests.post(URL, json=data)
            response.raise_for_status()

            raw = response.json()["response"]

            # Extract JSON from triple-backtick block if needed. This otherwise
            # confuses the model sometimes
            json_match = re.search(r"```json\s*(\[.*?\])\s*```", raw, re.DOTALL)

            if json_match:
                cleaned = json_match.group(1)
            else:
                cleaned = raw.strip()

            parsed = json.loads(cleaned)
            return parsed

        except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Failed after multiple attempts. Exiting.")
                return None


def rename_files(rename_list, dry_run=False): 
    """Rename files based on the rename_list; if dry_run is True, 
    only print changes."""

    for item in rename_list:
        old_name = item["old"]
        new_name = item["new"]
        
        if old_name == new_name:
            continue  # Skip files that don't need renaming

        # If there is a colon in the name, we need to replace it
        if ':' in new_name:
            new_name = new_name.replace(':', '')

        old_path = os.path.join(DIRECTORY, old_name)
        new_path = os.path.join(DIRECTORY, new_name)

        if dry_run:
            print(f"[DRY RUN] {old_name} -> {new_name}")
        else:
            try:
                os.rename(old_path, new_path)
                print(f"Renamed: {old_name} -> {new_name}")
            except OSError as e:
                print(f"Error renaming {old_name}: {e}")


if __name__ == "__main__":

    # We process files one at a time to avoid context length limitations
    # in the language model (LLM). When many filenames are sent at once,
    # the LLM may skip or truncate some due to confusion or token limits.
    # Processing them individually ensures each file is fully considered,
    # at the cost of some efficiency. Since the model remains in VRAM
    # after the first call, the performance impact is minor for small batches.

    parser = argparse.ArgumentParser(description="Clean up video file names.")
    parser.add_argument("-d", "--dry-run", action="store_true", help="Show renaming changes without modifying files.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print out data for testing.")
    args = parser.parse_args()

    video_files = get_video_files(DIRECTORY)

    # Testing: Print list of files found
    if args.verbose:
        print("Found video files:\n", video_files)
    
    if not video_files:
        print("No video files found.")
    else:
        all_results = []

        for i, filename in enumerate(video_files, start=1):

            if args.verbose:
                print(f"[{i}/{len(video_files)}] Processing: {filename}")
            prompt = generate_prompt([filename])
            result = send_to_ollama(prompt)

            if result:
                all_results.extend(result)

        if all_results:
            rename_files(all_results, dry_run=args.dry_run)
