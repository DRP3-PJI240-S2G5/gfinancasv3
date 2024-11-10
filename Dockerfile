FROM python:3.11-slim

ENV APP_HOME=/app
WORKDIR ${APP_HOME}

# Install basic SO and Python
RUN apt-get update --fix-missing \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-traditional \
    wget curl vim locales zip unzip apt-utils \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir uWSGI==2.0.25.1 uwsgitop==0.12

# Replace shell with bash so we can source files
SHELL ["/bin/bash", "-c"]
RUN echo "export LS_OPTIONS='--color=auto'" >>~/.bashrc && \
    echo "eval "\`dircolors\`"" >>~/.bashrc && \
    echo "alias ls='ls \$LS_OPTIONS'" >>~/.bashrc && \
    echo "alias ll='ls \$LS_OPTIONS -l'" >>~/.bashrc && \
    echo "alias l='ls \$LS_OPTIONS -lA'" >>~/.bashrc

#### Prepare BACKEND Django API

COPY requirements.txt ./
COPY requirements-dev.txt ./

RUN pip install --no-cache-dir -r requirements-dev.txt

COPY ./docker/bin/entrypoint.sh ./docker/bin/
RUN sed -i 's/\r$//g' ${APP_HOME}/docker/bin/entrypoint.sh
# Adicionar permissão para o script de entrada
RUN chmod +x ${APP_HOME}/docker/bin/entrypoint.sh

ENV PYTHONUNBUFFERED=1 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONIOENCODING=UTF-8
ENV SHELL=/bin/bash LANG=en_US.UTF-8

# Gets the current git commit hash
ARG GIT_HASH
ENV GIT_HASH=$GIT_HASH

COPY . ./

# Comando de entrada
ENTRYPOINT ["/app/docker/bin/entrypoint.sh"]