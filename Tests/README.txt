Test files for cleaning up video file names 
Scot W. Stevenson <scot.stevenson@gmail.com>
First version: 2025-04-12
This version: 2025-04-12

The empty files here are for testing the program to clean up video file names.
Do not run the program on these directly, but copy them to the make directory as
needed for testing. 

The command for copying should be something like 

       cp Tests/*.mkv .

Then run the program with 

        python3 renamevideos -v

and afterwards get rid of the output with 

        rm *.mkv

but only in the main directory.
