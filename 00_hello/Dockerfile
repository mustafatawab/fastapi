FROM python:3.12-alpine

WORKDIR /code

COPY pyproject.toml uv.lock ./


RUN pip install uv --no-cache-dir && uv sync

COPY main.py .

EXPOSE 8000

CMD ["uv" , "run" ,"uvicorn", "main:app" , "--reload" , "--port" , "8000" , "--host" , "0.0.0.0"]

