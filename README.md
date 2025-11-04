# Evolutionary Game with Cultural Sway

## 1. Overview

This document specifies a simulation framework for an evolutionary game with **Innovation (I)** and **Tradition (T)** strategies, governed by a tunable environmental parameter $\theta$ ("theta").  
The game explores how populations evolve under shifting environmental incentives and **cultural inertia**, modeled by a *cultural sway* parameter.

The framework supports multiple games indexed by $\theta$ values (sequentially or arbitrarily chosen).  
Each game produces equilibrium strategy distributions that feed into subsequent games, modulated by the cultural sway mechanism.

---

## 2. Game Definition

### 2.1 Strategy Space
Each agent chooses one of two strategies:
- **T:** Tradition  
- **I:** Innovation

### 2.2 Payoff Matrix (Parameterization by $\theta$)

For any pairwise interaction:

|                  | Tradition (T)       | Innovate (I)     |
|------------------|--------------------|------------------|
| **Tradition (T)** | $(16 - \theta, 16 - \theta)$ | $(4, 4)$           |
| **Innovate (I)**  | $(4, 4)$           | $(\theta, \theta)$ |

- $\theta \in [0, 16]$  
- Low $\theta$ favors **Tradition** (higher payoff for T–T interactions).  
- High $\theta$ favors **Innovation** (higher payoff for I–I interactions).  

### 2.3 Equilibrium Regions

| $\theta$ Range | Dominant Equilibrium | Description |
|-----------------|----------------------|--------------|
| $0 \leq \theta < 6$ | Tradition Immune | Pure Tradition is stable |
| $6 \leq \theta \leq 10$ | Susceptible | Mixed equilibria may arise |
| $10 < \theta \leq 16$ | Innovation Immune | Pure Innovation is stable |

---

## 3. Agents and Population

### 3.1 Agent Properties
Each of the $N$ agents has the following attributes:
- **strategy:** current strategy $\in \{T, I\}$  
- **payoff:** cumulative payoff over current game  
- **cultural_sway:** boolean (True/False)  
- **history:** record of strategies across all previous $\theta$ games (infinite memory)  
- **game_index:** current $\theta$ value associated with the game instance  

### 3.2 Initialization
At the beginning of the first game (initial $\theta$):
- Strategies are assigned randomly with equal probability (50% T, 50% I).
- A fraction $f_{\text{cultural}}$ (e.g., $3/4$) of agents are assigned `cultural_sway = True`.  
- The remaining $(1 - f_{\text{cultural}})$ have `cultural_sway = False`.

---

## 4. Game Dynamics (Within a Single $\theta$)

### 4.1 Population Interaction
- Population is **well-mixed** (no spatial structure).
- Each agent interacts with **one random partner** per iteration (pairwise interaction).
- Both agents receive payoffs from the payoff matrix according to their chosen strategies.

### 4.2 Evolutionary Update Rule
After all agents collect payoffs:
1. Each agent $i$ randomly samples another agent $j$ from the population.
2. Let $\pi_i$ and $\pi_j$ be their payoffs.  
3. The probability that $i$ adopts $j$’s strategy follows the **Fermi update rule**:

   $$
   P(\text{$i$ adopts $j$}) = \frac{1}{1 + \exp[-\beta (\pi_j - \pi_i)]}
   $$

   where $\beta$ is the selection intensity parameter.

4. Each agent independently updates its strategy based on this probability.

The implementation should be modular, allowing other update rules to be easily substituted.

### 4.3 Stopping Condition
Each simulation runs for a fixed number of steps (`max_steps`), or until no strategy changes occur between iterations.

---

## 5. Sequential Games and Cultural Sway

### 5.1 Multi-Game Simulation
A simulation consists of multiple **game instances**, each parameterized by a distinct $\theta$ value:

$$
\Theta = [\theta_1, \theta_2, \ldots, \theta_M]
$$

The $\theta$ values may:
- increase gradually,
- decrease,
- or vary arbitrarily.

### 5.2 Determining Initial Conditions for New Games
When a new $\theta_k$ is introduced:
1. Identify the **closest previous game** $\theta_m$ among $\{\theta_1, \ldots, \theta_{k-1}\}$.  
   (Minimize $|\theta_k - \theta_m|$.)
2. Retrieve the equilibrium strategy distribution from that previous game:
   - e.g., if 90% of the population played Tradition and 10% Innovation.

3. Initialize the new population as follows:
   - For agents with `cultural_sway = True`:  
     Each agent independently draws a strategy according to the previous equilibrium distribution (e.g., $P(T) = 0.9$, $P(I) = 0.1$).
   - For agents with `cultural_sway = False`:  
     Each agent is initialized with $P(T) = 0.5$, $P(I) = 0.5$ (random uniform).

### 5.3 Memory and Historical Influence
- All agents retain full memory of all previous games (infinite history).  
- Historical data (strategies and payoffs for all $\theta$) can be used for later analysis.

---

## 6. Parameters Summary

| Parameter | Description | Typical Value |
|-----------|-------------|----------------|
| $N$ | Number of agents | 100 |
| $\theta$ | Environment parameter | $[0, 16]$ |
| $f_{\text{cultural}}$ | Fraction of agents with cultural sway | $0.75$ |
| $\beta$ | Selection intensity (Fermi rule) | $1.0$ |
| `max_steps` | Max iterations per game | 5000 |
| `payoff_matrix` | As defined in Section 2.2 | — |

---

## 7. Simulation Flow

1. **Initialize** population for $\theta_1$:
   - Assign strategies randomly.
   - Assign cultural_sway attributes.

2. **Run Evolution** under $\theta_1$:
   - Pairwise interactions and payoff accumulation.
   - Strategy updates via Fermi rule.
   - Continue until equilibrium or `max_steps`.

3. **Record Equilibrium Composition**:
   - Compute fraction of T and I in final state.

4. **For each subsequent $\theta_k$:**
   - Determine closest previous $\theta_m$.
   - Initialize strategies according to Section 5.2.
   - Run evolution again.

5. **Repeat** until all $\theta$ values in $\Theta$ are simulated.

---

## 8. Notes and Extensibility

- The model can later include:
  - Network structure (e.g., spatial lattice or graph-based interactions)
  - Payoff noise or perception bias
  - Cultural sway decay or heterogeneity
  - Time-varying $\theta$ (dynamic environment)
- Output analysis (mean strategy fractions, stability measures, entropy, etc.) will be added in later design stages.

---

*Document version 1.0 – Framework design for the Evolutionary Game with Cultural Sway.*

