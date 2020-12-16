FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
<<<<<<< HEAD
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
=======
EXPOSE $PORT
ENTRYPOINT [ "python3" ]
CMD ["app.py"]
>>>>>>> 26eadf9252494327576d3b3f063873d84dd05bff
