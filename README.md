# homeserver-plot
Homeserver RRD data output using plot.

##Installation
- # sudo apt-get install npm
- # sudo npm install -g bower
- клонировать репозиторий, перейти в каталог проекта.
- # bower install
- # ./debug.sh

##Usage
- # python rrd_parse.py -h ;-)
- В качестве wsgi-сервера:
 - python rrd_parse.py -d
 - Отправлять запросы вида: http://localhost:8000/rrd/?filename=data.rrd&exclude=1&exclude=2
