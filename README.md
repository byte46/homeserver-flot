# homeserver-flot
Homeserver RRD data output using flot.

##Installation
- # sudo apt-get install nodejs-legacy npm
- # sudo npm install -g bower
- клонировать репозиторий, перейти в каталог проекта.
- # bower install
- # ./debug.sh

##Usage
- # python rrd_parse.py -h ;-)
- В качестве wsgi-сервера:
 - python rrd_parse.py -d
 - Отправлять запросы вида: http://localhost:8000/rrd/?filename=data.rrd&exclude=1&exclude=2
