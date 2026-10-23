
# Jaipur AI Agent - GoldCrusher

### Reinforcement Learning & Evolutionary Optimization for Imperfect-Information Strategy Games

**GoldCrusher** is a custom AI agent developed to play **Jaipur**, a two-player competitive strategy card game involving imperfect information, stochastic outcomes, resource management, and sequential decision-making.

The project explores **reinforcement learning, evolutionary optimization, and game-theoretic decision-making** to develop an autonomous agent capable of making strategic decisions under uncertainty.

Built and evaluated using the open-source [Bazaar-AI](https://github.com/chandra-gummaluru/bazaar-ai) simulation framework developed by Chandra Gummaluru, which provides the underlying Jaipur game environment, agent interface, and visualization tools.

**Key Result:** GoldCrusher achieved a **70%+ win rate against a reference agent**, representing a **20+ percentage-point performance advantage** in head-to-head evaluations.

---

## Project Overview

Jaipur is a two-player, turn-based trading game in which players compete to accumulate points by collecting and selling goods, managing limited resources, and anticipating their opponent's decisions.

Unlike fully observable games, Jaipur requires players to make decisions without complete knowledge of their opponent's hand or the remaining deck.

This introduces several AI challenges:

- **Imperfect Information:** Opponents' hands and future card draws are hidden, requiring decisions under uncertainty.
- **Stochastic Outcomes:** Card draws and evolving market conditions introduce randomness.
- **Strategic Resource Management:** Agents must balance collecting goods, executing profitable trades, and maintaining flexibility.
- **Delayed Rewards:** Actions may improve future opportunities rather than immediately maximize points.
- **Competitive Decision-Making:** Effective strategies require anticipating an opponent's actions and adapting to changing game states.

The objective of this project was to develop an autonomous agent capable of learning and refining effective gameplay strategies in this environment.

## GoldCrusher AI Agent

The custom **GoldCrusher** agent is located in the [`agents/`](agents/) directory, alongside other agents used for simulation and performance benchmarking.

GoldCrusher was developed to optimize decision-making in Jaipur by evaluating available actions, balancing immediate rewards against future outcomes, and adapting its strategy to competitive game conditions.

### Core Approach

**1. Reinforcement Learning**

Explored reward-based learning approaches to improve decision-making through gameplay experience and performance feedback.

**2. Evolutionary Optimization**

Used iterative evolutionary optimization to refine agent strategies and improve competitive performance.

**3. Strategic Decision-Making**

Developed decision logic to navigate trade-offs between collecting resources, selling goods, managing camels, and responding to the opponent's visible actions.

**4. Simulation-Based Evaluation**

Evaluated agent performance through repeated simulated games, analyzing outcomes and identifying weaknesses in decision-making strategies.

**5. Iterative Experimentation**

Refined agent policies through competitive simulations, systematic failure analysis, and performance benchmarking.

## Results & Performance

The GoldCrusher agent was evaluated through head-to-head simulations against a reference opponent.

| Metric | Result |
|--------|--------|
| Agent | GoldCrusher |
| Environment | Jaipur (Bazaar-AI) |
| Primary Language | Python |
| Learning Approach | Reinforcement Learning & Evolutionary Optimization |
| Win Rate | 70%+ |
| Performance Improvement | 20+ percentage points over reference agent |
| Evaluation | Simulated competitive gameplay |

These results demonstrate the effectiveness of iterative policy optimization and simulation-based evaluation for decision-making under imperfect information.

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Agent implementation and experimentation |
| Reinforcement Learning | Reward-based strategy improvement |
| Evolutionary Optimization | Iterative policy and strategy refinement |
| Game Theory | Competitive decision-making under uncertainty |
| Bazaar-AI | Jaipur game simulation and agent evaluation |
| Arelai | Underlying game framework |
| Simulation & Benchmarking | Strategy evaluation and performance analysis |

## Repository Structure

The repository contains both the Bazaar-AI simulation framework and the custom GoldCrusher agent.

```text
Jaipur-AI-Agent/
│
├── agents/
│   ├── goldcrusher/       # Custom GoldCrusher AI agent
│   └── ...                # Other agents and reference strategies
│
├── src/                   # Bazaar-AI simulator source code
│
├── launch-bazaar-ai.py    # Simulator launcher
├── launch-bazaar-ai.sh    # Linux/macOS launcher
├── launch-bazaar-ai.bat   # Windows launcher
│
├── README.md
└── ...
```

**Note:** The GoldCrusher implementation is located under `agents/goldcrusher/`. The surrounding game engine and simulator are based on Chandra Gummaluru's Bazaar-AI framework.

## Simulation Environment: Bazaar-AI

This project uses [Bazaar-AI](https://github.com/chandra-gummaluru/bazaar-ai), a Python-based Jaipur simulation environment built on top of [Arelai](https://github.com/chandra-gummaluru/arelai).

The framework provides:

- A complete implementation of Jaipur's game mechanics and rules.
- A customizable agent interface for developing competing strategies.
- Serializable game states suitable for reinforcement learning experiments.
- Support for custom reward functions and simulation-based training.
- A visual web-based simulator for observing agents compete.
- Tools for evaluating gameplay decisions and comparing agent strategies.

### Visual Simulator

The simulator allows users to observe matches between AI agents and analyze their decision-making processes.

<p align="center">
  <a href="https://chandra-gummaluru.github.io/2025-12-29/bazaar-ai">
    <img src="https://github.com/chandra-gummaluru/bazaar-ai/blob/main/bazaar-demo-gif.gif?raw=true" alt="Bazaar-AI Jaipur Game Simulator Demo" width="100%" />
  </a>
</p>

*Simulator visualization from the original Bazaar-AI project by Chandra Gummaluru.*

The simulator supports:

- Visualizing game states and agent decisions.
- Watching competitive matches between AI agents.
- Comparing gameplay strategies.
- Examining individual actions and their outcomes.
- Identifying strategy weaknesses for further optimization.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/RishikaSinghal/Jaipur-AI-Agent.git
cd Jaipur-AI-Agent
```

### 2. Launch the Simulator

**macOS / Linux:**

```bash
bash launch-bazaar-ai.sh
```

**Windows:**

```bash
.\launch-bazaar-ai.bat
```

The launcher starts the local Bazaar-AI simulation environment.

### 3. Explore the GoldCrusher Agent

Navigate to the `agents/` directory to find the custom GoldCrusher implementation.

```bash
cd agents
```

The agent follows the Bazaar-AI framework's interface for selecting actions and receiving game feedback.

### 4. Run Simulations

Use the Bazaar-AI simulator to run games between available agents and compare their behavior.

The simulation environment can be used to inspect strategic decisions, evaluate performance, and identify opportunities for further agent optimization.

## Research Motivation

Imperfect-information games provide a valuable environment for investigating intelligent decision-making under uncertainty.

Jaipur captures several challenges relevant to real-world AI applications:

- Making decisions with incomplete information.
- Balancing immediate gains with long-term objectives.
- Adapting strategies in competitive environments.
- Optimizing policies through feedback and experimentation.
- Evaluating autonomous systems through reproducible simulations.

These challenges are closely related to broader applications in reinforcement learning, sequential decision-making, and autonomous agents.

## Future Improvements

Potential areas for further exploration include:

- Deep reinforcement learning for more complex policy representations.
- Monte Carlo Tree Search and planning-based approaches.
- Opponent modeling and adaptive strategy selection.
- Larger-scale benchmarking across diverse competing agents.
- Improved reward shaping and automated hyperparameter optimization.
- Enhanced visualization of action selection and learning performance.

## Acknowledgements & Attribution

This project was developed as part of an academic exploration of **game theory, reinforcement learning, and intelligent decision-making**.

### GoldCrusher Agent

The GoldCrusher AI agent, learning experiments, strategy optimization, and performance evaluation were developed as part of the Jaipur AI agent project.

### Bazaar-AI Framework

The underlying Jaipur game simulation environment is based on **Bazaar-AI**, created by **Chandra Gummaluru**.

- [Bazaar-AI — Original Repository](https://github.com/chandra-gummaluru/bazaar-ai)
- [Arelai — Underlying Framework](https://github.com/chandra-gummaluru/arelai)
- [Bazaar-AI — Simulator Demo](https://chandra-gummaluru.github.io/2025-12-29/bazaar-ai)

Credit for the original simulator, core game implementation, and agent framework belongs to their respective authors.

The GoldCrusher agent is a custom implementation built on top of this existing environment.
