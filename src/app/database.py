#DATABASE_URL = "sqlite:///./fastapi.db"
#DATABASE_URL = "postgresql://postgres:password@localhost/fastapidb"

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import Config

Base = declarative_base()

class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None
    def __getattr__(self, name):
        return getattr(self._session, name)
    def init(self):
        self._engine = create_async_engine(
            Config.DB_CONFIG,
            future = True,
            echo = True
        )
        #self._engine = create_async_engine("sqlite:///./fastapi.db",echo=True,future=True)
        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )()
    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

db = AsyncDatabaseSession()