# diff-eq-solver

An application that uses the finite difference method to solve various types of differential equations, such as the
heat equation and wave equation. The solution is written to a table in an Excel file, and the solution is visually 
displayed on a plot. For time dependent PDEs, the plot is animated.  

<p align="center">
  <img src="./images/demo_fig_1.PNG" style="width: 400px;">
  <img src="./images/demo_fig_3.PNG" style="width: 400px;">
  <img src="./images/demo_fig_2.gif" style="width: 400px;">
</p>

## How to run locally
```
# Install requirements
pip3 install -r requirements.txt

# Run program
python3 app.py
```

## How to use
Once you open the solver, choose a differential equation type through the navigation bar above and enter the parameters for your equation. Clicking "Solve" will run the solving algorithm for your equation and generate a static plot in the right window. After a solution is prepared, you can export the solution as an xlsx file by clicking "Export". For partial differential equation types, you can play an animation in the right window by clicking "Play" and switch back to the static plot by clicking "Show Plot".

All of following differential equations are currently supported:
- [First order differential equations](#first-order-differential-equations)
- [Second order differential equations](#second-order-differential-equations)
- [One-dimensional Heat Equation](#one-dimensional-heat-equation)
- [One-dimensional Wave Equation](#one-dimensional-wave-equation)

## First Order Differential Equations
TODO

## Second Order Differential Equations
TODO

## One-dimensional Heat Equation
TODO

## One-dimensional Wave Equation
TODO
