ARG PYTHON_VERSION=3.13.2

FROM python:${PYTHON_VERSION}
ARG CIUR_VERSION=0.2.2

ENV PIP_ROOT_USER_ACTION=ignore
RUN echo "_pip install ciur==${CIUR_VERSION}_" > 1.log
RUN pip install ciur==${CIUR_VERSION} || true

# validate
# RUN set -x && ciur --version | grep -qF "${CIUR_VERSION}"
