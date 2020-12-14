FROM python:alpine3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5500
ENTRYPOINT [ "python3" ]
CMD ["app.py"]