from psycopg_pool import ConnectionPool
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/appdb",
)

pool = ConnectionPool(
    conninfo=DATABASE_URL,
    min_size=1,
    max_size=10,
    open=False,  # don't connect until startup
)   ## This can probably go away!


### Models

## models go here Jay!!

## Also Jay, for security reasons (and because fuck numbers) I'd like to use UUIDv4 (built into postgres) for ALL primary keys through the database
## I am aware taht there are some performance impacts but id prefer to use uuids for the sole fact that they can more readily be exposed to a public facing audience.

## Toodle doo!
## _ Joel