from agentswarm.state import AgentState, TaskStep, TaskStatus

def test_agent_state_defaults():
    state = AgentState(mission_goal="Analyze AI Voice Agents")
    assert len(state.mission_id) == 8
    assert state.is_approved is False
    assert state.quality_score == 0.0

    state.add_message("planner", "worker", "Task dispatched")
    assert len(state.messages) == 1
    assert state.messages[0].sender == "planner"
