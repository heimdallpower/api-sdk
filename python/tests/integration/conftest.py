import os
import pytest
from heimdall_api_client import HeimdallApiClient


@pytest.fixture(scope="session")
def api_client():
    return HeimdallApiClient(
        client_id=os.environ["HEIMDALL_CLIENT_ID"], client_secret=os.environ["HEIMDALL_CLIENT_SECRET"]
    )
