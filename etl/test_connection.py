import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

url = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@127.0.0.1:5433/{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(url)

with engine.connect() as conn:
    print(conn.execute(text("SELECT version();")).scalar())