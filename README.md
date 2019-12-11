# diff-eq-solver

This program uses various finite difference methods to solve ordinary differential equations and partial differential 
equations. For partial differential equations, we focus on special types of partial differential equations, such as the heat equation, wave equation, and Laplace's equation. The solution values are organized in a table and written to an excel file and the solution is visually represented on a plot generated with Matplotlib. <br>

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
f = lambda x: 2 * x - x ** 2  # Initial Condition
heatEquation = HeatEquation(1, 0, p, q, f)
heatEquation.plot_solution(2, 50, 1)
```
![Figure_1](https://user-images.githubusercontent.com/46363213/70382868-26dabb80-1918-11ea-91ef-ea636704b5ac.png)

