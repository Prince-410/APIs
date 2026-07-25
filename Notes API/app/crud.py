from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app import models, schemas


def create_note(db: Session, note_data: schemas.NoteCreate) -> models.Note:
    """
    Creates a new Note record in the database.
    """
    db_note = models.Note(
        title=note_data.title,
        content=note_data.content,
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_notes(db: Session, skip: int = 0, limit: int = 100) -> List[models.Note]:
    """
    Retrieves a list of notes with optional pagination.
    """
    return db.query(models.Note).offset(skip).limit(limit).all()


def get_note(db: Session, note_id: int) -> Optional[models.Note]:
    """
    Retrieves a single note by its ID.
    """
    return db.query(models.Note).filter(models.Note.id == note_id).first()


def update_note(
    db: Session, note_id: int, note_data: schemas.NoteUpdate
) -> Optional[models.Note]:
    """
    Updates an existing note's fields if provided.
    Also explicitly updates updated_at timestamp.
    """
    db_note = get_note(db, note_id=note_id)
    if not db_note:
        return None

    # Exclude unset fields for partial updates
    update_data = note_data.model_dump(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            setattr(db_note, field, value)
        db_note.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_note)

    return db_note


def delete_note(db: Session, note_id: int) -> bool:
    """
    Deletes a note by its ID. Returns True if deleted, False if not found.
    """
    db_note = get_note(db, note_id=note_id)
    if not db_note:
        return False

    db.delete(db_note)
    db.commit()
    return True
