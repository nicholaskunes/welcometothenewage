# -*- coding: utf-8 -*-

import time
import requests
from pytz import utc
from datetime import datetime

import gdax


auth_client = gdax.AuthenticatedClient(key, b64secret, passphrase)
