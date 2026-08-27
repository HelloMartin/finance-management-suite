from typer.testing import CliRunner

from finance_suite.cli import app

runner = CliRunner()


def test_cli_help_exits_successfully():
    """Tests cli help function"""
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Finance Management Suite CLI." in result.output
    assert "Usage: " in result.output


def test_cli_hello_outputs_app_name():
    """Tests cli hello function"""
    result = runner.invoke(app, ["hello"])

    assert result.exit_code == 0
    assert "Finance Management Suite" in result.output
