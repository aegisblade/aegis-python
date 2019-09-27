# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

FROM python:2.7-slim

RUN pip install twine wheel

WORKDIR /app


ARG userid
ENV userid=${userid}

RUN echo hey ${userid}

RUN groupadd -r container_user && useradd --no-log-init -u ${userid} -m -r -g container_user container_user

COPY --chown=container_user:container_user ./publish.sh /publish.sh
USER container_user

ENTRYPOINT ["/publish.sh"]