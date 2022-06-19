import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


def create_database_engine(
        user, database_name, host='', password='', echo=False
):
    return create_async_engine(
        f"postgresql+asyncpg://{user}:{password}"
        f"@{host}/{database_name}",
        echo=echo,
        future=True,
        pool_size=20,
        max_overflow=10
    )


Engine = create_database_engine(
    user=os.environ.get('DB_USER'),
    database_name=os.environ.get('DB_NAME'),
    host=os.environ.get('DB_HOST'),
    password=os.environ.get('DB_PASSWORD'),
    echo=False
)

Session = sessionmaker(Engine, expire_on_commit=False, class_=AsyncSession)
