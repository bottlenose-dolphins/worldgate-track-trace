FROM python:3.11

#cx-Oracle fails to install via alpine (smaller image)
# FROM python:3.12.0a4-alpine3.17

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV TZ="Asia/Singapore"
# ENV SQLALCHEMY_DATABASE_URI=<DB URI>
ENV PYTHONPATH="${PYTHONPATH}:."

EXPOSE 5000

# start the server
CMD [ "python", "./app/user.py" ]