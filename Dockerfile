FROM archlinux

ENV PIP_NO_CACHE_DIR 1

WORKDIR /app/

# Installing Required Packages
RUN pacman -Syu --noconfirm \
    curl \
    git \
    libffi \
    libjpeg-turbo \
    libjpeg6-turbo \
    libwebp \
    python-lxml \
    postgresql \
    python-psycopg2 \
    libpqxx \
    libxml2 \
    libxslt \
    python-pip \
    python-sqlalchemy \
    openssl \
    wget \
    python \
    readline \
    libyaml \
    gcc \
    zlib \
    ffmpeg \
    libxi \
    unzip \
    libopusenc \
    && rm -rf /var/cache/pacman/pkg /tmp

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip3 install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

# remove readme to avoid ban
RUN rm README.md

# Starting Worker
CMD ["python3","-m","nana"]