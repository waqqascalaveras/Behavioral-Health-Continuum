import subprocess
import sys
import time
import os
import signal
import pytest

ETL_DIR = os.path.dirname(os.path.abspath(__file__))
CLI_APP_PATH = os.path.join(ETL_DIR, 'cli_app.pyw')

@pytest.mark.timeout(10)
def test_cli_app_launches_and_stays_open():
    """
    Test that cli_app.pyw launches and does not immediately exit (in a non-interactive environment, should show a Tk window).
    """
    # Launch the .pyw file as a subprocess
    proc = subprocess.Popen([sys.executable, CLI_APP_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3)  # Give it time to open (and possibly close)
    # Check if process is still running
    still_running = proc.poll() is None
    if still_running:
        # Clean up: terminate the process
        if os.name == 'nt':
            proc.send_signal(signal.CTRL_BREAK_EVENT)
        else:
            proc.terminate()
    assert still_running, 'cli_app.pyw closed immediately (should stay open or show a window)'

if __name__ == '__main__':
    import pytest
    raise SystemExit(pytest.main([__file__]))
