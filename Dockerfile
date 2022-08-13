FROM python:3.8-slim-buster

# Select workdir
WORKDIR /usr/src/personal-bot

# Install dependency
RUN apt update && apt upgrade -y
RUN apt install -y libraqm-dev
RUN pip install poetry

# Copy Source code
COPY pyproject.toml .
COPY poetry.lock .

# Labels
LABEL maintainer = "dearrude@tfwno.gf"
RUN poetry install --no-dev

COPY . .

# Run scheduled
CMD [ "poetry", "run", "python3", "./src/main.py" ]
