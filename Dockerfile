FROM python:3.10-slim

# Change working directory
WORKDIR /app/

# Copy project files
COPY . .

# Install deps
RUN pip install pipenv

RUN pipenv install --system --deploy --ignore-pipfile --dev

CMD sleep 5 \
    && python3 manage.py migrate \
    && python3 manage.py runserver 0.0.0.0:80
