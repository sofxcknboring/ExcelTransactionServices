import json
from unittest.mock import patch

from src.views import get_homepage_json


@patch("json.dumps")
@patch("src.utils.read_excel")
def test_get_homepage_json(mock_read_excel, mock_json_dumps, transactions_data):
    mock_read_excel.return_value.read_excel.return_value = transactions_data
    expected_result = {
        "1": "1",
    }
    mock_json_dumps.return_value = json.dumps(expected_result)
    filter_date = "01.02.2021"
    result = get_homepage_json(filter_date)
    assert result == json.dumps(expected_result)
