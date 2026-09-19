import pytest

from parsers import parse_apache_line, is_apache_format


# ============================================================================
# Testing parse_apache_line()
# ============================================================================


def test_parse_apache_line_extracts_ip():
    """Test that parse_apache_line() correctly extracts the IP address."""
    line = '192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326'
    
    result = parse_apache_line(line)
    
    assert result is not None
    assert result['ip'] == '192.168.1.1'


def test_parse_apache_line_extracts_timestamp():
    """Test that parse_apache_line() correctly extracts the timestamp."""
    line = '192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326'
    
    result = parse_apache_line(line)
    
    assert result['timestamp'] == '10/Oct/2023:13:55:36 +0000'


def test_parse_apache_line_extracts_method_and_path():
    """Test that parse_apache_line() correctly extracts HTTP method and path."""
    line = '10.0.0.5 - - [10/Oct/2023:13:55:37 +0000] "POST /login.php HTTP/1.1" 401 512'
    
    result = parse_apache_line(line)
    
    assert result['method'] == 'POST'
    assert result['path'] == '/login.php'


def test_parse_apache_line_extracts_status_as_int():
    """Test that parse_apache_line() converts status to integer."""
    line = '192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 404 2326'
    
    result = parse_apache_line(line)
    
    assert result['status'] == 404
    assert isinstance(result['status'], int)


def test_parse_apache_line_extracts_size_as_int():
    """Test that parse_apache_line() converts size to integer."""
    line = '192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326'
    
    result = parse_apache_line(line)
    
    assert result['size'] == 2326
    assert isinstance(result['size'], int)


def test_parse_apache_line_handles_dash_size():
    """Test that parse_apache_line() handles '-' size as None."""
    line = '10.0.0.6 - - [10/Oct/2023:13:55:38 +0000] "GET /notfound HTTP/1.1" 404 -'
    
    result = parse_apache_line(line)
    
    assert result['size'] is None


def test_parse_apache_line_returns_none_for_invalid_line():
    """Test that parse_apache_line() returns None for non-Apache lines."""
    invalid_line = 'This is not an Apache log entry'
    
    result = parse_apache_line(invalid_line)
    
    assert result is None


def test_parse_apache_line_returns_none_for_empty_line():
    """Test that parse_apache_line() returns None for empty lines."""
    assert parse_apache_line('') is None
    assert parse_apache_line('   ') is None
    assert parse_apache_line('\n') is None


def test_parse_apache_line_handles_delete_method():
    """Test that parse_apache_line() handles non-GET/POST HTTP methods."""
    line = '10.0.0.7 - - [10/Oct/2023:13:55:42 +0000] "DELETE /api/users/1 HTTP/1.1" 500 0'
    
    result = parse_apache_line(line)
    
    assert result['method'] == 'DELETE'
    assert result['status'] == 500


def test_parse_apache_line_handles_ipv4_addresses():
    """Test that parse_apache_line() works with different IPv4 addresses."""
    lines = [
        '10.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET / HTTP/1.1" 200 100',
        '172.16.0.10 - - [10/Oct/2023:13:55:36 +0000] "GET / HTTP/1.1" 200 100',
        '203.0.113.5 - - [10/Oct/2023:13:55:36 +0000] "GET / HTTP/1.1" 200 100',
    ]
    
    for line in lines:
        result = parse_apache_line(line)
        assert result is not None
        assert 'ip' in result


# ============================================================================
# Testing is_apache_format()
# ============================================================================


def test_is_apache_format_returns_true_for_valid_line():
    """Test that is_apache_format() returns True for valid Apache lines."""
    line = '192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326'
    
    assert is_apache_format(line) is True


def test_is_apache_format_returns_false_for_invalid_line():
    """Test that is_apache_format() returns False for non-Apache lines."""
    invalid_line = 'INFO: Application started normally'
    
    assert is_apache_format(invalid_line) is False


def test_is_apache_format_returns_false_for_empty_line():
    """Test that is_apache_format() returns False for empty lines."""
    assert is_apache_format('') is False
    assert is_apache_format('   ') is False


def test_is_apache_format_returns_false_for_generic_log():
    """Test that is_apache_format() returns False for generic log lines."""
    generic_line = '2023-10-10 13:55:36 ERROR Database connection failed'
    
    assert is_apache_format(generic_line) is False