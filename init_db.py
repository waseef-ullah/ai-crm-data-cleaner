from app.database import engine
from app import models
print('Creating tables...')
models.Base.metadata.create_all(bind=engine)
print('Done.')
