import pytest
import sys
import os
import json
from pathlib import Path
from collections import Counter

# Add parent directory to path so we can import log_analyzer
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from log_analyzer import *


def test_import():
    """Verify that all required functions can be imported successfully."""
    assert True


# ============================================================================
# PHASE 2: Testing core parsing functions
# ============================================================================


def test_ip_pattern_matches_correctly():
    """
    Test that IP_PATTERN correctly matches valid IP addresses.
    
    Why: IP detection is the foundation of security analysis.
    """
    test_line = '192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326'
    
    matches = re.findall(IP_PATTERN, test_line)
    
    assert len(matches) == 1
    assert matches[0] == '192.168.1.1'


def test_ip_pattern_ignores_invalid_ips():
    """
    Test that IP_PATTERN doesn't match invalid IP addresses.
    
    Why: False positives waste analyst time investigating non-existent threats.
    """
    test_line = '999.999.999.999 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326'
    
    matches = re.findall(IP_PATTERN, test_line)
    
    assert len(matches) == 0


def test_error_pattern_detects_keywords():
    """
    Test that ERROR_PATTERN correctly identifies error keywords.
    
    Why: Error detection helps identify system failures and attacks.
    """
    test_line = 'ERROR: Database connection failed - CRITICAL'
    
    matches = re.findall(ERROR_PATTERN, test_line, re.IGNORECASE)
    
    # Should detect both ERROR and CRITICAL
    assert len(matches) >= 2
    assert 'ERROR' in [m.upper() for m in matches]
    assert 'CRITICAL' in [m.upper() for m in matches]


def test_error_pattern_case_insensitive():
    """
    Test that ERROR_PATTERN is case-insensitive.
    
    Why: Log entries vary in case (error, ERROR, Error).
    """
    test_line = 'error: System failure - Warning: Disk full'
    
    matches = re.findall(ERROR_PATTERN, test_line, re.IGNORECASE)
    
    # Should detect both 'error' and 'Warning'
    assert len(matches) >= 2
    assert 'ERROR' in [m.upper() for m in matches]
    assert 'WARNING' in [m.upper() for m in matches]


def test_analyze_log_counts_lines_correctly():
    """
    Test that analyze_log() correctly counts total lines using temporary file.
    
    Why: Line counting is the most basic but critical metric.
    """
    # Create temporary log content
    content = [
        'Line 1 - INFO: Started',
        'Line 2 - ERROR: Failed',
        'Line 3 - WARNING: Timeout',
    ]
    
    # Write to temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False, encoding='utf-8') as tmp:
        tmp.writelines(line + '\n' for line in content)
        tmp_path = tmp.name
    
    try:
        line_count, _, _, _ = analyze_log(Path(tmp_path))
        assert line_count == 3
    finally:
        os.remove(tmp_path)


def test_analyze_log_extracts_ip_addresses():
    """
    Test that analyze_log() correctly extracts and counts IPs from log content.
    
    Why: IP counting identifies unique sources and potential attackers.
    """
    content = [
        '192.168.1.1 - - "GET /index.html" 200',
        '192.168.1.1 - - "POST /login.php" 401',
        '10.0.0.2 - - "GET /about.html" 200',
        '192.168.1.1 - - "GET /admin.php" 403',
    ]
    
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False, encoding='utf-8') as tmp:
        tmp.writelines(line + '\n' for line in content)
        tmp_path = tmp.name
    
    try:
        _, ip_count, _, _ = analyze_log(Path(tmp_path))
        
        # IP 192.168.1.1 appears 3 times, 10.0.0.2 appears 1 time
        assert ip_count['192.168.1.1'] == 3
        assert ip_count['10.0.0.2'] == 1
        assert len(ip_count) == 2
    finally:
        os.remove(tmp_path)


def test_analyze_log_detects_errors():
    """
    Test that analyze_log() correctly counts error keywords.
    
    Why: Error frequency indicates system health and potential attacks.
    """
    content = [
        'INFO: Application started',
        'ERROR: Database timeout',
        'WARNING: Low memory',
        'ERROR: Connection refused',
        'CRITICAL: Service down',
    ]
    
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False, encoding='utf-8') as tmp:
        tmp.writelines(line + '\n' for line in content)
        tmp_path = tmp.name
    
    try:
        _, _, error_count, _ = analyze_log(Path(tmp_path))
        
        assert error_count['ERROR'] == 2
        assert error_count['WARNING'] == 1
        assert error_count['CRITICAL'] == 1
        assert len(error_count) == 3
    finally:
        os.remove(tmp_path)


def test_analyze_log_handles_empty_file():
    """
    Test that analyze_log() gracefully handles empty files.
    
    Why: Edge cases must be handled to prevent crashes in production.
    """
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False, encoding='utf-8') as tmp:
        tmp.write('')  # Empty file
        tmp_path = tmp.name
    
    try:
        line_count, ip_count, error_count, preview = analyze_log(Path(tmp_path))
        
        assert line_count == 0
        assert len(ip_count) == 0
        assert len(error_count) == 0
        assert len(preview) == 0
    finally:
        os.remove(tmp_path)


def test_log_preview_limited_to_max_lines():
    """
    Test that log preview doesn't exceed MAX_PREVIEW_LINES.
    
    Why: Memory efficiency matters for large log files.
    """
    content = [f'Line {i}: INFO: Message' for i in range(150)]
    
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False, encoding='utf-8') as tmp:
        tmp.writelines(line + '\n' for line in content)
        tmp_path = tmp.name
    
    try:
        _, _, _, preview = analyze_log(Path(tmp_path))
        
        # Should only store last MAX_PREVIEW_LINES (100) lines
        assert len(preview) <= MAX_PREVIEW_LINES
        assert preview[0] == 'Line 50: INFO: Message'  # First line in preview should be line 50
    finally:
        os.remove(tmp_path)


def test_get_log_files_handles_file_path():
    """
    Test that get_log_files() returns the file itself when path is a file.
    
    Why: Function should handle both single files and directories.
    """
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.log', delete=False) as tmp:
        tmp_path = Path(tmp.name)
    
    try:
        result = get_log_files(tmp_path, recursive=True)
        assert len(result) == 1
        assert result[0] == tmp_path
    finally:
        os.remove(tmp_path)


def test_get_log_files_filters_by_extension():
    """
    Test that get_log_files() only returns files with log extensions (.log, .txt).
    
    Why: Should ignore non-log files to avoid parsing errors.
    """
    import tempfile
    import shutil
    
    # Create a temporary directory with mixed files
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # Create log files
        (tmp_path / 'file1.log').touch()
        (tmp_path / 'file2.txt').touch()
        
        # Create non-log files
        (tmp_path / 'file3.py').touch()
        (tmp_path / 'file4.json').touch()
        (tmp_path / 'file5.exe').touch()
        
        result = get_log_files(tmp_path, recursive=False)
        
        # Should only find .log and .txt files
        assert len(result) == 2
        assert all(f.suffix.lower() in {'.log', '.txt'} for f in result)


def test_get_log_files_recursive_search():
    """
    Test that get_log_files() recursively searches subdirectories.
    
    Why: Log files are often organized in nested directory structures.
    """
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # Create nested directory structure
        sub_dir = tmp_path / 'subdir'
        sub_dir.mkdir()
        
        # Create log files
        (tmp_path / 'root.log').touch()
        (sub_dir / 'nested.log').touch()
        
        # Non-recursive search
        non_recursive = get_log_files(tmp_path, recursive=False)
        assert len(non_recursive) == 1
        assert non_recursive[0].name == 'root.log'
        
        # Recursive search
        recursive = get_log_files(tmp_path, recursive=True)
        assert len(recursive) == 2
        assert {f.name for f in recursive} == {'root.log', 'nested.log'}


def test_generate_report_includes_all_sections():
    """
    Test that generate_report() creates a report with all required sections.
    
    Why: Report must be complete for effective analysis.
    """
    filename = Path('test.log')
    line_count = 10
    ip_count = Counter({'192.168.1.1': 5, '10.0.0.2': 3})
    error_count = Counter({'ERROR': 2, 'WARNING': 1})
    log_preview = ['Line 1: Test', 'Line 2: Test']
    analysis_time = '2026-09-06 12:00:00'
    
    report = generate_report(
        filename, line_count, ip_count, error_count, log_preview, analysis_time
    )
    
    # Verify key sections are present
    assert 'LOG ANALYZER' in report
    assert 'IP ADDRESSES OCCURRENCES' in report
    assert 'ERRORS OCCURRENCES' in report
    assert 'SUMMARY REPORT' in report
    assert 'END OF REPORT' in report
    
    # Verify IPs are listed
    assert '192.168.1.1 → 5' in report
    assert '10.0.0.2 → 3' in report
    
    # Verify errors are listed
    assert 'ERROR → 2' in report
    assert 'WARNING → 1' in report
    
    # Verify summary stats
    assert 'Total Lines   : 10' in report
    assert 'Total IPs     : 8' in report
    assert 'Unique IPs    : 2' in report
    assert 'Total Errors  : 3' in report
    assert 'Unique Errors : 2' in report


def test_generate_report_handles_empty_results():
    """
    Test that generate_report() handles cases with no IPs or errors.
    
    Why: Should display friendly messages instead of empty sections.
    """
    filename = Path('test.log')
    line_count = 5
    ip_count = Counter()
    error_count = Counter()
    log_preview = ['Line 1', 'Line 2']
    analysis_time = '2026-09-06 12:00:00'
    
    report = generate_report(
        filename, line_count, ip_count, error_count, log_preview, analysis_time
    )
    
    # Should show "no IP" and "no errors" messages
    assert 'NO IP ADDRESSES FOUND' in report
    assert 'NO ERRORS FOUND' in report
    assert 'No IP addresses found in the log file.' in report
    assert 'No errors found in the log file.' in report


def test_export_functions_create_files(tmp_path):
    """
    Test that export_to_txt() and export_to_json() create files.
    
    Why: Reports must be saved to disk for later review.
    """
    report_text = 'Test report content'
    filename = Path('test.log')
    line_count = 10
    ip_count = Counter({'192.168.1.1': 5})
    error_count = Counter({'ERROR': 2})
    log_preview = ['Line 1']
    analysis_time = '2026-09-06 12:00:00'
    
    # Test TXT export
    export_to_txt(report_text, tmp_path, quiet=True)
    txt_files = list(tmp_path.glob('report_*.txt'))
    assert len(txt_files) == 1
    assert txt_files[0].read_text(encoding='utf-8') == report_text
    
    # Test JSON export
    export_to_json(
        filename, line_count, ip_count, error_count, 
        log_preview, analysis_time, tmp_path, quiet=True
    )
    json_files = list(tmp_path.glob('report_*.json'))
    assert len(json_files) == 1
    
    # Verify JSON content
    data = json.loads(json_files[0].read_text(encoding='utf-8'))
    assert data['file'] == 'test.log'
    assert data['total_lines'] == 10
    assert data['ip_addresses']['192.168.1.1'] == 5