FROM python:3.7
ENV TZ=Europe/Moscow
COPY . /code
WORKDIR /code
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

