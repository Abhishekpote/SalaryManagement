FROM python:3.12

RUN apt-get update && \
    apt-get install -y dos2unix && \
    apt-get clean

RUN mkdir app
WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY / .

COPY startup.sh .
RUN chmod +x startup.sh
RUN dos2unix startup.sh
EXPOSE 5000
CMD ["./startup.sh","start"]

# CMD ["alembic","upgrade","head"]
# CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]
# CMD ["mqttwarn" "--version"]