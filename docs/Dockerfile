# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

FROM python:3.6-slim

RUN pip install pdoc3

ARG userid
ENV userid=${userid}

RUN groupadd -r container_user && useradd --no-log-init -u ${userid} -m -r -g container_user container_user

RUN mkdir /app && chown container_user:container_user /app
WORKDIR /app

COPY --chown=container_user:container_user ./docs/entrypoint.sh /entrypoint.sh
COPY --chown=container_user:container_user . /app
USER container_user

ENTRYPOINT ["/entrypoint.sh"]