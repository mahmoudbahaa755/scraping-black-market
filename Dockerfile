FROM tiangolo/uvicorn-gunicorn:python3.11

RUN pip install fastapi uvicorn
COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "15400"]
