# datasette-gunicorn

[![PyPI](https://img.shields.io/pypi/v/datasette-gunicorn.svg)](https://pypi.org/project/datasette-gunicorn/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-gunicorn?include_prereleases&label=changelog)](https://github.com/simonw/datasette-gunicorn/releases)
[![Tests](https://github.com/simonw/datasette-gunicorn/workflows/Test/badge.svg)](https://github.com/simonw/datasette-gunicorn/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-gunicorn/blob/main/LICENSE)

Run a [Datasette](https://datasette.io/) server using [Gunicorn](https://gunicorn.org/)

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-gunicorn

## Usage

The plugin adds a new `datasette gunicorn` command. This takes the exact same options as `datasette serve`, plus one more option for setting the number of Gunicorn workers to start:

`-w/--workers X` - set the number of workers. Defaults to 1.

To start serving a database using 4 workers, run the following:

    datasette gunicorn fixtures.db -w 4

It is advisable to switch your datasette [into WAL mode](https://til.simonwillison.net/sqlite/enabling-wal-mode) to get the best performance out of this configuration:

    sqlite3 fixtures.db 'PRAGMA journal_mode=WAL;'

Run `datasette gunicorn --help` for a full list of options (which are the same as `datasette serve --help`, with the addition of the new `-w` option).

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-gunicorn
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
