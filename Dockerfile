#FROM asr/offline:191023
#FROM asr/offline:191114
#FROM asr/offline:191120
#FROM asr/offline:191202
#FROM asr/offline:191220
FROM asr/offline:200120

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app
COPY requirements.txt /usr/src/app/

## using python3.6
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y apt-utils
RUN apt -y install software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt update && apt-get -qq -y install \
    python3.6 \
    python3.6-dev \
    python3.6-tk \
    python3-pip \
    python3-chardet \
    python3-requests \
    python3-six \
    python3-urllib3

RUN python3.6 -m pip install -U pip
RUN python3.6 -m pip install -r requirements.txt
