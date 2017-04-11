# Mosaicer
A set of programs for generating mosaiced images, and demosaicing them back to full RGB images.

Requires PIL (Python Imaging Library). Requires Python 3 (for print statements).

Run -h on any of the scripts to get usage information. Input and output of almost all image types are supported (though lossless formats are the only ones that make sense in this context). Here's an example of how to use the stdout/stdin redirect to skip an intermediary mosaiced image save and load:

./mosaicer.py -i in.png -o - | ./const_hue_norm.py -i - -o out.png

Infact you can input a normal image into any of the interpolation scripts to get the same result as the corresponding mosaiced image; mosaicing first is not neccesary. Running a mosaiced image through will merely prove that I didn't cheat.
