"""
Log format parsers for Log Analyzer.

This module provides parsers for different log formats:
- Apache/Nginx Combined Log Format
- (Future: JSON logs, syslog, etc.)
"""

from __future__ import annotations

import re
from typing import Optional


# ===================== APACHE/Nginx COMBINED LOG FORMAT =====================
# Example line:
# 192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326
#
# Fields extracted:
# - ip:        Client IP address
# - timestamp: Request date and time
# - method:    HTTP method (GET, POST, PUT, DELETE, ...)
# - path:      Requested resource path
# - status:    HTTP status code (200, 404, 500, ...)
# - size:      Response size in bytes (may be '-' for empty responses)

APACHE_PATTERN = re.compile(
    r'^(?P<ip>\S+)\s+'           # Client IP
    r'\S+\s+'                    # Identity (usually '-')
    r'\S+\s+'                    # User (usually '-')
    r'\[(?P<timestamp>[^\]]+)\]\s+'  # Timestamp between brackets
    r'"(?P<method>\S+)\s+'       # HTTP method
    r'(?P<path>\S+)\s+'          # Requested path
    r'\S+"\s+'                   # HTTP version (ignored)
    r'(?P<status>\d{3})\s+'      # HTTP status code
    r'(?P<size>\S+)'             # Response size
)


def parse_apache_line(line: str) -> Optional[dict]:
    """
    Parse a single Apache/Nginx Combined Log Format line.
    
    Args:
        line: A single log line to parse.
    
    Returns:
        A dictionary containing parsed fields, or None if the line
        doesn't match the Apache format.
        
        Dictionary keys:
            - ip (str): Client IP address
            - timestamp (str): Request timestamp
            - method (str): HTTP method (GET, POST, ...)
            - path (str): Requested resource path
            - status (int): HTTP status code
            - size (int or None): Response size in bytes ('-' becomes None)
    
    Example:
        >>> line = '192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326'
        >>> result = parse_apache_line(line)
        >>> result['ip']
        '192.168.1.1'
        >>> result['status']
        200
    """
    if not line or not line.strip():
        return None
    
    match = APACHE_PATTERN.match(line.strip())
    
    if not match:
        return None
    
    data = match.groupdict()
    
    # Convert status to integer for easier analysis
    try:
        data['status'] = int(data['status'])
    except (ValueError, TypeError):
        return None
    
    # Convert size to integer, handling '-' as None (empty response)
    if data['size'] == '-':
        data['size'] = None
    else:
        try:
            data['size'] = int(data['size'])
        except (ValueError, TypeError):
            data['size'] = None
    
    return data


def is_apache_format(line: str) -> bool:
    """
    Check if a line matches the Apache/Nginx Combined Log Format.
    
    This is a fast check used for auto-detection. It doesn't fully
    parse the line, just verifies it matches the pattern.
    
    Args:
        line: A single log line.
    
    Returns:
        True if the line matches Apache format, False otherwise.
    """
    if not line or not line.strip():
        return False
    
    return APACHE_PATTERN.match(line.strip()) is not None