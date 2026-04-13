FROM python:3.12-alpine

WORKDIR /code

COPY . .

RUN pip install uv && uv sync

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0"]