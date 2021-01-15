FROM python:3.8-slim-buster

# Select workdir
WORKDIR /usr/src/personal-bot

# Copy Source code
COPY . .

# Labels
LABEL maintainer = "dearrude@tfwno.gf"

# Install dependency
RUN pip install poetry
RUN poetry install --no-dev

# Run scheduled
CMD [ "poetry", "run", "python3", "./src/main.py" ]
