from app.database import Base, engine
from app.models import Task

Base.metadata.create_all(engine)
print('таблицы созданы')