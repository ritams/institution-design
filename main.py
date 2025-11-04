import logging
from src.simulation import Simulation

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def main():
    logging.info("Starting main simulation")
    # Parameters
    N = 1000 # ensure this is even
    f_cultural = 0.5
    theta_list = [0, 4, 8, 12, 16]
    beta = 0.01
    max_steps = 50
    ensemble_size = 10

    sim = Simulation(N, f_cultural, theta_list, beta, max_steps, ensemble_size)
    equilibria = sim.run_simulation()
    logging.info("Main simulation completed")

if __name__ == "__main__":
    main()
