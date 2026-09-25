import pytest


@pytest.mark.integration
def test_should_return_valid_assets(api_client):
    assets = api_client.get_assets()
    assert assets is not None, "Assets should not be None"
    assert hasattr(assets, "data"), "Assets should have a 'data' attribute"
    assert hasattr(assets.data, "grid_owners"), "Assets data should have 'grid_owners' attribute"
    assert isinstance(assets.data.grid_owners, list), "Grid owners should be a list"
    assert len(assets.data.grid_owners) > 0, "There should be at least one grid owner"


def _facilities(api_client):
    return [facility for grid_owner in api_client.get_assets().data.grid_owners for facility in grid_owner.facilities]


@pytest.mark.integration
def test_facility_voltages_should_be_non_negative(api_client):
    facilities = _facilities(api_client)

    for facility in facilities:
        assert facility.nominal_voltage >= 0, f"facility {facility.id} nominal voltage {facility.nominal_voltage} V"
        # Unset or None when the facility has no operational voltage configured.
        if facility.operational_voltage:
            assert facility.operational_voltage >= 0, (
                f"facility {facility.id} operational voltage {facility.operational_voltage} V"
            )
    # Guards against the field silently defaulting for every facility.
    assert any(facility.nominal_voltage > 0 for facility in facilities), "some facility should have a nominal voltage"


@pytest.mark.integration
def test_operational_voltage_should_be_near_nominal_when_both_are_set(api_client):
    facilities = [f for f in _facilities(api_client) if f.nominal_voltage > 0 and f.operational_voltage]
    if not facilities:
        pytest.skip("No facility with both a nominal and an operational voltage")

    # Grids run within a few percent of nominal; 20 % catches unit mix-ups (V vs kV) without being brittle.
    for facility in facilities:
        ratio = facility.operational_voltage / facility.nominal_voltage
        assert 0.8 <= ratio <= 1.2, f"facility {facility.id} operational/nominal voltage ratio {ratio:.3f}"
