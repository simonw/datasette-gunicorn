from datasette.app import Datasette
import httpx
import pytest
import subprocess
import sys
import tempfile
import time


@pytest.fixture(scope="session")
def localhost_server():
    ds_proc = subprocess.Popen(
        [sys.executable, "-m", "datasette", "gunicorn", "-p", "8043"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        # Avoid FileNotFoundError: [Errno 2] No such file or directory:
        cwd=tempfile.gettempdir(),
    )
    # Give the server time to start
    time.sleep(1.5)
    # Check it started successfully
    assert not ds_proc.poll(), ds_proc.stdout.read().decode("utf-8")
    print(ds_proc)
    yield ds_proc
    # Shut it down at the end of the pytest session
    ds_proc.terminate()


@pytest.mark.parametrize(
    "path,expected_status_code",
    (
        ("/", 200),
        ("/.json", 200),
        ("/_memory", 200),
        ("/_memory.json", 200),
        ("/404", 404),
        ("/404.json", 404),
    ),
)
def test_page(localhost_server, path, expected_status_code):
    response = httpx.get("http://localhost:8043{}".format(path))
    assert response.status_code == expected_status_code
    if path.endswith(".json"):
        assert isinstance(response.json(), dict)
