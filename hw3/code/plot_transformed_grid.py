from numpy import *
from matplotlib import pyplot as plt

def plot_transformed_grid(T, n, fname='transformed_grid'):
    '''
    Plot a transformed uniform grid on [-1, 1] x [-1, 1] using n points
    
    input
    -----
    T(x,y) :  Transformation function to map uniform grid on [-1, 1] x [-1, 1]
    
    n : int, number of spacings

    fname : string, filename for image to be saved

    output
    ------
    transformed grid
    '''

    pts = linspace(-1,1,n)
    h = pts[1] - pts[0]
    plt.figure(541)
    plt.clf()
    for i in range(0, n-1):
        for j in range(0,n-1):
            new_pt1 = T(pts[j], pts[i])
            new_pt2 = T(pts[j+1], pts[i])
            plt.plot([new_pt1[0], new_pt2[0] ], [new_pt1[1], new_pt2[1]], "-k")
    
            new_pt1 = T(pts[j], pts[i])
            new_pt2 = T(pts[j], pts[i+1])
            plt.plot([new_pt1[0], new_pt2[0] ], [new_pt1[1], new_pt2[1]], "-k")
    
    i = n-1
    for j in range(0, n-1):
        new_pt1 = T(pts[j], pts[i])
        new_pt2 = T(pts[j+1], pts[i])
        plt.plot([new_pt1[0], new_pt2[0] ], [new_pt1[1], new_pt2[1]], "-k")

    j = n-1
    for i in range(0, n-1):
        new_pt1 = T(pts[j], pts[i])
        new_pt2 = T(pts[j], pts[i+1])
        plt.plot([new_pt1[0], new_pt2[0] ], [new_pt1[1], new_pt2[1]], "-k")

    plt.xlabel('$x$', fontsize='large')
    plt.ylabel('$y$', fontsize='large')
    plt.savefig(fname+".png", dpi=500, format='png', bbox_inches='tight', pad_inches=0.0,)




