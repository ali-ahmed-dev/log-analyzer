import pytest
import tempfile
import os


@pytest.fixture
def sample_log_content():
    """Return sample Apache log entries for testing."""
    return [
        '192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326',
        '10.0.0.2 - - [10/Oct/2023:13:55:37 +0000] "POST /login.php HTTP/1.1" 404 532',
        '192.168.1.1 - - [10/Oct/2023:13:56:10 +0000] "GET /about.html HTTP/1.1" 200 1234',
        '10.0.0.3 - - [10/Oct/2023:13:57:01 +0000] "GET /index.html HTTP/1.1" 500 0',
        '192.168.1.1 - - [10/Oct/2023:13:58:20 +0000] "GET /admin.php HTTP/1.1" 403 512',
        '10.0.0.4 - - [10/Oct/2023:13:59:45 +0000] "GET /index.html HTTP/1.1" 200 1024',
    ]


@pytest.fixture
def create_temp_log_file(sample_log_content):
    """
    Create a temporary log file with sample content.
    
    Yields the file path for test usage and cleans up after completion.
    Using NamedTemporaryFile with delete=False to avoid auto-deletion on Windows.
    """
    with tempfile.NamedTemporaryFile(
        mode='w', 
        suffix='.log', 
        delete=False, 
        encoding='utf-8'
    ) as tmp:
        tmp.writelines(line + '\n' for line in sample_log_content)
        tmp_path = tmp.name
    
    yield tmp_path
    
    # Clean up: remove temporary file after test completes
    try:
        os.remove(tmp_path)
    except OSError:
        # File might already be deleted by another process
        pass
