FROM python:3.13-alpine
WORKDIR .
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY . .
CMD ["fastapi", "run", "main.py", "--port", "80"]