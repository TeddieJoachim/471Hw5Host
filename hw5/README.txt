++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
README file for Homework 5, Math 471, Fall 2026, J. Schroder
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

- The homework report is in the directory hw5/report and is called hw5.pdf. Also
contained in that directory is the LaTex file required for compilation, as well as 
the plot of the magnitudes of the simulation forces that the latex requires. 

- The src directory contains our C implementation of RK4 in the file boids.c. The web directory contains the 
javascript/webgl environment used for rendering, the plotting directory contains three CSV files and a python 
script for plotting. To reproduce our plot, simply run: python3 plotter.py from within this directory. The build
directory can be ignored by the user as it contains the generated webassembly and javascript that the emscripten 
compiler generates using our C code. These files should never be edited manually.

- This project was written primarily in C, and the emscripten compiler was used to create a 
webassembly module and corresponding javascript file that allows our C code to be run in the browser.
To reproduce our results, you do not need to rebuild the code necessarily. The easiest way to run this 
locally is by using the Makefile. Run: make serve to run on port 8000. Visit: http://localhost:8000/web/index-local.html. 
If you want to recompile or edit the C code that implements RK4, you must install emscripten. 
Follow these instructions: https://emscripten.org/docs/getting_started/downloads.html. A common
message is that it could not be found when you run emcc ... . This just means you need to 'activate' it.
To activate emscripten in current directory (once it has been succesfully installed in the emsdk directory),
run: source ~/emsdk/emsdk_env.sh
