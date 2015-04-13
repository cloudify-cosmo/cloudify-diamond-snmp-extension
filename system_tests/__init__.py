from pkgutil import extend_path

from cosmo_tester.framework.testenv import bootstrap, teardown

__path__ = extend_path(__path__, __name__)


def setUp():
    bootstrap()


def tearDown():
    teardown()
