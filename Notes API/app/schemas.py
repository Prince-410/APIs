from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class NoteBase(BaseModel):
    """Base Pydantic model for Note shared attributes."""
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="The title of the note.",
        examples=["Meeting Notes"]
    )
    content: str = Field(
        ...,
        min_length=1,
        description="The content body of the note.",
        examples=["Discuss project timeline and deliverables."]
    )


class NoteCreate(NoteBase):
    """Request payload schema for creating a new Note."""
    pass


class NoteUpdate(BaseModel):
    """Request payload schema for updating an existing Note (partial updates allowed)."""
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Updated title of the note.",
        examples=["Updated Meeting Notes"]
    )
    content: Optional[str] = Field(
        None,
        min_length=1,
        description="Updated content body of the note.",
        examples=["Updated details about deliverables."]
    )


class NoteResponse(NoteBase):
    """Response schema for returning a Note object."""
    id: int = Field(..., description="Unique identifier for the note.")
    created_at: datetime = Field(..., description="Timestamp when the note was created.")
    updated_at: datetime = Field(..., description="Timestamp when the note was last updated.")

    model_config = ConfigDict(from_attributes=True)
