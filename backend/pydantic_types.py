from pydantic import BaseModel, Field


# Common Pydantic Types
class PaginationParams(BaseModel):
    page: int = Field(1, gt=0, description='Page number')
    page_size: int = Field(100, gt=0, description='Number of items per page')


class TaskProgressUpdateSubModel(BaseModel):
    type: str = Field(..., description='Type of update (e.g., "task_progress")')
    status: str = Field(..., description='Current status (e.g., "processing", "completed", "failed")')
    message: str = Field(..., description='Human-readable message')
    timestamp: str = Field(..., description='ISO timestamp of the update')
    data: dict|None = Field(default_factory=dict, description='Additional data for the update')


class SendTaskUpdateRequest(BaseModel):
    task_id: int = Field(..., description='The ID of the task to update')
    message: TaskProgressUpdateSubModel = Field(..., description='The progress update message to send to the task')
