import logging
from src.simulation import Simulation

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def main():
    logging.info("Starting main simulation")
    # Parameters
    N = 1000 # ensure this is even
    f_cultural = 3 / 4
    theta_list = [1, 3, 15]
    beta = 0.1
    max_steps = 5
    ensemble_size = 100

    sim = Simulation(N, f_cultural, theta_list, beta, max_steps, ensemble_size)
    equilibria = sim.run_simulation()
    logging.info("Main simulation completed")

if __name__ == "__main__":
    main()
