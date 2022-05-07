# diff-eq-solver

![Tests](https://github.com/joeyshi12/diff-eq-solver/actions/workflows/tests.yml/badge.svg)

An application that uses the finite difference method to solve various types of differential equations, such as the
heat equation and wave equation. The solution is written to a table in an Excel file, and the solution is visually
displayed on a plot. For time dependent PDEs, the plot is animated.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/github.com/joeyshi12/diff-eq-solver/)

<p align="center">
  <img src="./assets/heat_eq_demo.png" style="width: 400px;">
  <img src="./assets/wave_eq_demo.png" style="width: 400px;">
  <img src="./assets/wave_eq_demo.gif" style="width: 400px;">
</p>

## How to run locally
```
# Install package
pip3 install -e .

# Run diffeq_tk script
detk
```

## How to use
Once you open the solver, choose a differential equation type through the navigation bar above and enter the parameters for your equation. Clicking "Solve" will run the solving algorithm for your equation and generate a static plot in the right window. After a solution is prepared, you can export the solution as an xlsx file by clicking "Export". For partial differential equation types, you can play an animation in the right window by clicking "Play" and switch back to the static plot by clicking "Show Plot".

All of following differential equations are currently supported:
- [First order differential equations](#first-order-differential-equation-solving-algorithm)
- [Second order differential equations](#second-order-differential-equation-solving-algorithm)
- [One-dimensional Heat Equation](#one-dimensional-heat-equation-solving-algorithm)
- [One-dimensional Wave Equation](#one-dimensional-wave-equation-solving-algorithm)

## First Order Differential Equation Solving Algorithm
First order differential equations problems can be written as the following initial value problem:
* `x' = f(t, x)`, `0 < t <= T`
* `x0 = x(0)` [initial value]

Let `x[i] = x(i * dt)` for `i = 0` to `i = N - 1`, where `dt = T / (N - 1)`. For `dt` 'small' enough, we can approximate the derivative `x'(t)` using the forward difference:

```
x'(t) = (x(t + dt) - x(t)) / dt = f(t, x)
x(t + dt) = x(t) + f(t, x) * dt
```

Then, we can compute all values of `x[i]` with the following:
```
x[i] = { x[i - 1] + f(i * dt, x) * dt    0 < i <= N - 1
       { x0                              i = 0
```

So, the algorithm simplifies to the following:
```python
x = np.zeros(N)
x[0] = x0
for i in range(1, N):
  x[i] = x[i - 1] + f((i - 1) * dt, x[i - 1]) * dt
```
[[full code implementation](src/diffeq_solver_tk/services/first_order_ode_service.py)]

## Second Order Differential Equation Solving Algorithm
Second order differential equation problems can be written as the following initial value problem:
* `y' = f(t, x, y)`, `0 < t <= T`
* `y = x'`
* `x0 = x(0)` [initial value]
* `y0 = x'(0)` [initial derivative]

Let `x[i] = x(i * dt)` and `y[i] = y(i * dt)` for `i = 0` to `i = N - 1`, where `dt = T / (N - 1)`. As with the [first order ode problem](#first-order-differential-equation-solving-algorithm), for `dt` small enough, we can use the forward difference approximation to obtain
```
y(t) = y(t - dt) + f(t - dt, x(t - dt), y(t - dt)) * dt
```

Again, we can use the forward difference approximation `y(t) =  x'(t) = [x(t + dt) - x(t)] / dt` to get
```
x(t + dt) = x(t) + y(t) * dt
```

So, we can compute all values of `x[i]` and `y[i]` with the following:
```
x[i] = { x[i - 1] + y[i - 1] * dt   0 < i <= N - 1
       { x0                         i = 0

y[i] = { y[i - 1] + f(i * dt, x[i - 1], y[i - 1]) * dt    0 < i <= N - 1
       { y0                                               i = 0
```

Thus, the algorithm simplifies to the following:
```python
x, y = np.zeros([2, N])
x[0], y[0] = x0, y0
for i in range(1, N):
  x[i] = x[i - 1] + y[i - 1] * dt
  y[i] = y[i - 1] + f((i - 1) * dt, x[i - 1], y[i - 1]) * dt
```
[[full code implementation](src/diffeq_solver_tk/services/second_order_ode_service.py)]

## One-dimensional Heat Equation Solving Algorithm
We let `u(t, x)` be the solution function for the differential equation defined by
* `u_{t}(t, x) = α * u_{xx}(t, x) + S(t, x)`, `0 < x <= L`, `0 < t <= T`
* `u(t, 0) = Φ_1(t)` (Left Dirichlet Boundary Condition)
* `u_{t}(t, L) = Φ_2(t)` (Right Neumann Boundary Condition)
* `u(0, x) = f(x)` (initial values)

Let `u[i][j] = u(i * dt, j * dx)` for `i = 0` to `i = K - 1` and `j = 0` to `j = N - 1` for `dt = T / (K - 1)` and `dx = L / (N - 1)`. For `dt` small enough, we can approximate `u_{t}(t, x)` with the forward difference:
```
u_{t}(t, x) = (u(t + dt, x) - u(t, x)) / dt
```

For `dx` small enough, we can approximate `u_{xx}(t, x)` with the second order central difference:
```
u_{xx}(t, x) = (u(t, x + dx) - 2 * u(t, x) + u(t, x - dx)) / (dx ** 2)
```

So after substituting and rearranging `u_{xx}`, `u_{t}` in `u_{t}(t, x) = α * u_{xx}(t, x) + S(t, x)`, we get
```
u(t + dt, x) = u(t, x) + (α * dt / dx ** 2) * (u(t, x + dx) - 2 * u(t, x) + u(t, x - dx)) + S(t, x) * dt
```

Thus, we can compute all values of `u[i][j]` with the following:
```
u[i][j] = { u[i - 1, j] + (α * dt / dx ** 2) * (u[i - 1, j + 1] - 2 * u[i - 1, j] + u[i - 1, j - 1]) + S(i * dt, j * dx) * dt   0 < i <= K - 1, 0 < j < N - 1
          { Φ_1(i * dt)                                                                                                         j = N - 1
          { u[i, j - 2] + Φ_2(i * dt) * dt                                                                                      j = 0
          { f(j * dx)                                                                                                           i = 0
```
[[full code implementation](src/diffeq_solver_tk/services/heat_equation_service.py)]

## One-dimensional Wave Equation Solving Algorithm
TODO
