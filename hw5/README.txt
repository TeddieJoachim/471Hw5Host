++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
README file for Homework 5, Math 471, Fall 2026, J. Schroder
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

- The homework report is in the directory hw5/report and is called hw5.pdf. Also
contained in that directory is the LaTex file required for compilation, as well as ...                    TODO
m
- The code directory contains                                                                             TODO

- This project was written primarily in C, and the emscripten compiler was used to create a 
webassembly module and corresponding javascript file that allows our C code to be run in the browser.
To reproduce our results, ...                                                                             TODO
If you want to recompile or edit the C code that implements RK4, you must install emscripten. 
Follow these instructions: https://emscripten.org/docs/getting_started/downloads.html. A common
message is that it could not be found when you run emcc ... . This just means you need to 'activate' it.
To activate emscripten in current directory (once it has been succesfully installed in the emsdk directory),
run: source ~/emsdk/emsdk_env.sh
