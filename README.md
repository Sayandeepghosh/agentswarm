# agentswarm

[![CI Tests](https://img.shields.io/badge/pytest-passing-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)]()
[![Architecture](https://img.shields.io/badge/Architecture-Cyclic%20StateGraph-purple.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

A lightweight, deterministic multi-agent state graph orchestration framework featuring cyclic execution, typed Pydantic state machines, AST-safe tool calling, and automated reflection.

---

## StateGraph Topology

```text
       ┌───────────────┐
       │ Planner Node  │ ── Deconstructs mission into typed TaskStep sequence
       └───────┬───────┘
               │
               ▼
       ┌───────────────┐
       │Researcher Node│ ── Fetches telemetry, competitor pricing & metrics
       └───────┬───────┘
               │
               ▼
       ┌───────────────┐
       │ Analyst Node  │ ── Executes CalculatorTool for CAGR & price percentiles
       └───────┬───────┘
               │
               ▼
       ┌───────────────┐
       │  Critic Node  │ ── Evaluates quality score against strict audit rubric
       └───────┬───────┘
               │
               ├─────────────────────────────────┐
       [Quality >= 85: Approved]         [Quality < 85: Reject]
               │                                 │
               ▼                                 ▼
       ┌───────────────┐                 (Cycles back to Researcher)
       │Synthesizer Node│
       └───────┬───────┘
               │
               ▼
             [END]
```

---

## Core Capabilities

- **Cyclic State Machine:** Directed state graphs supporting sequential and conditional edges with iteration budgets to prevent runaway recursion.
- **Typed State Management:** Centralized `AgentState` schema using Pydantic V2 ensuring immutability across transitions.
- **Safe Tool Registry:** AST-based expression evaluation (`CalculatorTool`) preventing code injection alongside HTML extraction tools (`WebFetcherTool`).
- **Audit & Reflection:** Critic nodes assign numerical quality scores (0-100) before gating downstream synthesis.

---

## Quickstart

```bash
git clone https://github.com/Sayandeepghosh/agentswarm.git
cd agentswarm

python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -e .
```

### Running a Mission
```bash
python -m agentswarm.cli "Autonomous AI Voice Agents in 2026"
```

Output:
```text
====================================================================
AgentSwarm Runtime | Initializing Swarm Mission
Goal: Autonomous AI Voice Agents in 2026
====================================================================

Execution Finished in 2.14 ms (5 graph steps).
  • Node: planner        | Duration:   0.12 ms | Quality: 0.0/100
  • Node: researcher     | Duration:   0.14 ms | Quality: 0.0/100
  • Node: analyst        | Duration:   0.62 ms | Quality: 0.0/100
  • Node: critic         | Duration:   0.08 ms | Quality: 100.0/100
  • Node: synthesizer    | Duration:   0.31 ms | Quality: 100.0/100

Report written to: reports/market_intelligence_report.md
```

---

## Test Suite

```bash
pytest tests/ -v
```

---

## License
MIT
