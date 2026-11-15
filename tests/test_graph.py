from agentswarm.state import AgentState
from agentswarm.agents import create_market_intelligence_swarm

def test_market_intelligence_swarm_execution():
    swarm = create_market_intelligence_swarm()
    initial_state = AgentState(mission_goal="Enterprise Retrieval Systems")

    final_state, trace = swarm.execute(initial_state)

    assert final_state.is_approved is True
    assert final_state.quality_score >= 85.0
    assert final_state.final_report is not None
    assert "Executive Market Intelligence Briefing" in final_state.final_report
    assert len(trace.steps) >= 5
    assert trace.total_duration_ms > 0
