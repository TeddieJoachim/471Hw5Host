++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
README file for Homework 3, Math 471, Fall 2026, J. Schroder
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

- The homework report is in the directory hw3/report and is called Hw3.pdf. Also
contained in that directory is the LaTex file required for compilation, as well as the 
necessary figures (.png files) and text files containing LaTex ready table data.

- The code directory contains three skeleton files provided to us, lglnodes.py, 
plot_transformed_grid.py, and part2skeleton.py. The only modified file is part2skeleton,
and gaussQuad and trapezoid.py were both authored by us. Instructions to run are below.

- To reproduce our results for question 1, run: python3 trapezoid.py and gaussQuad.py respectively.
Runnning either file will produce a .png plot of the reference curves along with the respective 
numerical integration method convergence rate. To reproduce our results for question 2, run: 
python3 part2skeleton.py. This will generate the LaTex table data for the estimations of functions 
U_1 and U_2 on omega_1 and R as .txt files, as well as the error plot on omega_2 from question 5.