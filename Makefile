# MiniCPS Makefile

# VARIABLES {{{1

LATEST_VERSION = 1.1.3
MININET = sudo mn

PYTHON = sudo python
PYTHON_OPTS =

# regex testMatch: (?:^|[b_.-])[Tt]est)
# --exe: include also executable files
# -s: don't capture std output
# nosetests -s tests/devices_tests.py:fun_name


# NOTE: sudo because of mininet
TESTER = sudo nosetests
TESTER_TRAVIS = nosetests
TESTER_OPTS = -s -v --exe  --rednose
TESTER_OPTS_COV_HTML = $(TESTER_OPTS) --with-coverage --cover-html

UPLOADER=twine
# }}}

.PHONY: tests tests-travis clean

# Matlab-Sc1 {{{1

matlab-sc1-init:
	cd examples/matlab-sc1; $(PYTHON) $(PYTHON_OPTS) init.py; cd ../..

matlab-sc1:
	cd examples/matlab-sc1; $(PYTHON) $(PYTHON_OPTS) run.py; cd ../..

test-matlab-sc1:
	cd examples/matlab-sc1; $(TESTER) $(TESTER_OPTS) tests.py; cd ../..

# }}}

# TESTS {{{1

# ALL {{{2
tests:
	$(TESTER) $(TESTER_OPTS) tests

# }}}

# MANUAL {{{2
test-mcps:
	$(TESTER) $(TESTER_OPTS) tests/mcps_tests.py

test-networks:
	$(TESTER) $(TESTER_OPTS) tests/networks_tests.py

test-sdns:
	$(TESTER) $(TESTER_OPTS) tests/sdns_tests.py


test-protocols:
	$(TESTER) $(TESTER_OPTS) tests/protocols_tests.py

test-enip:
	$(TESTER) $(TESTER_OPTS) tests/protocols_tests.py:TestEnipProtocol

test-modbus:
	$(TESTER) $(TESTER_OPTS) tests/protocols_tests.py:TestModbusProtocol


test-utils:
	$(TESTER) $(TESTER_OPTS) tests/utils_tests.py

test-states:
	$(TESTER) $(TESTER_OPTS) tests/states_tests.py


test-devices:
	$(TESTER) $(TESTER_OPTS) tests/devices_tests.py

test-device:
	$(TESTER) $(TESTER_OPTS) tests/devices_tests.py:TestDevice
# }}}

# TRAVIS {{{2
tests-travis:
	$(TESTER_TRAVIS) $(TESTER_OPTS) tests/protocols_tests.py
	$(TESTER_TRAVIS) $(TESTER_OPTS) tests/devices_tests.py
	$(TESTER_TRAVIS) $(TESTER_OPTS) tests/states_tests.py


# https://pypi.python.org/pypi/nose-cov/1.6
# FIXME: test cov
# report: term, term-missing, html, xml, annotate
# --cov set the covered FS
# test-cov:
# 	sudo $(TESTER) $(TESTER_OPTS_COV) minicps_tests.py
# }}}

# }}}

# CLEAN {{{1
clean: clean-cover clean-pyc clean-logs

clean-simulation:
	sudo pkill  -f -u root "python -m cpppo.server.enip"
	sudo mn -c

clean-cover:
	rm -f minicps/*,cover
	rm -f tests/*,cover

clean-pyc:
	rm -f minicps/*.pyc
	rm -f tests/*.pyc

clean-logs:
	rm -f logs/*.log

clean-cpppo:
	sudo pkill  -f -u root "python -m cpppo.server.enip"

clean-mininet:
	sudo mn -c

# }}}

# PYPI {{{1

pypi-wheel:
	./setup.py sdist bdist_wheel

pypi-upload:
	$(UPLOADER) upload dist/minicps-$(LATEST_VERSION)*

# }}}
