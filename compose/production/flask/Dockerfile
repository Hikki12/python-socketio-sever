FROM python:3.9.0-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update \
    && apk add --no-cache gcc musl-dev linux-headers

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --upgrade pip
RUN pip install -r /requirements/production.txt


COPY ./compose/production/flask/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

# Configure an entrypoint
COPY ./compose/production/flask/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

WORKDIR /app
RUN echo $(ls)

ENTRYPOINT ["/entrypoint"]
