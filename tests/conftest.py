import os
from unittest import mock

mock.patch.dict(os.environ, {
    'ADA_CHROME_DEBUGGER_ADDRESS_PORT': 'MOCKED_PORT_VALUE'
}).start()
