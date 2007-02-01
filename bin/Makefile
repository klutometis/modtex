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
