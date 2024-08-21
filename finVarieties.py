import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import math
import tkinter as tk
from tkinter import messagebox

def plot_lattice(size, special_points, title, center):
    """
    Plots a lattice with specified points in a different color.

    Parameters:
    - size: Tuple (width, height) for the size of the lattice grid.
    - special_points: List of tuples [(x1, y1), (x2, y2), ...] specifying points to be highlighted.
    """
    
    # Highlight special points
    if special_points:
        special_x, special_y = zip(*special_points)
        plt.scatter(special_x, special_y, color='red', label='Solutions', zorder=5)

    # Add grid and labels
    plt.grid(True)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(title)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=2)
    plt.gca().set_aspect('equal', adjustable='box')
    # Set the grid lines to appear at every integer
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.grid(True)
    # Control the number of axis labels using MaxNLocator
    #plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True, prune='both'))
    #plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True, prune='both')) 
    
    plt.show()


def specify_polynomial():
    degree = int(input("Enter the degree of the polynomial: "))
    coefficients = []
    
    for i in range(degree, -1, -1):
        coeff = int(input(f"Enter the coefficient for x^{i}: "))
        coefficients.append(coeff)
    
    polynomial = sum(c * sp.symbols('x')**i for i, c in enumerate(reversed(coefficients)))
    return polynomial

def test_polynomial(polynomial):
    while True:
        try:
            x_value = int(input("Enter a value of x to test (or type 'exit' to quit): "))
        except ValueError:
            print("Exiting...")
            break

        result = int(polynomial.subs(sp.symbols('x'), x_value))
        print(f"The value of the polynomial at x = {x_value} is: {result}")
    

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


#main()
##################
def generate_command():
    #Clear previous plot
    plt.clf()
    # Define the symbol used in the polynomial
    x = sp.symbols('x')

    # LaTeX string (as an example)
    latex_poly = EntryPoly.get()
    center = switch.get()
    print(center)

    # Convert LaTeX to a sympy expression
    poly_expr = sp.sympify(latex_poly.replace('^', '**'))

    # Print the Python expression
    print(poly_expr)

    # Convert sympy expression to a Python function
    poly_func = sp.lambdify(x, poly_expr, 'numpy')  

    p = int(entryPrime.get())
    n = int(entryPower.get())
    print(p)
    print(n)

    if center:
        index = range(math.floor(-0.5*(p**n - 1)), math.ceil(0.5*(p**n - 1))+1)
    else:
        index = range(0, p**n)
    
    y = []
    for i in index:
        y.append(int( poly_func(i)) % (p**n))
    
    # Example usage
    lattice_size = p**n
    special_points = [[i] for i in index]
    print(special_points)
    for i in range(0, p**n):
        print(i)
        special_points[i].append(y[i])
        special_points[i] = tuple(special_points[i])

    print(special_points)

    plot_lattice(lattice_size, special_points, "plot of $"+latex_poly+"$ mod $"+str(p)+"^"+str(n)+"$", center )



##################

# Create the main application window
root = tk.Tk()
root.title("Basic GUI Application")

#Polynomial Entry
label = tk.Label(root, text="Enter an integral polynomial in the variable x")
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
switch = Switch(root, text="Center", bg='lightcoral')
switch.pack(pady=20)


#Generate graph button
generate = tk.Button(root, text="Generate", command=generate_command)
generate.pack(pady=10)

# Run the application's main loop
root.mainloop()

