FROM python:3.8-slim

# to prevent python from copying pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# to log the python output in terminal
ENV PYTHONUNBUFFERED 1

# Move code to work dir
RUN mkdir /code
ADD requirements.txt /code/
ADD . /code/
WORKDIR /code

# Install dependencies
RUN pip install -r requirements.txt

