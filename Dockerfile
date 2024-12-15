FROM python:3.12

WORKDIR /code
EXPOSE 80

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY ./books_api ./books_api
CMD ["poetry", "run", "fastapi", "run", "books_api/main.py", "--port", "80"]
