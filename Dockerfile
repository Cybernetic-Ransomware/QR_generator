FROM python:3.12
LABEL authors="AM"
WORKDIR /app
COPY requirements.txt ./

RUN python -m pip install --upgrade pip &&  \
    pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]

