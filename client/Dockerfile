# pull official base image
FROM python:3.9.5-slim-buster


# set working directory and copy files over
WORKDIR /app
COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install packages
RUN pip3 install -r requirements.txt

EXPOSE 5000
#CMD flask run --cert=adhoc
#CMD ["gunicorn", "-w", "3", "-b", ":5000", "-t", "360", "--reload", "app:app"]
