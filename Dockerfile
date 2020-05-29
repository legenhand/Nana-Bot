# We're using Alpine stable
FROM alpine:edge

# We have to uncomment Community repo for some packages
RUN sed -e 's;^#http\(.*\)/v3.9/community;http\1/v3.9/community;g' -i /etc/apk/repositories

# Installing Required Packages
RUN apk add --no-cache=true --update \
    bash \
    build-base \
    bzip2-dev \
    curl \
    figlet \
    gcc \
    git \
    sudo \
    util-linux \
    chromium \
    chromium-chromedriver \
    jpeg-dev \
    libffi-dev \
    libpq \
    libwebp-dev \
    libxml2 \
    libxml2-dev \
    libxslt-dev \
    linux-headers \
    musl \
    neofetch \
    openssl-dev \
    php-pgsql \
    postgresql \
    postgresql-client \
    postgresql-dev \
    py-lxml \
    py-pillow \
    py-pip \
    py-requests \
    py-sqlalchemy \
    py-tz \
    py3-aiohttp \
    openssl \
    pv \
    jq \
    wget \
    python3 \
    python3-dev \
    readline-dev \
    sqlite \
    sqlite-dev \
    sudo \
    zlib-dev \
    ffmpeg \
    curl-dev \
    libressl-dev \
    nodejs \
    npm \
    udev \
    ttf-freefont

# Setting up ENV Path for Chrom-bin and Chrome-Path
ENV CHROME_BIN=/usr/bin/chromium-browser

# Pypi package Repo upgrade
RUN pip3 install --upgrade pip setuptools
RUN apk --no-cache add build-base

# carbon.now.sh installation
RUN sudo npm install -g carbon-now-cli --unsafe-perm=true --allow-root

# Added Database Postgres
RUN apk --no-cache add postgresql-dev

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
