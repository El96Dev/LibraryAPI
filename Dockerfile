FROM python:3.12
ENV PYTHONUNBUFFERED=1
COPY ./requirements.txt /app/requirements.txt
COPY ./app /app
WORKDIR /app
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt