import pytest
from datetime import datetime

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    config.option.htmlpath = './reports/test_report_' + datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + '.html'