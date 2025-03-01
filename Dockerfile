FROM python:3.13-alpine
WORKDIR .
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY . .
EXPOSE 80
EXPOSE 5432
CMD ["fastapi", "run", "main.py", "--port", "80"]