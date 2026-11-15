import logging
import time
from typing import Dict, Any, Callable, List, Optional, Tuple
from .state import AgentState

logger = logging.getLogger(__name__)

END = "__END__"

class ExecutionTrace:
    def __init__(self, mission_id: str):
        self.mission_id = mission_id
        self.steps: List[Dict[str, Any]] = []
        self.start_time = time.perf_counter()
        self.end_time: Optional[float] = None

    def log_node_execution(self, node_name: str, duration_ms: float, state_snapshot: Dict[str, Any]):
        self.steps.append({
            "node": node_name,
            "duration_ms": duration_ms,
            "iteration": state_snapshot.get("iteration_count", 0),
            "approved": state_snapshot.get("is_approved", False),
            "quality_score": state_snapshot.get("quality_score", 0.0)
        })

    def finish(self):
        self.end_time = time.perf_counter()

    @property
    def total_duration_ms(self) -> float:
        if self.end_time is None:
            return round((time.perf_counter() - self.start_time) * 1000, 2)
        return round((self.end_time - self.start_time) * 1000, 2)

class StateGraph:
    """Cyclic StateGraph orchestration engine with conditional edge routing."""

    def __init__(self, entry_point: str):
        self.entry_point = entry_point
        self.nodes: Dict[str, Callable[[AgentState], AgentState]] = {}
        self.edges: Dict[str, str] = {}
        self.conditional_edges: Dict[str, Tuple[Callable[[AgentState], str], Dict[str, str]]] = {}

    def add_node(self, name: str, action: Callable[[AgentState], AgentState]) -> None:
        self.nodes[name] = action

    def add_edge(self, from_node: str, to_node: str) -> None:
        self.edges[from_node] = to_node

    def add_conditional_edge(
        self,
        from_node: str,
        condition: Callable[[AgentState], str],
        branch_map: Dict[str, str]
    ) -> None:
        self.conditional_edges[from_node] = (condition, branch_map)

    def execute(self, state: AgentState) -> Tuple[AgentState, ExecutionTrace]:
        trace = ExecutionTrace(state.mission_id)
        current_node_name = self.entry_point

        while current_node_name != END:
            if state.iteration_count >= state.max_iterations:
                logger.warning(f"Swarm reached max iterations budget ({state.max_iterations}). Forcing termination.")
                break

            if current_node_name not in self.nodes:
                raise KeyError(f"Graph node '{current_node_name}' is not registered.")

            node_fn = self.nodes[current_node_name]
            node_start = time.perf_counter()
            state.iteration_count += 1

            # Execute node function
            state = node_fn(state)
            node_duration = round((time.perf_counter() - node_start) * 1000, 2)
            trace.log_node_execution(current_node_name, node_duration, state.model_dump())

            # Determine next node
            if current_node_name in self.conditional_edges:
                condition_fn, branch_map = self.conditional_edges[current_node_name]
                branch_key = condition_fn(state)
                if branch_key not in branch_map:
                    raise KeyError(f"Conditional branch '{branch_key}' not mapped for node '{current_node_name}'")
                current_node_name = branch_map[branch_key]
            elif current_node_name in self.edges:
                current_node_name = self.edges[current_node_name]
            else:
                current_node_name = END

        trace.finish()
        return state, trace
