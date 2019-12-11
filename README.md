# diff-eq-solver

This program uses various finite difference methods to solve ordinary differential equations and partial differential 
equations. For partial differential equations, we focus on special types of partial differential equations, such as the 
heat equation, wave equation, and Laplace's equation. The solution values are organized in a table and written to an 
excel file and the solution is visually represented on a plot generated with Matplotlib. <br>

## Progress
- [x] First Order ODE Class
- [x] Second Order ODE Class
- [ ] n-th Order ODE Class
- [x] Heat Equation Class
- [ ] Wave Equation Class
- [ ] Laplace's Equation Class

## Getting Started

Sample code for running the program can be found at src/main/ui/Main.py. Try changing the parameters of the constructor 
calls and see how it changes the excel spreadsheets in src/main/ui/excel_data. 

## Example
```python
p = lambda t: 0               # Left Boundary
q = lambda t: 0               # Right Boundary
f = lambda x: 2 * x - x ** 2  # Initial Values
heatEquation = HeatEquation(1, 0, p, q, f)
L = 2
n = 25
t = 1
m = heatEquation.get_stable_m(L, n, t)    # Larger values increases accuracy
try:
    heatEquation.plot_solution(L, n, t, m)
    heatEquation.write_solution(L, n, t, m)
except BoundaryTypeException:
    print("Invalid boundary type in heat equation")
```

![heat_figure](https://user-images.githubusercontent.com/46363213/70660505-378c7980-1c17-11ea-9d0c-3286d399c247.png)

![heat_data](https://user-images.githubusercontent.com/46363213/70660477-217eb900-1c17-11ea-8e75-1e420af3dca0.PNG)

