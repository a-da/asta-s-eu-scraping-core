ARG CIUR_VERSION=0.2.2.dev8

FROM adan/ciur:${CIUR_VERSION}

ARG ASTA_S_EU_SCRAPING_CORE_VERSION=0.0.2

ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install asta_s_eu_scraping_core==${ASTA_S_EU_SCRAPING_CORE_VERSION} || true

# validate
# RUN set -x && ciur --version | grep -qF "${CIUR_VERSION}"
