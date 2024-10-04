from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.types import Date
from app import db
from datetime import date, datetime

class User(db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True, nullable=False)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256), nullable=True)
    date_of_birth: so.Mapped[date] = so.mapped_column(sa.Date)
    gender: so.Mapped[str] = so.mapped_column(sa.String(20))
    height: so.Mapped[float] = so.mapped_column(sa.Float)
    initial_weight: so.Mapped[float] = so.mapped_column(sa.Float)
    phone_number: so.Mapped[str] = so.mapped_column(sa.String(30))

    # Relationships
    # The use of quotes around 'TrainingSession' allows for forward references
    training_sessions: so.Mapped[List['TrainingSession']] = so.relationship(
        'TrainingSession', back_populates='user', cascade='all, delete-orphan'
    )

class TrainingSession(db.Model):
    __tablename__ = 'training_sessions'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'), nullable=False)
    date: so.Mapped[date] = so.mapped_column(sa.Date, nullable=False)
    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, nullable=True)

    # Relationships
    user: so.Mapped['User'] = so.relationship('User', back_populates='training_sessions')
    training_details: so.Mapped[List['TrainingDetail']] = so.relationship(
        'TrainingDetail', back_populates='session', cascade='all, delete-orphan'
    )

class TrainingDetail(db.Model):
    __tablename__ = 'training_details'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    session_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('training_sessions.id'), nullable=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=False)
    serie: so.Mapped[int] = so.mapped_column(nullable=False)
    rep: so.Mapped[int] = so.mapped_column(nullable=False)
    kg: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    d: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, nullable=True)
    vm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, nullable=True)
    vmp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, nullable=True)
    rm: so.Mapped[Optional[int]] = so.mapped_column(nullable=True)
    p_w: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, nullable=True)
    perfil: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    ejercicio: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    ecuacion: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    atleta_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'), nullable=False)

    # Relationships
    session: so.Mapped['TrainingSession'] = so.relationship('TrainingSession', back_populates='training_details')
    atleta: so.Mapped['User'] = so.relationship('User')