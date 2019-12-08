# diff-eq-solver

This program uses various finite difference methods to solve ordinary differential equations and partial differential 
equations. For partial differential equations, we focus on specific types, such as the heat equation, wave equation, 
and Laplace's equation. Matplotlib is used to represent the solutions on graphs. <br>
[Work in progress]

## Getting Started

The file for running this program can be found at src/main/ui/Main.py. 

## Example
```python
heatEquation = HeatEquation(1, 0, lambda x: 1 - (x - 1) ** 2)
heatEquation.plot_solution(2, 50, 1)
```
![Figure_1](https://user-images.githubusercontent.com/46363213/70382868-26dabb80-1918-11ea-91ef-ea636704b5ac.png)

