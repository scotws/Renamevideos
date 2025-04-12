# Renamevideos
Clean up video file names with local AI support

This is a simple program to rename old video files that have weird names from
the bad old days when we were all afraid of white space in file names such as
"Berlin.2012-02-12.Kids.mkv". Earlier incarnations of this program used complex
regex to figure out how to rename it to a more standard format "Berlin
2012-02-12.mkv". The aim here was to see if we can use AI to do this with far
less effort, as part of a learning experience on integrating Python and LLM
workflows. 


## Assumptions

This code assumes that you have Ollama running on the local computer. It has
only been tested on a Linux machine. For more information on Ollama, see
https://github.com/ollama/ollama and other sites. The current default LLM is
Gemma 2 from the Ollama library at https://ollama.com/library . 

Note that on first use, Ollama takes a bit to move stuff to video RAM. Once that
is done, it keeps the LLM in VRAM for five minutes by default, so subsequent
calls are faster. 

Testing was done on a Nvidia GeForce RTX 4060 Ti with 16 GB VRAM.


## Code Structure

The prompt is hard-coded in the Python code with examples. If you want to modify
this script for your own use, be sure to change those as well. 

Note that we feed the name of the file to be cleaned up to the LLM one at a
time, not in a batch. Running the script in batches was slightly more efficient,
but resulted in file names getting skipped or mangled, persumably because of
token limits on a machine with only 16 GB of VRAM. If I can ever afford a
card with more RAM, I might test batch processing again. 


## Usage

For testing, you can copy the empty files from the Tests folder to the current
directory, see the README file there. 

Use the "-v" (verbose) flag to see what the machine is doing, and "-d" for a dry
run that shouldn't change things. 

```bash
python3 renamevideos.py -v -d
```

This software is provided as is, without any guarantees. Use at your own risk,
and make sure to backup your files for this and any other project.


## Further Development

Currently, no further development of this script is planned, as it was a
one-shot learning project for a limited number of old family video files. Feel
free to clone the repo for your own use. 



