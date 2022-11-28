FROM python:3.11-slim
ARG JASECI_PYPI_VERSION
ARG JASECI_SERV_PYPI_VERSION
ARG JASECI_AI_KIT_PYPI_VERSION
ARG BUILD_WITH_AI
WORKDIR /
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update; apt -y upgrade; apt -y install --no-install-recommends git g++ build-essential pkg-config cmake
RUN pip3 install jaseci==$JASECI_PYPI_VERSION
RUN pip3 install jaseci-serv==$JASECI_SERV_PYPI_VERSION
RUN pip3 install numpy==1.23.5
RUN if [[ -n "$BUILD_WITH_AI" ]]; then pip3 install jaseci-ai-kit==$JASECI_AI_KIT_PYPI_VERSION; fi
CMD ["echo", "Ready"]
