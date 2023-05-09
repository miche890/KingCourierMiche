import pytest
from KingCourier import settings

@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test',
        'ATOMIC_REQUESTS': True,
    }