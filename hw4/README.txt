++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
README file for Homework 4, Math 471, Fall 2026, J. Schroder
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

- The homework report is in the directory hw4/report and is called hw4.pdf. Also
contained in that directory is the LaTex file required for compilation, as well as the 
necessary figures (.png files) and text files containing data used in the construction of tables.

- The code directory contains three skeleton files provided to us, hw4_skeleton.py, 
hw4.sh, poisson.py and check_matvec.py. The only modified files are hw4_skeleton,
and hw4.sh. We authored strongScale.py. Instructions to run are below.

- To reproduce our results for part 1, you must first modify hw4_skeleton to use option 3 or 2 depending on 
which experiment you would like to replicate. The code that generates plots is at the bottom of the file, it must 
have the comments removed in order to plot. Once these changes have been made, simply run: python3 hw4_skeleton.py.
Runnning with these options will produce as many .png plots as threads of the reference curves along with the respective 
error convergence rate. 
To reproduce our results for part 2, modify hw4_skeleton.py to use option 1, comment out the plotting code (if uncommented), 
and uncomment the savetxt code. This will save the minimal time across 5 trials. Then run: python3 hw4_skeleton.py. 
This will generate the table data for the strong scaling studies. Then to generate the efficiency and timing plots,   
edit strongScale.py so that one block of plotting code is commented out and the other is uncommented. run: python3 strongScale.py,
then reverse which block is commented out and which is not and run it as before. This will generate one .png per run that 
has the efficiency or run time on the y axis and number of threads on the x axis.