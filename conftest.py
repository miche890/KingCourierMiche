import pytest
from KingCourier import settings

@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = settings.DATABASES['test']