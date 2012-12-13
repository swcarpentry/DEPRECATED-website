# The Computer Language Benchmarks Game
# http://shootout.alioth.debian.org/
#
# originally by Kevin Carson
# modified by Tupteq, Fredrik Johansson, and Daniel Nanz
# modified by Maciej Fijalkowski
# modified by Greg Wilson
# modified by Erik Bray

import sys
from math import pi
import time
import numpy as np

SOLAR_MASS = 4 * pi * pi
DAYS_PER_YEAR = 365.24

#-------------------------------------------------------------------------------

def setup(raw):
    """
    Turn a list-of-lists of [name, px, py, pz, vx, vy, vz, m] records
    into three NumPy arrays: position vectors, velocity vectors, and
    masses.
    """
    positions = np.empty((len(raw), 3))
    velocities = np.empty((len(raw), 3))
    masses = np.empty(len(raw))
    for i, b in enumerate(raw):
        positions[i] = b[1:4]
        velocities[i] = b[4:7]
        masses[i] = b[7]
    return positions, velocities, masses

#-------------------------------------------------------------------------------

def square_vector(arr):
    """
    Square either a single vector or an array of vectors.
    """
    return (arr ** 2).sum(axis=1)

#-------------------------------------------------------------------------------

def advance(dt, num_steps, positions, velocities, masses):
    """
    Advance the simulation a specified number of timesteps.
    """
    for step in xrange(num_steps):
        for i, pos in enumerate(positions):
            mass = masses[i]
            pos_rest = positions[i + 1:]
            vel_rest = velocities[i + 1:]
            mass_rest = masses[i + 1:]
            d_pos = pos - pos_rest
            mags = dt * square_vector(d_pos) ** -1.5
            left_forces = mass * mags
            right_forces = mass_rest * mags
            left_d_vel = d_pos.T * right_forces
            right_d_vel = d_pos.T * left_forces
            velocities[i] -= left_d_vel.sum(axis=1)
            vel_rest += right_d_vel.T
        positions += velocities * dt

#-------------------------------------------------------------------------------

def total_energy(positions, velocities, masses):
    """
    Calculate the total energy (kinetic and potential) in the system.
    """
    e = (masses * square_vector(velocities) / 2).sum()
    for i, pos in enumerate(positions):
        mass = masses[i]
        pos_rest = positions[i + 1:]
        mass_rest = masses[i + 1:]
        d_pos = pos - pos_rest
        d_e = (mass * mass_rest) / square_vector(d_pos) ** 0.5
        e -= d_e.sum()
    return e

#-------------------------------------------------------------------------------

def offset_momentum(ref, velocities, masses):
    origin = -(velocities.T * masses).sum(axis=1)
    velocities[ref] = origin / masses[ref]

#-------------------------------------------------------------------------------

def simulate(positions, velocities, masses, timestep_len, num_timesteps):
    """
    Run the simulation.
    """
    offset_momentum(0, velocities, masses)
    e_original = total_energy(positions, velocities, masses)
    t_original = time.time()
    advance(timestep_len, num_timesteps, positions, velocities, masses)
    t_final = time.time()
    e_final = total_energy(positions, velocities, masses)
    d_energy = 100 * abs((e_final - e_original) / e_original)
    d_time = t_final - t_original
    print "%-9s: %.9f - %.9f (%f %%) / %.9f" % \
          ("Final", e_final, e_original, d_energy, d_time)

#-------------------------------------------------------------------------------

def main(args, bodies):
    num_timesteps = int(sys.argv[1])
    if len(sys.argv) > 2:
        timestep_len = float(sys.argv[1])
    else:
        timestep_len = 0.01
    positions, velocities, masses = setup(bodies)
    simulate(positions, velocities, masses, timestep_len, num_timesteps)

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    bodies = [
        ['Sun',
         0.0, 0.0, 0.0,
         0.0, 0.0, 0.0,
         1.0 * SOLAR_MASS],

        ['Jupiter',
          4.84143144246472090e+00,
         -1.16032004402742839e+00,
         -1.03622044471123109e-01,
          1.66007664274403694e-03 * DAYS_PER_YEAR,
          7.69901118419740425e-03 * DAYS_PER_YEAR,
         -6.90460016972063023e-05 * DAYS_PER_YEAR,
          9.54791938424326609e-04 * SOLAR_MASS],

        ['Saturn',
          8.34336671824457987e+00,
          4.12479856412430479e+00,
         -4.03523417114321381e-01,
         -2.76742510726862411e-03 * DAYS_PER_YEAR,
          4.99852801234917238e-03 * DAYS_PER_YEAR,
          2.30417297573763929e-05 * DAYS_PER_YEAR,
          2.85885980666130812e-04 * SOLAR_MASS],

        ['Uranus',
          1.28943695621391310e+01,
         -1.51111514016986312e+01,
         -2.23307578892655734e-01,
          2.96460137564761618e-03 * DAYS_PER_YEAR,
          2.37847173959480950e-03 * DAYS_PER_YEAR,
         -2.96589568540237556e-05 * DAYS_PER_YEAR,
          4.36624404335156298e-05 * SOLAR_MASS],

        ['Neptune',
          1.53796971148509165e+01,
         -2.59193146099879641e+01,
          1.79258772950371181e-01,
          2.68067772490389322e-03 * DAYS_PER_YEAR,
          1.62824170038242295e-03 * DAYS_PER_YEAR,
         -9.51592254519715870e-05 * DAYS_PER_YEAR,
          5.15138902046611451e-05 * SOLAR_MASS]
    ]
    main(sys.argv, bodies)
