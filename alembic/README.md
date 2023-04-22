Generic single-database configuration.

## Setting up connection data variables

Unix:
``` bash
export DB_USER=... 
export DB_PASS=...
export DB_HOST=...
```

Windows:
``` powershell
$env:DB_USER = '...'
$env:DB_PASS = '...'
$env:DB_HOST = '...' 
```

Replace three dots with the respective database connection data.

## Installing and using alembic

``` sh
poetry install
poetry shell
alembic ...
```

## Making revisions

To make a new revision run the following command in your terminal:
``` sh
alembic revision --autogenerate -m "revision message"
```

## Applying migrations

To apply migrations run the following command in your terminal:
``` sh
alembic upgrade head
```
