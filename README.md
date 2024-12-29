# diff-eq-solver

![Tests](https://github.com/joeyshi12/diff-eq-solver/actions/workflows/tests.yml/badge.svg)
![PyPI](https://img.shields.io/pypi/v/diffeq-solver-tk)

An application that uses the finite difference method to solve various types of differential equations, such as the
heat equation and wave equation. The solution is written to a table in an Excel file, and the solution is visually
displayed on a plot. For time dependent PDEs, the plot is animated.

*Tkinter works best on Windows*

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/github.com/joeyshi12/diff-eq-solver/)

<p align="center">
  <img src="https://raw.githubusercontent.com/joeyshi12/diff-eq-solver/master/snapshots/heat_eq_demo.png" style="width: 400px;">
  <img src="https://raw.githubusercontent.com/joeyshi12/diff-eq-solver/master/snapshots/wave_eq_demo.png" style="width: 400px;">
  <img src="https://raw.githubusercontent.com/joeyshi12/diff-eq-solver/master/snapshots/wave_eq_demo.gif" style="width: 400px;">
</p>

## Installation
```
pip3 install diffeq-solver-tk
```

## Usage
The GUI can be started with `detk`. Once you open the solver, choose a differential equation type through the
navigation bar above and enter the parameters for your equation. Clicking "Solve" will run the solving algorithm
for your equation and generate a static plot in the right window. After a solution is prepared, you can export the
solution as an xlsx file by clicking "Export". For partial differential equation types, you can play an animation
in the right window by clicking "Play" and switch back to the static plot by clicking "Show Plot".

diffeq-solver-tk can also be used in the command-line by running `detk-cli <diff-eq-type> <infile> <outfile>`.
Examples of valid `<infile>` files are provided in `tests/queries`. Run `detk-cli -h` for more info.

## Dev Wiki
- [First order differential equations](https://github.com/joeyshi12/diff-eq-solver/wiki/First-Order-Differential-Equation-Solving-Algorithm)
- [Second order differential equations](https://github.com/joeyshi12/diff-eq-solver/wiki/Second-Order-Differential-Equation-Solving-Algorithm)
- [One-dimensional Heat Equation](https://github.com/joeyshi12/diff-eq-solver/wiki/One-dimensional-Heat-Equation-Solving-Algorithm)
- [One-dimensional Wave Equation](https://github.com/joeyshi12/diff-eq-solver/wiki/One-dimensional-Wave-Equation-Solving-Algorithm)
