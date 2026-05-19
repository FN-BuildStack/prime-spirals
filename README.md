# Prime-Spirals: Interactive Geometric Visualization

## Abstract
Prime-Spirals is a high-performance, object-oriented visualization suite built in Python. It provides an interactive, real-time animation of prime number distributions mapped across two distinct mathematical geometries: the Ulam Spiral (Square) and the Sacks Spiral (Archimedean). 

This project demonstrates advanced management of event-loops, dynamic rendering buffers, and vectorized mathematical computations within graphical interfaces.

## Mathematical Geometry

### The Ulam Spiral
Discovered by Stanislaw Ulam in 1963, this structure plots positive integers in a square spiral. Prime numbers tend to conspicuously cluster along specific diagonal lines, revealing unexplained quadratic polynomials that generate unusually high densities of primes.

### The Sacks Spiral
Created by Robert Sacks in 1994, this variant plots the integers on an Archimedean spiral where the polar coordinates are defined by:

$$r = \sqrt{n}$$
$$\theta = 2\pi\sqrt{n}$$

In this topology, perfect squares align perfectly in a straight horizontal line, while primes form distinct curves corresponding to Euler's quadratic generating equations.

## Technical Architecture

* **Vectorized Sieve Engine:** Utilizes a NumPy-optimized Sieve of Eratosthenes to precompute primality boolean masks in milliseconds, completely bypassing the computational bottleneck of standard iterative prime evaluations.
* **Dynamic Buffer Rendering:** Leverages `matplotlib.animation.FuncAnimation` to update coordinate offsets (`set_offsets()`) and array slices dynamically. It avoids full-frame redraws and implements conditional geometry injection to prevent CPU/Memory saturation during the 20,000-point rendering cycle.
* **Event-Driven UI:** Implements hardware hooks (`mpl_connect`) to handle asynchronous keyboard and mouse inputs, allowing real-time interruption and modification of the rendering thread (speed adjustments, theme toggling, and fast-forward coordinate tracking).

## Installation

Deploy the suite within an isolated virtual environment to ensure dependency integrity:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/FN-BuildStack/prime-spirals.git](https://github.com/FN-BuildStack/prime-spirals.git)
   cd prime-spirals

2. **Initialize the virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

## Execution & Controls

Launch the interactive engine directly from the terminal:

```bash
python spirals.py
```

### Hotkeys & Interactivity

* **[UP / DOWN]:** Accelerate or decelerate the animation frame rate dynamically.
* **[B]:** Toggle between Dark Mode and Light Theme.
* **[G]:** Toggle analytical grid bounds.
* **[L]:** Toggle continuous spiral path rendering (optimized for zero-lag visibility switching).
* **[C]:** Toggle prime coordinate scatter dots.
* **Search Box:** Input any integer up to the defined boundary (default: `20000`) to highlight its exact vector position across both geometries. If the integer is beyond the current rendering index, the engine will automatically fast-forward the timeline to the target.

## License

Distributed under the MIT License. See `LICENSE` for more information.
