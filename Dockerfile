# We're using Alpine stable
FROM alpine:edge

#
# We have to uncomment Community repo for some packages
#
RUN sed -e 's;^#http\(.*\)/v3.9/community;http\1/v3.9/community;g' -i /etc/apk/repositories

# Installing Python
RUN apk add --no-cache --update \
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
    python-dev \
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
    libcurl4-openssl-dev \
    libssl-dev \

RUN pip3 install --upgrade pip setuptools
RUN apk --no-cache add build-base
RUN apk --no-cache add postgresql-dev
RUN python3 -m pip install psycopg2

# Copy Python Requirements to /root/nana

RUN git clone https://github.com/legenhand/Nana-Bot.git /root/nana
WORKDIR /root/nana

#Copy config file to /root/nana/nana
COPY ./nana/config.example.py ./nana/config.py* /root/nana/nana/

#Copy credentials google drive to /root/nana
COPY ./README.md ./client_secrets.json* /root/nana/

ENV PATH="/home/userbot/bin:$PATH"

# Added Database Postgres

#
# Install requirements
#
RUN sudo pip3 install -r requirements.txt
CMD ["python3","-m","nana"]
