FROM python:3.9

WORKDIR /usr/src/app

RUN apt update &&  \
    apt install -y binutils libproj-dev gdal-bin && \
    pip install -U pip && \
    apt install -y curl netcat && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

COPY . .

ENV PATH="${PATH}:/root/.poetry/bin"



RUN poetry config virtualenvs.create false &&  \
    poetry install

RUN python manage.py collectstatic --noinput