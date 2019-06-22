FROM python:3.7
MAINTAINER Sven Mark Hofstra
ENV PYTHONUNBUFFERED=1
ADD . /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD exec gunicorn groceryapp.wsgi:application --bind 0.0.0.0:5000 --workers 3