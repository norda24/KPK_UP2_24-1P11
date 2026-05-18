"""Модуль моделей базы данных для Work Program Service."""
import datetime
from peewee import SqliteDatabase, Model, CharField, DateTimeField, \
    ForeignKeyField, IntegerField, BooleanField, AutoField

db = SqliteDatabase('work_programs.db', pragmas={'foreign_keys': 1})


class BaseModel(Model):
    """Базовая модель для связи с SQLite."""

    class Meta:
        database = db


class WorkProgram(BaseModel):
    """Модель рабочих программ с проверкой уникальности названия и версии."""

    id = AutoField()
    title = CharField(null=False)
    file_path = CharField(null=False, unique=True)
    version = CharField(null=False, default="1.0")
    is_deleted = BooleanField(null=False, default=False)
    created_at = DateTimeField(default=datetime.datetime.now, null=False)

    class Meta:
        indexes = (
            (('title', 'version'), True),
        )


class ProgramAssignment(BaseModel):
    """Связь программ с внешними ID специальностей и дисциплин (3НФ)."""

    assignment_id = AutoField() 
    program = ForeignKeyField(
        WorkProgram,
        backref='assignments',
        on_delete='CASCADE',  
        column_name='work_program_id'
    )
    specialty_id = IntegerField(null=False)
    discipline_id = IntegerField(null=False)
    is_deleted = BooleanField(null=False, default=False)  

    class Meta:
        indexes = (
            (('program', 'specialty_id', 'discipline_id'), True), 
        )


def init_db():
    """Инициализация таблиц базы данных."""
    db.connect()
    db.create_tables([WorkProgram, ProgramAssignment])
    print("БД успешно инициализирована.")


if __name__ == "__main__":
    init_db()
