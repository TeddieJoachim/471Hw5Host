++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
README file for Homework 2, Math 471, Fall 2026, J. Schroder
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

- The homework report is in the directory hw2/report and is called homework2.pdf. Also
contained in that directory is the LaTex file required for compilation, as well as the generated
plots of our network solutions for multidimensional Newton's Method, and the convergence data 
generated using savetxt().

- The code directory contains the skeleton code we were provided, that is drive_newton.py and plot_network.py.
it also contains code that we wrote, including multi_newton.py and drive_network.py. All of the coe in this 
directory was used at one point or another in producing our report.

- To reproduce our results for one dimensional Newton's method, simply run: "python drive_newton.py" this 
will generate the convergence data in a .txt file in the same directory that you run the file in. It will 
be three .txt files, convergence1, 2, and 3 corresponding to each function from question 1,
in a format that is ready to be imported into a LaTex table. The same is true of multi dimensional Newton's. 
Simply run: "python drive_newtwork.py" and you will see a new "multiNewtonIters.txt" file appear in your CWD.
To plot a network solution for multi dimensional Newton, look in drive_network.py. You will see a line containing
a call to plot_network() commented out. Uncomment this and the driver will generate a .png in your CWD.