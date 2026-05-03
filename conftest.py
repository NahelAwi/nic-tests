import pytest
import subprocess

# The interface we're testing - change this if needed
INTERFACE = "ens33"
EXPECTED_SPEED = 1000      # Mbps
EXPECTED_MTU = 1500        # bytes
GATEWAY_IP = "192.168.223.2"
EXTERNAL_IP = "8.8.8.8"

def run_command(cmd):
    """Helper: run a shell command, return (returncode, stdout, stderr)"""
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()

@pytest.fixture
def interface():
    """Fixture: provides interface name to all tests"""
    return INTERFACE

@pytest.fixture
def nic_constants():
    """Fixture: provides expected NIC values to all tests"""
    return {
        "interface": INTERFACE,
        "expected_speed": EXPECTED_SPEED,
        "expected_mtu": EXPECTED_MTU,
        "gateway": GATEWAY_IP,
        "external": EXTERNAL_IP
    }
