import argparse
import os
import sys
from .state import AgentState
from .agents import create_market_intelligence_swarm

def main():
    parser = argparse.ArgumentParser(
        prog="agentswarm",
        description="AgentSwarm: Autonomous StateGraph multi-agent orchestration runtime."
    )
    parser.add_argument("goal", nargs="?", default="Conversational AI Voice Agents for Enterprise Customer Support")
    parser.add_argument("--out", "-o", default="reports/market_intelligence_report.md", help="Output file path")
    parser.add_argument("--max-iter", type=int, default=6, help="Maximum execution iterations")

    args = parser.parse_args()

    print("=" * 68)
    print(f"AgentSwarm Runtime | Initializing Swarm Mission")
    print(f"Goal: {args.goal}")
    print("=" * 68)

    swarm = create_market_intelligence_swarm()
    initial_state = AgentState(
        mission_goal=args.goal,
        max_iterations=args.max_iter
    )

    final_state, trace = swarm.execute(initial_state)

    print(f"\nExecution Finished in {trace.total_duration_ms} ms ({len(trace.steps)} graph steps).")
    for s in trace.steps:
        print(f"  • Node: {s['node']:<14} | Duration: {s['duration_ms']:>6.2f} ms | Quality: {s['quality_score']}/100")

    if final_state.final_report:
        os.makedirs(os.path.dirname(args.out), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(final_state.final_report)
        print(f"\nReport written to: {args.out}")
        print("\n--- Summary Preview ---\n")
        print("\n".join(final_state.final_report.splitlines()[:16]))
    else:
        print("\nMission failed to synthesize approved output.")
        sys.exit(1)

if __name__ == "__main__":
    main()
