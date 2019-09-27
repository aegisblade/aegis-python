FROM python:3.6-slim

RUN pip install pdoc3

WORKDIR /app


ARG userid
ENV userid=${userid}

RUN echo hey ${userid}

RUN groupadd -r container_user && useradd --no-log-init -u ${userid} -m -r -g container_user container_user

COPY --chown=container_user:container_user ./entrypoint.sh /entrypoint.sh
USER container_user

ENTRYPOINT ["/entrypoint.sh"]