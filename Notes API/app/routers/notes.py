from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.post(
    "/",
    response_model=schemas.NoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note",
    description="Creates a new note with a title and content body.",
)
def create_note_endpoint(
    note: schemas.NoteCreate, db: Session = Depends(get_db)
):
    """
    Create a new note in the database.
    """
    return crud.create_note(db=db, note_data=note)


@router.get(
    "/",
    response_model=List[schemas.NoteResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all notes",
    description="Retrieves a paginated list of all notes.",
)
def read_notes_endpoint(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of items to return"),
    db: Session = Depends(get_db),
):
    """
    Retrieve all notes with pagination support (skip & limit).
    """
    return crud.get_notes(db=db, skip=skip, limit=limit)


@router.get(
    "/{note_id}",
    response_model=schemas.NoteResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a note by ID",
    description="Retrieves details of a specific note by its ID.",
)
def read_note_endpoint(note_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific note by ID.
    """
    db_note = crud.get_note(db=db, note_id=note_id)
    if db_note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with ID {note_id} not found",
        )
    return db_note


@router.put(
    "/{note_id}",
    response_model=schemas.NoteResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a note",
    description="Updates the title and/or content of an existing note.",
)
def update_note_endpoint(
    note_id: int, note_data: schemas.NoteUpdate, db: Session = Depends(get_db)
):
    """
    Update a note by ID.
    """
    updated_note = crud.update_note(db=db, note_id=note_id, note_data=note_data)
    if updated_note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with ID {note_id} not found",
        )
    return updated_note


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note",
    description="Deletes a specific note by its ID.",
)
def delete_note_endpoint(note_id: int, db: Session = Depends(get_db)):
    """
    Delete a note by ID.
    """
    deleted = crud.delete_note(db=db, note_id=note_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with ID {note_id} not found",
        )
    return None
