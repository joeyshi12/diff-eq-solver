# diff-eq-solver

An application that uses the finite difference method to solve various types of differential equations, such as the
heat equation and wave equation. The solution is written to a table in an Excel file, and the solution is visually
displayed on a plot. For time dependent PDEs, the plot is animated.

<p align="center">
  <img src="./assets/heat_eq_demo.png" style="width: 400px;">
  <img src="./assets/wave_eq_demo.png" style="width: 400px;">
  <img src="./assets/wave_eq_demo.gif" style="width: 400px;">
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
- [First order differential equations](#first-order-differential-equation-solving-algorithm)
- [Second order differential equations](#second-order-differential-equation-solving-algorithm)
- [One-dimensional Heat Equation](#one-dimensional-heat-equation-solving-algorithm)
- [One-dimensional Wave Equation](#one-dimensional-wave-equation-solving-algorithm)

## First Order Differential Equation Solving Algorithm
We let `x(t)` be the solution function and defined first order differential equation problems by
* `x' = f(t, x)`, `0 <= t <= T`
* `x0 = x(0)`

where `f(t, x)` is an arbitrary function of `(t, x)` and `x0` is some constant. The user is allowed to specify these parameters and also defined the range of the solution `0 <= t <= T` and the points in the solution array `len(x) = N > 0`.

Let `dt = T / (N - 1)`. If we have a 'small' value of `dt`, we can approximate the derivative using the forward difference: `x'(t) = (x(t + dt) - x(t)) / dt`. Thus, `x(t + dt) = x(t) + f(t, x(t)) * dt`.

So, we may iteratively compute values for `x[i] = x(i * dt)` from `i = 0` to `i = N - 1` as such:
```python
x[0] = x0
x[1] = x[0] + f(0, x[0]) * dt
x[2] = x[1] + f(dt, x[1]) * dt
...
x[N - 1] = x[N - 2] + f((N - 2) * dt, x[N - 2]) * dt
```

We can write this more simply as:
```python
x[0] = x0

for i in range(1, N):
  x[i] = x[i - 1] + f((i - 1) * dt, x[i - 1]) * dt
```

## Second Order Differential Equation Solving Algorithm
We let `x(t)` be the solution function for the differential equation defined by
* `y' = f(t, x, y)`, `0 <= t <= T`
* `y = x'`
* `x0 = x(0)`
* `y0 = x'(0)`

where `f(t, x, y)` is an arbitrary function of `(t, x, y)` and `x0`, `y0` are some constants. As with the [first order differential equation solving algorithm](#first-order-differential-equation-solving-algorithm), we can derive `x'(t + dt) = x'(t) + f(t, x(t), y(t)) * dt` by using the forward difference approximation, where `dt = T / (N - 1)`.

So, we may iteratively compute values for `x[i] = x(i * dt)` from `i = 0` to `i = N - 1` as such:
```python
x[0] = x0
y[0] = y0

x[1] = x[0] + y[0] * dt
y[1] = y[0] + f(0, x[0], y[0]) * dt

...

x[N - 1] = x[N - 2] + y[N - 2] * dt
y[N - 1] = y[N - 2] + f((N - 2) * dt, x[N - 2], y[N - 2]) * dt
```

We can write this more simply as:
```python
x[0], y[0] = x0, y0

for i in range(1, N):
  x[i] = x[i - 1] + y[i - 1] * dt
  y[i] = y[i - 1] + f((i - 1) * dt, x[i - 1], y[i - 1]) * dt
```

## One-dimensional Heat Equation Solving Algorithm
We let `u(t, x)` be the solution function for the differential equation defined by
* u(x, t)
* Φ1(t) (Left Dirichlet BC)
* Φ2(t) (Right Dirichlet BC)

TODO

## One-dimensional Wave Equation Solving Algorithm
TODO
