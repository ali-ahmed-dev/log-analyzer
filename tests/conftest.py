import pytest
import tempfile
import os


@pytest.fixture
def sample_log_content():
    """Return sample generic log entries for testing."""
    return [
        '192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326',
        '10.0.0.2 - - [10/Oct/2023:13:55:37 +0000] "POST /login.php HTTP/1.1" 404 532',
        '192.168.1.1 - - [10/Oct/2023:13:56:10 +0000] "GET /about.html HTTP/1.1" 200 1234',
        '10.0.0.3 - - [10/Oct/2023:13:57:01 +0000] "GET /index.html HTTP/1.1" 500 0',
        '192.168.1.1 - - [10/Oct/2023:13:58:20 +0000] "GET /admin.php HTTP/1.1" 403 512',
        '10.0.0.4 - - [10/Oct/2023:13:59:45 +0000] "GET /index.html HTTP/1.1" 200 1024',
    ]


@pytest.fixture
def sample_apache_log_content():
    """Return sample Apache Combined Log Format entries for testing."""
    return [
        '192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326',
        '192.168.1.1 - - [10/Oct/2023:13:55:37 +0000] "GET /about.html HTTP/1.1" 200 1234',
        '10.0.0.5 - - [10/Oct/2023:13:55:38 +0000] "POST /login.php HTTP/1.1" 401 512',
        '10.0.0.5 - - [10/Oct/2023:13:55:39 +0000] "POST /login.php HTTP/1.1" 401 512',
        '10.0.0.5 - - [10/Oct/2023:13:55:40 +0000] "POST /login.php HTTP/1.1" 200 1024',
        '10.0.0.6 - - [10/Oct/2023:13:55:41 +0000] "GET /admin.php HTTP/1.1" 404 0',
        '10.0.0.7 - - [10/Oct/2023:13:55:42 +0000] "DELETE /api/users/1 HTTP/1.1" 500 0',
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
    
    try:
        os.remove(tmp_path)
    except OSError:
        pass


@pytest.fixture
def create_temp_apache_log_file(sample_apache_log_content):
    """Create a temporary Apache log file with sample content."""
    with tempfile.NamedTemporaryFile(
        mode='w', 
        suffix='.log', 
        delete=False, 
        encoding='utf-8'
    ) as tmp:
        tmp.writelines(line + '\n' for line in sample_apache_log_content)
        tmp_path = tmp.name
    
    yield tmp_path
    
    try:
        os.remove(tmp_path)
    except OSError:
        pass