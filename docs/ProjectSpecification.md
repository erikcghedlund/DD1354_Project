# Project Specification

## Simulation of baseball in 2D (E or higher grade)

### Introduction

I want to simulate a baseball bat striking an incoming ball based on an starting point, contact point and acceleration for the bat. More specifically, variables for the mass, starting velocity, starting angle, starting height and gravitational pull. Based on this an original movement arch of the ball will be calculated. The contact point of the bat and the ball must be on this arch.

### Problem

The problem consist of two parts: Calculating collision point of two or more moving objects and apply the forces of the objects once they do collide. The minimum viable product of the simulation is one where the bat's starting point, collision point, mass and acceleration are set by the user. The project can later be extended to calculating collision point for maximizing distance instead of having a set collision point.

### Implementation

The trajectory and velocity of the different moving bodies will be simulated using the time-stepping algorithm Explicit Euler. More algorithms may be implemented if there's time to be spared. Gravitational forces will be modelled using the formula for free-fall acceleration. The collision will be modelled in adherence to Newton's third law using `F = ma`. At the start of project, elasticity will be hardcoded to 1.

The time point of the intersection of the ball's and the bat's movement will be approximated by finding the closest point to the chosen collision point in the bats traversal. The bat will start to decelerate once it has passed the collision point. The check for this event will be (sign(x), sign(y))<sub>i</sub> = (-sign(x), -sign(y))<sub>i-1</sub>. The approximated time point for collision will be the time point of these, i, i-1, which has the positional value closest to the collision point.

The simulation will be implemented in Python 3 using Pygame for visualization and Tkinter for GUI.

#### Tables of objects in simulation and their characteristics

##### Ball

| Characteristic | Priority      | Complexity |
|:--------------:|:-------------:|:----------:|
| Has mass       | High          | Trivial |
| Has starting height | High     | Trivial |
| Has starting angle | High      | Trivial |
| Has starting velocity | High   | Trivial |
| Has gravitational pull | High  | Easy    |
| These values should not be hardcoded | High | Easy |
| These values  should be changeable in UI | Mid-High  | Medium |

##### Ball's original movement arch

| Characteristic | Priority      | Complexity |
|:--------------:|:-------------:|:----------:|
| Calculated based on ball's variables      | High | Easy |
| Calculated with a time-stepping algorithm | High | Easy |
| Time-stepping interval should be able changeable in UI | Mid-High | Medium |

##### Bat

| Characteristic | Priority      | Complexity |
|:--------------:|:-------------:|:----------:|
| Has starting point | High | Trivial |
| Has collision point | High | Trivial |
| Has acceleration | High | Trivial |
| Has mass | High | Trivial |
| These values should not be hardcoded | High | Easy |
| These values  should be changeable in UI | Mid-High  | Medium |
| The collision point should be on the ball's original movement arch | High | Medium |
| Starts moving at a time calculated by the simulation based on acceleration, starting point and collision point | High | Medium |

##### Bat's movement arch

| Characteristic | Priority      | Complexity |
|:--------------:|:-------------:|:----------:|
| Is straight due to gravity not affecting the bat | High | Trivial |
| Calculated with a time-stepping algorithm | High | Easy |
| Uses the same time-stepping interval as the ball's movement arch | High | Trivial |

#### Ball's post-collision movement arch

| Characteristic | Priority      | Complexity |
|:--------------:|:-------------:|:----------:|
| Calculated the same way as the original movement arch, but with the force of the bat applied to the ball as the starting velocity | High | Easy |
| Runs until hitting ground (to start with) | High | Easy |
| Implement different elasticity for collision | Low | Hard |

### References

[Collision between two bodies (No code available)](https://ophysics.com/e2.html)

[Simulation of the arch travelled (No code available)](https://phet.colorado.edu/sims/html/projectile-motion/latest/projectile-motion_en.html)

### Risks

| Risk | Counter-actions |
|:--------------:|:-------------:|
| Pygame is too limited for good visualization | Test the visualization part early |
| Python 3 is too slow | Write computationally demanding parts in C. Avoid running the simulation in real-time |
| Project is too simple for a pass| Receive feedback from Chris Peters and TAs early in development. Have ideas of extension of the code ready |

### Degree of simulation

All of the simulation-code will be built from scratch

### Blog

[Link](https://github.com/GammaEpsilon/DD1354_Project/wiki/Blog)

