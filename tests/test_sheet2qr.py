from sheet2dict import Worksheet
import pytest
from sheet2qr import sheet_to_dict_list, sheet_factory


@pytest.fixture()
def workbook_fixture():
    ws = Worksheet()
    # with open("tests/sample_sheet.xlsx", "r") as f:
    # ws.csv_to_dict(csv_file=f, delimiter=';')
    ws.xlsx_to_dict(path="tests/sample_sheet.xlsx", select_sheet="Sheet1")
    yield ws


def test_sheet_to_dict(workbook_fixture):
    dict_list = sheet_to_dict_list(workbook_fixture)
    assert len(dict_list) == 3
    assert dict_list[0]["header1"] == "value11"
    assert dict_list[2]["header2"] == "value32"
    assert dict_list[2]["header3"] == "value33"


def test_sheet_factory_xsxl():
    ws = sheet_factory("xlsx", "tests/sample_sheet.xlsx")
    assert list(ws.header.keys()) == ["header1", "header2", "header3"]


def test_sheet_factory_csv():
    ws = sheet_factory("csv", "tests/sample_sheet.csv")
    print(ws)
    assert list(ws.header.keys()) == ["header1", "header2", "header3"]


def test_sheet_factory_undefined():
    with pytest.raises(Exception) as exc_info:
        sheet_factory("x", "tests/sample_sheet.csv")
    assert str(exc_info.value) == "Unsupported sheet format x"
