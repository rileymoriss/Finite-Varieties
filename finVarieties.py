import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import math
import tkinter as tk
from tkinter import messagebox

def plot_lattice(index,  special_points, title, center, centerY):
    """
    Plots a lattice with specified points in a different color.

    Parameters:
    - size: Tuple (width, height) for the size of the lattice grid.
    - special_points: List of tuples [(x1, y1), (x2, y2), ...] specifying points to be highlighted.
    """
    pn = len(index)
    # Highlight special points
    if special_points:
        special_x, special_y = zip(*special_points)
        plt.scatter(special_x, special_y, color='red', label='Solutions', zorder=5)

    # Add grid and labels
    plt.grid(True)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(title)
    #plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=2)
    # Set the grid lines to appear at every integer
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')

    plt.xlim(min(index)-1, max(index)+1)
    plt.ylim( -1 , pn )
    if centerY:
        plt.ylim( - pn//2 - 1 , pn//2 + 1)
        
    # Control the number of axis labels using MaxNLocator
    #plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True, prune='both'))
    #plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True, prune='both')) 
    
    plt.show()
    
def mod_congruence(value, n, centerY):
    # Compute the standard modulo
    mod_value = value % n
    
    # Adjust to fit within the range -n to n
    if (mod_value > n // 2) and centerY:
        return mod_value - n
    return mod_value

class Switch(tk.Checkbutton):
    def __init__(self, master=None, **kwargs):
        self.var = tk.BooleanVar()  # Initialize the variable
        super().__init__(master, variable=self.var, **kwargs)
        self.configure(command=self.toggle, indicatoron=False, width=6)
        self.bind('<Button-1>', self.toggle)
        self.toggle()  # Initialize the appearance based on the initial state

    def toggle(self, event=None):  # Accept optional event argument
        if self.var.get():
            self.configure(bg='lightgreen', relief='sunken')
        else:
            self.configure(bg='lightcoral', relief='raised')

    def set_on(self, on):
        self.var.set(on)
        self.toggle()

    def get(self):
        return self.var.get()

##################
def generate_command():
    #Clear previous plot
    plt.clf()
    # Define the symbol used in the polynomial
    x = sp.symbols('x')

    # LaTeX string (as an example)
    latex_poly = EntryPoly.get()
    center = switchX.get()
    centerY = switchY.get()

    # Convert LaTeX to a sympy expression
    poly_expr = sp.sympify(latex_poly.replace('^', '**'))
    # Convert sympy expression to a Python function
    poly_func = sp.lambdify(x, poly_expr, 'numpy')  

    p = int(entryPrime.get())
    n = int(entryPower.get())

    if center:
        index = range(math.floor(-0.5*(p**n - 1)), math.ceil(0.5*(p**n - 1))+1)
    else:
        index = range(0, p**n)
    
    #Apply the function
    y = []
    for i in index:
        y.append(mod_congruence(int(poly_func(i)), p**n, centerY) )
    
    # Example usage
    lattice_size = p**n
    special_points = [[i] for i in index]
    for i in range(0, p**n):
        special_points[i].append(y[i])
        special_points[i] = tuple(special_points[i])

    plot_lattice(index, special_points, "plot of $"+latex_poly+"$ mod $"+str(p)+"^"+str(n)+"$" , center, centerY)

def generate_elliptic_command():
#Clear previous plot
    plt.clf()
    # Define the symbol used in the polynomial
    x = sp.symbols('x')

    # LaTeX string (as an example)
    latex_poly = EntryPoly.get()
    center = switchX.get()
    centerY = switchY.get()

    # Convert LaTeX to a sympy expression
    poly_expr = sp.sympify(latex_poly.replace('^', '**'))
    # Convert sympy expression to a Python function
    poly_func = sp.lambdify(x, poly_expr, 'numpy')  

    p = int(entryPrime.get())
    n = int(entryPower.get())

    if center:
        index = range(math.floor(-0.5*(p**n - 1)), math.ceil(0.5*(p**n - 1))+1)
    else:
        index = range(0, p**n)
    
    #Apply the function
    y = []
    for i in index:
        y.append(mod_congruence(int(poly_func(i)), p**n, centerY) )
    
    # Example usage
    lattice_size = p**n
    special_points = [[i] for i in index]
    for i in range(0, p**n):
        special_points[i].append(y[i])
        special_points[i] = tuple(special_points[i])
    
    temp = []
    for i in special_points:
        if ((i[0]**2 % p**n)- (i[1] % p**n ))% p**n== 0:
            temp.append(i)


    plot_lattice(index, temp, "plot of $"+latex_poly+"$ mod $"+str(p)+"^"+str(n)+"$", center, centerY )
##################

# Create the main application window
root = tk.Tk()
root.title("Finite Field Varieties")
root.geometry("500x500")

#Polynomial Entry
label = tk.Label(root, text="Enter an integral polynomial in the variable x\n Use LaTeX formating for powers and * for multiplication e.g. 3*x^2")
label.pack(pady=10)
EntryPoly = tk.Entry(root)
EntryPoly.pack(pady=10)

#Prime Entry
label = tk.Label(root, text="Prime")
label.pack(pady=10)
entryPrime = tk.Entry(root)
entryPrime.pack(pady=10)

#Power Entry
label = tk.Label(root, text="Power")
label.pack(pady=10)
entryPower = tk.Entry(root)
entryPower.pack(pady=10)

#Center?
# Create a variable to store the state of the switch
var = tk.BooleanVar()
# Create a switch widget
switchX = Switch(root, text="Center X", bg='lightcoral')
switchX.pack(pady=20)
switchY = Switch(root, text="Center Y", bg='lightcoral')
switchY.pack(pady=20)


#Generate graph button
generate = tk.Button(root, text="Generate", command=generate_command)
generate.pack(pady=10)
generateE = tk.Button(root, text="Generate Elliptic Curve", command=generate_elliptic_command)
generateE.pack(pady=10)

# Run the application's main loop
root.mainloop()

