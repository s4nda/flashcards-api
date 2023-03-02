import pytest


class TestSample:
    @classmethod
    def setup_class(cls):
        print("OVO JE PRE TESTA")

    def test_majmun(self):
        print("OVO JE TEST")
        assert True

    def test_majmun2(self):
        print("Ovo je drugi test")
        assert True

    def teardown_method(self, method):
        print("OVO je teardown -- posle testa")
