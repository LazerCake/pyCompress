A python application for smallifying uncompressed video files.
Should work with any video (tested with MP4 and WebM)

Run pyCompress.exe. A command prompt window will pop up as well - that's normal.

Select a video with the file explorer button (and then change filetype in bottom right if not looking for mp4s).
After that, select where the output video should go (defaults to output folder). 

Desired size can be changed, and if one is given the program will do a 2-pass compression to get to target output size.

When it's done (cmd printout will tell you), the compressed video will appear in the "output" folder. It's name will be whatever
you entered for the output name, or the original + "_Compressed" if none was given.
The output folder will be generated if not already there / on first operation.

The cmd window should only ever prompt you for action if you do something wrong like give it a filename that's already present.
You can just interact with the prompts it gives you like a normal cmd window, because it is one.

Sometimes temporary files may be left over from the 2-pass operation. You can safely delete these.

--------

Changelog

v2.1:
Added a fix for "Conversion failed" and "Frames left in buffer" issues
Added a check for the requested output size being too small. Displays this minimum in a printout if triggered.
Output name is no longer a compulsory field - if none is given it will simply give it the input name + "_Compressed"

v2:
Added size specification - program performs 2-pass encoding to reach a specified output size, if one is provided.
Added button to browse for folder which output will be placed in.
Added seperate headers for title, file selected, and output path.
Added compression preset selection, with slower presets yielding better encoding. Most impactful on single-pass encoding.