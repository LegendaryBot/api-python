import overwatch.overwatch as ow


def test_overwatch():
    event = {
        "pathParameters": {
            "battletag": "Greatman-1189",
            "region": "us"
        }
    }
    result = ow.get_overwatch_stats(event, None)
    assert result['statusCode'] == 404
    event = {
        "pathParameters": {
            "battletag": "Spek-11212",
            "region": "us"
        }
    }
    result = ow.get_overwatch_stats(event, None)
    assert result['statusCode'] == 200

    event = {
        "pathParameters": {
            "battletag": "Spek-112123",
            "region": "us"
        }
    }
    result = ow.get_overwatch_stats(event, None)
    assert result['statusCode'] == 404
