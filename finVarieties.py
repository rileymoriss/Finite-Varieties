import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

def plot_lattice(size, special_points, title):
    """
    Plots a lattice with specified points in a different color.

    Parameters:
    - size: Tuple (width, height) for the size of the lattice grid.
    - special_points: List of tuples [(x1, y1), (x2, y2), ...] specifying points to be highlighted.
    """
    # Generate lattice points
    x = np.arange(0, size[0], 1)
    y = np.arange(0, size[1], 1)
    X, Y = np.meshgrid(x, y)

    # Plot the lattice points
    plt.scatter(X, Y, color='blue')

    # Highlight special points
    if special_points:
        special_x, special_y = zip(*special_points)
        plt.scatter(special_x, special_y, color='red', label='Solutions', zorder=5)

    # Add grid and labels
    plt.grid(False)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(title)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=2)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.show()


def specify_polynomial():
    degree = int(input("Enter the degree of the polynomial: "))
    coefficients = []
    
    for i in range(degree, -1, -1):
        coeff = float(input(f"Enter the coefficient for x^{i}: "))
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

def main():
    print("Specify your polynomial:")
    polynomial = specify_polynomial()
    print(f"\nYour polynomial is: {polynomial}")
    print("Now we will specify the field:")
    p = int(input("Enter a prime: "))
    n = int(input("Enter a power: "))

    y = []
    for i in range(0, p**n - 1):
        print(i)
        print(y)
        y.append(int(polynomial.subs(sp.symbols('x'), i)) % (p**n))

    # Example usage
    lattice_size = (p**n , p**n )
    special_points = [[i] for i in range(0, p**n - 1)]
    print(special_points)
    for i in range(0, p**n - 1):
        special_points[i].append(y[i])
        special_points[i] = tuple(special_points[i])
        print(special_points)

    plot_lattice(lattice_size, special_points, "plot of "+str(polynomial) )

    
    


main()

input("...")
    
