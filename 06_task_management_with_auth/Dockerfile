FROM python

WORKDIR /code

RUN apt-get update

COPY pyproject.toml uv.lock /code/

RUN pip install --no-cache-dir uv

COPY . ./code

RUN uv sync --frozen

EXPOSE 8000

LABEL APP_NAME="Task_management" AUTHOR="Mustafa Tawab"

CMD [ "uv", "run" , "uvicorn" , "main:app" ,"--host" , "0.0.0.0" ,"--port" , "8000", "--reload" ]