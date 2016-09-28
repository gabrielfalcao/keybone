# Config
OSNAME			:= $(shell uname)

DEBIAN_FRONTEND		:= noninteractive
PYTHONUNBUFFERED	:= true

ifeq ($(OSNAME), Linux)
OPEN_COMMAND		:= gnome-open
OSDEPS			:= sudo apt-get update && sudo apt-get -y install python-dev libtool build-essential libev-dev libevent-dev redis-tools virtualenvwrapper
else
OPEN_COMMAND		:= open
OSDEPS			:= brew install redis libevent libev
endif

# all: tests html-docs

TZ				:= UTC
PYTHONPATH			:= $(shell pwd)
EASYGPG_LOGLEVEL			:= DEBUG
PATH				:= $(PATH):$(shell pwd)
KEYBONE_CONFIG_PATH		:= $(shell pwd)/tests/keybone.yml
executable			:= keybone
export TZ
export PATH
export PYTHONPATH
export EASYGPG_LOGLEVEL
export DEBIAN_FRONTEND
export PYTHONUNBUFFERED
export KEYBONE_CONFIG_PATH

all:
	python main.py

tests: lint unit functional

setup: os-dependencies ensure-dependencies

os-dependencies:
	$(OSDEPS)

lint:
	@printf "\033[1;33mChecking for static errors\033[0m\n"
	@find keybone -name '*.py' | grep -v node | xargs flake8 --ignore=E501

clean:
	git clean -Xdf

unit:
	nosetests tests/unit

functional:
	nosetests tests/functional

integration:
	keybone quickstart --force tests/keybone.yml
	keybone create "John Doe" john@doe.com --secret='foobar'
	keybone import "$$(cat https://stallman.org/rms-pubkey.txt)"
	keybone import "$(curl 'http://pgp.mit.edu/pks/lookup?op=get&search=0xEFAF4C707AED2EF2')"
	keybone decrypt --secret='foobar' "$$(keybone encrypt john@doe.com 'A Private Hello')"
	keybone list
	keybone backup > backup.keybone
	keybone wipe --no-backup --force
	keybone recover --force backup.keybone
	keybone list
	keybone private john@doe.com
	keybone public 0F6A146532D869AEE438F74B6211AA3B00411886
	keybone wipe --no-backup --force

tests: unit functional

prepare: remove
	ensure-dependencies

remove:
	-@pip uninstall -y keybone

ensure-dependencies:
	@pip install -U pip
	@CFLAGS='-std=c99' python setup.py develop
	@CFLAGS='-std=c99' pip install -r development.txt

release:
	@./.release
	@python setup.py sdist register upload

list:
	@$(executable) list

.PHONY: html-docs docs

html-docs:
	cd docs && make html

docs: html-docs
	$(OPEN_COMMAND) docs/build/html/index.html

graph-profile:
	for callgrind in `ls *.callgrind`; do echo processing $$callgrind; gprof2dot -w --show-samples --total=callstacks -f callgrind -o $$callgrind.dot $$callgrind; dot -Tpng $$callgrind.dot -o $$callgrind.png; done
	$(OPEN_COMMAND) *.callgrind.png
