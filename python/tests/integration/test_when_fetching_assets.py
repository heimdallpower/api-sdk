import pytest

@pytest.mark.integration
def test_should_return_valid_assets(api_client):
    assets = api_client.get_assets()
    assert assets is not None, "Assets should not be None"
    assert hasattr(assets, 'data'), "Assets should have a 'data' attribute"
    assert hasattr(assets.data, 'grid_owners'), "Assets data should have 'grid_owners' attribute"
    assert isinstance(assets.data.grid_owners, list), "Grid owners should be a list"
    assert len(assets.data.grid_owners) > 0, "There should be at least one grid owner"
