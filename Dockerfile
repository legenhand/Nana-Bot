# We're using Debian Slim Buster image
FROM python:3.8-slim-buster

ENV PIP_NO_CACHE_DIR 1

RUN sed -i.bak 's/us-west-2\.ec2\.//' /etc/apt/sources.list

# Installing Required Packages
RUN apt update && apt upgrade -y && \
    apt install --no-install-recommends -y \
    bash \
    bzip2 \
    curl \
    figlet \
    gcc \
    git \
    sudo \
    util-linux \
    chromium \
    libffi-dev \
    libjpeg-dev \
    libjpeg62-turbo-dev \
    libwebp-dev \
    linux-headers-amd64 \
    musl-dev \
    musl \
    neofetch \
    php-pgsql \
    postgresql \
    postgresql-client \
    postgresql-server-dev-10 \
    libxml2-dev \
    libxslt1-dev \
    python3-pip \
    python3-requests \
    python3-sqlalchemy \
    python3-tz \
    python3-aiohttp \
    openssl \
    pv \
    jq \
    wget \
    python3 \
    python3-dev \
    libreadline-dev \
    libyaml-dev \
    sqlite3 \
    libsqlite3-dev \
    sudo \
    zlib1g \
    ffmpeg \
    libssl-dev \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists /var/cache/apt/archives /tmp

# Setting up ENV Path for Chrom-bin and Chrome-Path
ENV CHROME_BIN=/usr/bin/chromium-browser

# Pypi package Repo upgrade
RUN pip3 install --upgrade pip setuptools
RUN apt install --no-install-recommends -y build-essential

# carbon.now.sh installation
RUN sudo npm install -g carbon-now-cli --unsafe-perm=true --allow-root

# Added Database Postgres
RUN apt install --no-install-recommends -y postgresql-server-dev-10

# Chromium Install
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true
ENV CHROMIUM_PATH /usr/bin/chromium-browser

# Copy Python Requirements to /root/nana
RUN git clone https://github.com/pokurt/Nana-Bot.git /root/nana
WORKDIR /root/nana

#Copy config file to /root/nana/nana
COPY ./nana/config.example.py ./nana/config.py* /root/nana/nana/

#Copy credentials google drive to /root/nana
COPY ./README.md ./client_secrets.json* /root/nana/

ENV PATH="/home/userbot/bin:$PATH"

# Install requirements
RUN sudo pip3 install -U -r requirements.txt

# Starting Worker
CMD ["python3","-m","nana"]
