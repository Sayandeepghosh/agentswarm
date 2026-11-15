import time
import uuid
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskStep(BaseModel):
    task_id: str
    description: str
    assigned_agent: str
    status: TaskStatus = TaskStatus.PENDING
    output: Optional[Any] = None
    retry_count: int = 0
    max_retries: int = 2

class AgentMessage(BaseModel):
    sender: str
    recipient: str
    content: str
    timestamp: float = Field(default_factory=time.time)

class AgentState(BaseModel):
    mission_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    mission_goal: str
    plan: List[TaskStep] = Field(default_factory=list)
    current_step_idx: int = 0
    context_store: Dict[str, Any] = Field(default_factory=dict)
    messages: List[AgentMessage] = Field(default_factory=list)
    quality_score: float = 0.0
    critic_feedback: str = ""
    is_approved: bool = False
    final_report: Optional[str] = None
    iteration_count: int = 0
    max_iterations: int = 6

    def add_message(self, sender: str, recipient: str, content: str) -> None:
        self.messages.append(AgentMessage(sender=sender, recipient=recipient, content=content))
