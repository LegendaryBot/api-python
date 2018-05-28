import wow.wow_region as wr
import json


def test_wow_region_get_token_price():
    event = {
        "pathParameters": {
            "region": "us"
        }
    }
    result = wr.get_token_price(event, None)
    assert result['statusCode'] == 200
    json_entry = json.loads(result['body'])
    assert "title" in json_entry

    event = {
        "pathParameters": {
            "region": "eu"
        }
    }
    result = wr.get_token_price(event, None)
    assert result['statusCode'] == 200
    json_entry = json.loads(result['body'])
    assert "title" in json_entry

    event = {
        "pathParameters": {
            "region": "asdf"
        }
    }
    result = wr.get_token_price(event, None)
    assert result['statusCode'] == 404

def test_wow_region_get_legion_building():
    event = {
        "pathParameters": {
            "region": "us"
        }
    }
    result_us = wr.get_legion_building(event, None)
    event = {
        "pathParameters": {
            "region": "eu"
        }
    }
    result_eu = wr.get_legion_building(event, None)
    assert result_us != result_eu
    assert result_us['statusCode'] == 200
    assert result_eu['statusCode'] == 200
