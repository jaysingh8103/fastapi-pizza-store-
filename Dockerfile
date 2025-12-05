
FROM python:3.12-slim


WORKDIR /app


RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .


RUN pip install -e .


RUN mkdir -p /app/data


ENV DB_PATH=/app/data/pizza_store.sqlite
ENV PYTHONUNBUFFERED=1


RUN python -c "from main.database import initialize_database; initialize_database()"


EXPOSE 8000


CMD ["uvicorn", "main.api:app", "--host", "0.0.0.0", "--port", "8000"]