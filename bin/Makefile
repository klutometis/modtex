COM=PYTHONPATH=../build/lib ./modtex

all:

build:
	cd ..;\
	python setup.py clean build

start: build
	sudo bash -c "${COM} start"

start-debug: build
	sudo bash -c "${COM}-debug start"

stop: build
	sudo bash -c "${COM} stop"

restart:
	sudo apachectl stop;\
	sudo modtex stop;\
	cd ..;\
	sudo rm -frv build;\
	sudo rm -frv /usr/local/lib/python2.5/site-packages/modtex;\
	python setup.py build;\
	sudo python setup.py install;\
	sudo modtex start;\
	sudo apachectl start;\
	sudo tail -f /usr/local/apache2/logs/error_log
