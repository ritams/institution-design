from src.simulation import Simulation

def main():
    # Parameters
    N = 100
    f_cultural = 0.75
    theta_list = [0, 4, 8, 12, 16]
    beta = 1.0
    max_steps = 5000

    sim = Simulation(N, f_cultural, theta_list, beta, max_steps)
    equilibria = sim.run_simulation()
    print("Equilibria:", equilibria)

if __name__ == "__main__":
    main()
