FROM python:3.8-slim

# to prevent python from copying pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# to log the python output in terminal
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/requirements.txt

WORKDIR /code
# Install dependencies
RUN pip install -r requirements.txt

# Move code to work dir
ADD . /code/
