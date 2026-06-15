from miniproject import calculate_energy_financials


def test_under_discount_threshold():
    devices = [
        {
            "id": "M01",
            "location": "A",
            "old_index": 0,
            "new_index": 10000,
            "status": "Normal"
        }
    ]

    result = calculate_energy_financials(devices)

    assert result == (
        10000,
        0,
        30000000
    )
