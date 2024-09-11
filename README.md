## Ball Collision Simulator in a Dynamic Gravity Field

This GitHub repository contains a physics simulation project that models the collisions between multiple balls within a closed box. The unique feature of this simulation is the ability to change the field of gravity within the system, allowing for the observation of how varying gravitational forces affect the movement and interactions of the balls.

### Features

* **Realistic Physics:** The simulation employs physics principles to accurately calculate the motion, collisions, and energy transfers between the balls.
* **Dynamic Gravity:** The user can modify the direction and magnitude of the gravitational field, leading to interesting and unpredictable ball movements.
* **Customizable Parameters:** The number of balls, their properties (size, mass, elasticity), and the dimensions of the box can be adjusted.
* **Visualization:** The simulation provides a visual representation of the balls and their trajectories within the box, allowing for easy observation of the effects of the changing gravity.

### Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/GlitchyPeng/Ball_Collision_Simulation.git
   ```
2. **Install Dependencies:**
   ```bash
   cd Ball_Collision_Simulation
   pip install -r requirements.txt
   ```
3. **Run the Simulation:**
   ```bash
   python Simulation.py
   ```

### Usage

* **Adjusting Parameters:** Modify the configuration file (`config.json`) to change the number of balls, their properties, the box dimensions, and the initial gravity field.
* **Controlling Gravity:** Use the provided interface (GUI or command-line) to dynamically change the gravity during the simulation.
* **Observing the Results:** Watch the visualization to see how the balls react to the changing gravitational forces.

### Potential Applications

* **Educational Purposes:** The simulation can be used to demonstrate physics concepts related to motion, collisions, and gravity in an interactive and engaging way.
* **Research:** The ability to manipulate gravity can be useful for exploring the behavior of particles under non-standard conditions.
* **Game Development:** The simulation can serve as a foundation for building games with unique physics-based mechanics.

### Contributing

Contributions are welcome! Feel free to open issues for bug reports or feature requests, or submit pull requests with improvements to the code.

### License

This project is licensed under the MIT License - see the `LICENSE` file for details.

**Disclaimer:** This simulation is a simplified model of real-world physics. While efforts have been made to ensure accuracy, there may be limitations and deviations from actual physical phenomena.
