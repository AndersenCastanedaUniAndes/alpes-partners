FROM python:3.11

EXPOSE 8000

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /src

CMD ["uvicorn", "alpespartners.main:app", "--host", "0.0.0.0", "--port", "8000"]
