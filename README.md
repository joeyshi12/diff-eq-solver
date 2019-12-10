# diff-eq-solver

This program uses various finite difference methods to solve ordinary differential equations and partial differential 
equations. For partial differential equations, we focus on special types of partial differential equations, such as the heat equation, wave equation, and Laplace's equation. The solution values are written to an excel file and the solution is visually represented on a plot generated with Matplotlib. <br>
[Work in progress]

## Getting Started

The file for running this program can be found at src/main/ui/Main.py. 

## Example
```python
p = lambda t: 0
q = lambda t: 0
f = lambda x: 2 * x - x ** 2
heatEquation = HeatEquation(1, 0, p, q, f)
heatEquation.plot_solution(2, 50, 1)
```
![Figure_1](https://user-images.githubusercontent.com/46363213/70382868-26dabb80-1918-11ea-91ef-ea636704b5ac.png)

