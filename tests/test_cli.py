from click.testing import CliRunner
from unittest.mock import patch
from sheet2qr.__main__ import cli, default_config


runner = CliRunner()


@patch('sheet2qr.__main__.sheet2qr')
def test_sheet_to_qr_happy_path(sheet2qr_mock):
    result = runner.invoke(
        cli,
        ["from-xlsx",
         "--file", "test.xlsx",
         "--sheet-name", "Sheet1",
         "to-pdf",
         "--file", "qr.pdf"

         ])
    sheet2qr_mock.assert_called_once_with(
        {**default_config,
         **{"src_file": "test.xlsx",
            "sheet_name": "Sheet1",
            "src_file_type": "xlsx",
            "dst_file": "qr.pdf",
            "dst_file_type": "pdf"
            }})
    assert result.exit_code == 0


def test_sheet_to_qr_happy_failure():
    result = runner.invoke(
        cli,
        ["from-xlsx",
         "--file", "test.xlsx",
         "--sheet-name", "some-workbook",
         "to-pdf",
         ])
    assert result.exit_code == 1
