FROM python:3.8

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

#RUN echo $(ls)

COPY . /app

ENV PYTHONUNBUFFERED=1

CMD ["python3", "main.py"]
