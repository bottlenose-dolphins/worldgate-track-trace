FROM python:3.11

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV TZ="Asia/Singapore"
ENV SQLALCHEMY_DATABASE_URI
ENV PYTHONPATH="${PYTHONPATH}:."

EXPOSE 5001

# start the server
CMD [ "python", "./app/user.py" ]