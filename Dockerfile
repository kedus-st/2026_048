#FROM osgeo/gdal:latest
FROM python:3.10.2
ENV PYTHONBUFFERED 1

WORKDIR /app

RUN apt-get update
RUN apt-get install -y python3 python3-dev pip libpq-dev gdal-bin libgdal-dev libspatialindex-dev python3-distutils gcc gettext musl-dev libproj-dev proj-data proj-bin libgeos-dev supervisor

COPY requirements.txt .
RUN python3 -m pip install setuptools==57.5.0
RUN SETUPTOOLS_USE_DISTUTILS=stdlib
RUN python3 -m pip install numpy
RUN python3 -m pip install cython
RUN python3 -m pip install -r requirements.txt

COPY . .
CMD ["/usr/bin/supervisord", "-c", "supervisord.conf"]
#CMD sh -c "celery -A management worker -l info & celery -A management beat -l info & python3 manage.py runserver 0.0.0.0:80"
#CMD sh -c "python3 manage.py runserver 0.0.0.0:80"