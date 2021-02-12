"""
Shared fixtures for all tests
"""

import pytest


@pytest.fixture(autouse=True)
def prevent_http_requests(monkeypatch):
    """
    Raise an error if a http request is made in a test
    """

    def urlopen_mock(self, method, url, *args, **kwargs):
        raise RuntimeError(
            f"The test was about to {method} {self.scheme}://{self.host}{url}"
        )

    monkeypatch.setattr(
        "urllib3.connectionpool.HTTPConnectionPool.urlopen", urlopen_mock
    )
