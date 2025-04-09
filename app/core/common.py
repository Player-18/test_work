# from os import getenv


# def get_database_url() -> str:
#     """Получить ссылку на базу."""
#     user = getenv("DB_USER", "postgres")
#     name = getenv("DB_NAME")
#     password = getenv("DB_PASS")
#     host = getenv("DB_HOST")
#     port = getenv("DB_PORT")
#
#     url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"
#
#     return url
