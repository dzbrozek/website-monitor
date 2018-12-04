import pytest

from errors import InvalidConfigError
from resource import MonitoredResource


@pytest.mark.parametrize("config,error", [
    (dict(), 'Missing config file.'),
    (dict(url=''), 'Invalid config file. The "url" section is missing.'),
    (dict(url='http://www.onet.pl/'), 'Invalid config file. The "schedule" section is missing.'),
    (dict(url='http://www.onet.pl/', schedule='* * *'),
     'Invalid config file. "* * *" is an invalid expression for the "schedule" section'),
    (dict(url='http://www.onet.pl/', schedule='* * * * *'),
     'Invalid config file. The "conditions" section is missing.'),
    (dict(url='http://www.onet.pl/', schedule='* * * * *', conditions=dict(status='')),
     'Invalid config file. The "conditions" section is invalid.')
])
def test_load_invalid_config(config, error):
    with pytest.raises(InvalidConfigError) as cm:
        MonitoredResource(config)

    assert str(cm.value) == error

