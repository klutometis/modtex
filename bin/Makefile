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
	sudo python setup.py install;\
	sudo modtex start;\
	sudo apachectl start
