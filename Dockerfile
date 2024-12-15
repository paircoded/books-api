FROM python:3.12

WORKDIR /code
EXPOSE 80

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY ./olis ./olis
CMD ["poetry", "run", "fastapi", "run", "olis/main.py", "--port", "80"]
