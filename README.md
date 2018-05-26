Home Assistant
=============================================================

Home Assistant is a home automation platform running on Python 3. It is able to track and control all devices at home and offer a platform for automating control.

Installation
---------------------

Requirements:
docker.ce
bash
socat
jq
curl
avahi-daemon
dbus-daemon
python3-pip
python3-dev
python3-venv
libssl-dev
libxml2-dev
libxslt1-dev
libjpeg-dev
libffi-dev
libudev-dev
zlib1g-dev

$ git clone https://github.com/veresspeter/home-assistant.git
$ cd home-assistant
$ python3 -m venv .
$ source bin/activate
$ script/setup
$ docker build -t home-assistant .
$ mkdir /config
$ docker run -v /config:/config -v /etc/localtime:/etc/localtime:ro --net=host home-assistant

