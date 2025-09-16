#python3.13.2

# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt

# --- Physical Constants ---
# Parameters given in the problem
G = 9.81  # Gravitational acceleration (m/s^2)
L = 2.5   # Length of the pendulum arm (m)

# Set a nice plotting style for the figures
plt.style.use('seaborn-v0_8-whitegrid')

# Part 1: Calculate the analytical period for the linear pendulum
T_analytical = 2 * np.pi * np.sqrt(L / G)
print(f"The analytical period of the linear pendulum is T = {T_analytical:.4f} seconds.")

def run_simulation(theta0_deg, t_max, dt, is_nonlinear=False):
    """
    Runs the pendulum simulation using the Velocity Verlet method.
    
    Args:
        theta0_deg (float): Initial angle in degrees.
        t_max (float): Maximum simulation time in seconds.
        dt (float): Time step in seconds.
        is_nonlinear (bool): If True, use sin(theta). If False, use theta.
        
    Returns:
        A dictionary containing the results: time, theta, energy_per_mass.
    """
    # TODO: I should add 'omega' to the return values and the docstring.
    # It's not required for this homework, but it would be good practice for a general-purpose function.
    
    # 1. Initialization
    theta0_rad = np.deg2rad(theta0_deg)
    num_steps = int(t_max / dt)
    
    t = np.linspace(0, t_max, num_steps + 1)
    theta = np.zeros(num_steps + 1)
    omega = np.zeros(num_steps + 1)
    
    theta[0] = theta0_rad
    omega[0] = 0.0

    # 2. Main integration loop
    for i in range(num_steps):
        # Calculate current acceleration
        if is_nonlinear:
            alpha_t = -(G / L) * np.sin(theta[i])
        else:
            alpha_t = -(G / L) * theta[i]
            
        # Update position
        theta[i+1] = theta[i] + omega[i] * dt + 0.5 * alpha_t * (dt**2)
        
        # Calculate acceleration at the new position
        if is_nonlinear:
            alpha_t_plus_1 = -(G / L) * np.sin(theta[i+1])
        else:
            alpha_t_plus_1 = -(G / L) * theta[i+1]
            
        # Update velocity
        omega[i+1] = omega[i] + 0.5 * (alpha_t + alpha_t_plus_1) * dt

    # 3. Post-processing to calculate energy (for Part 3)
    kinetic_energy_per_mass = 0.5 * (L**2) * (omega**2)
    potential_energy_per_mass = G * L * (1 - np.cos(theta))
    total_energy_per_mass = kinetic_energy_per_mass + potential_energy_per_mass
    
    return {
        "time": t,
        "theta": np.rad2deg(theta), # Convert back to degrees for plotting
        "energy_per_mass": total_energy_per_mass
    }

def analytical_solution(t, theta0_rad):
    """Calculates the analytical solution for the linear pendulum."""
    omega_analytical = np.sqrt(G / L)
    return theta0_rad * np.cos(omega_analytical * t)

# Part 2: Run the linear simulation and plot the comparison
theta0_linear_deg = 2.5
dt_good = 0.01
sim_time_linear = 5 * T_analytical # Simulate for 5 periods

# Run the simulation
result_linear = run_simulation(theta0_linear_deg, sim_time_linear, dt_good, is_nonlinear=False)

# Calculate the corresponding analytical solution for the same time points
theta_analytical_rad = analytical_solution(result_linear["time"], np.deg2rad(theta0_linear_deg))
theta_analytical_deg = np.rad2deg(theta_analytical_rad)

# Plot the results
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(result_linear["time"], result_linear["theta"], label=f'Numerical (dt={dt_good}s)', linestyle='-')
ax.plot(result_linear["time"], theta_analytical_deg, label='Analytical', linestyle='--')
ax.set_title(f'Linear Pendulum ($\u03B8_0$={theta0_linear_deg}°): Numerical vs. Analytical Solution')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Angle $\u03B8$ (degrees)')
ax.legend()
ax.grid(True)
plt.show()

# Part 3: Calculate the exact total energy for the nonlinear case
theta0_nonlinear_deg = 125.0
exact_energy_per_mass = G * L * (1 - np.cos(np.deg2rad(theta0_nonlinear_deg)))
print(f"Exact Total Energy per unit mass = {exact_energy_per_mass:.4f} J/kg.")

# --Plot--
# Part 3: Run nonlinear simulations to observe energy drift
sim_time_nonlinear = 75 # Should be enough for >15 periods
# Set a series of increasing time steps to test
time_steps = [0.04, 0.08, 0.16, 0.32] 
fig, ax = plt.subplots(figsize=(12, 7))

# Plot the exact energy as a horizontal reference line
ax.axhline(y=exact_energy_per_mass, color='black', linestyle='--', label='Exact Energy')

for dt in time_steps:
    result = run_simulation(theta0_nonlinear_deg, sim_time_nonlinear, dt, is_nonlinear=True)
    ax.plot(result["time"], result["energy_per_mass"], label=f'Numerical (dt={dt}s)')

# Style the plot
ax.set_title('Nonlinear Pendulum: Total Energy vs. Time (Illustrating Energy Drift)')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Total Energy per Mass (J/kg)')
ax.legend()
ax.grid(True)
plt.show()

# [Self-Note]: The plot above uses default colors and line styles for all curves,
# which makes them a bit hard to tell apart. For a final report, I should manually specify
# different colors or linestyles for each 'dt' value to improve clarity.
# For example, by adding a color=... or linestyle=... argument inside the plot loop.
# anyway, this is sufficient for now. got no time for that.