from sqlmodel import SQLModel, Field, Column
from typing import Optional
from enum import Enum
from datetime import datetime, timedelta
from sqlalchemy import DateTime, func
from pydantic import field_validator, BaseModel

class TaskStatus(str, Enum):
    pending = 'pending'
    in_progress = 'in_progress'
    completed = 'completed'
    cancelled = 'cancelled'

class TaskPriority(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'
    urgent = 'urgent'

class TaskBase(SQLModel):
    title: str = Field(max_length=200, index=True)
    description: Optional[str] = Field(default=None ,max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.pending)
    priority: TaskPriority = Field(default=TaskPriority.medium)
    due_date: Optional[datetime] = Field(default_factory=lambda: datetime.now() + timedelta(days=3))
    assigned_to: Optional[str] = Field(max_length=100, default=None)

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field( 
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now()
        ))

class TaskValidationMixin:
    @field_validator('title')
    @classmethod
    def empty_title(cls, title):
        title = title.strip()
        if not title:
            raise ValueError("Title must not be empty or whitespaced")
        return title

    @field_validator('due_date', mode='before')
    @classmethod
    def future_date(cls, date):
        if date is not None and date <= datetime.now():
            raise ValueError("Due date must be in the future")
        return date
    
class CreateTask(TaskValidationMixin, TaskBase):
    pass

class TaskUpdate(TaskValidationMixin, SQLModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None
    assigned_to:  str | None = None

    
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 
