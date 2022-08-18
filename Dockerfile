FROM python:3.10-slim-buster

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

# Install
COPY . .
RUN poetry install --no-dev


# Run scheduled
CMD [ "poetry", "run", "python3", "personal-bot/main.py" ]
