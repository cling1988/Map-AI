FROM python:3.11-slim

RUN apt-get update

WORKDIR /

COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./app /app

EXPOSE 60001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "60001", "--workers", "2"]
