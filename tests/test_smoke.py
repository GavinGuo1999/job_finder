from jobradar import __version__
from jobradar.cli import DESCRIPTION, build_parser, main


def test_version_is_defined() -> None:
    assert __version__


def test_cli_help_smoke(capsys) -> None:
    parser = build_parser()

    try:
        parser.parse_args(["--help"])
    except SystemExit as exc:
        assert exc.code == 0

    captured = capsys.readouterr()
    assert DESCRIPTION in captured.out


def test_cli_main_smoke() -> None:
    assert main([]) == 0
