import subprocess
import os
from conftest import run_command, INTERFACE, EXPECTED_SPEED, EXPECTED_MTU

class TestInterfaceState:
    """Tests that verify NIC interface properties"""

    def test_interface_exists(self):
        """Verify interface appears in /sys/class/net"""
        sys_path = f"/sys/class/net/{INTERFACE}"
        assert os.path.exists(sys_path), \
            f"FAIL: Interface {INTERFACE} not found in /sys/class/net"

    def test_interface_is_up(self):
        """Verify interface operational state is UP"""
        rc, stdout, stderr = run_command(
            ["cat", f"/sys/class/net/{INTERFACE}/operstate"]
        )
        assert rc == 0, f"FAIL: Could not read operstate: {stderr}"
        assert stdout == "up", \
            f"FAIL: Interface {INTERFACE} state is '{stdout}', expected 'up'"

    def test_interface_speed(self):
        """Verify interface link speed meets expectation"""
        rc, stdout, stderr = run_command(
            ["cat", f"/sys/class/net/{INTERFACE}/speed"]
        )
        assert rc == 0, f"FAIL: Could not read speed: {stderr}"
        actual_speed = int(stdout)
        assert actual_speed >= EXPECTED_SPEED, \
            f"FAIL: Speed {actual_speed} Mbps below expected {EXPECTED_SPEED} Mbps"

    def test_interface_mtu(self):
        """Verify interface MTU is set correctly"""
        rc, stdout, stderr = run_command(
            ["cat", f"/sys/class/net/{INTERFACE}/mtu"]
        )
        assert rc == 0, f"FAIL: Could not read MTU: {stderr}"
        actual_mtu = int(stdout)
        assert actual_mtu == EXPECTED_MTU, \
            f"FAIL: MTU is {actual_mtu}, expected {EXPECTED_MTU}"

    def test_interface_has_mac(self):
        """Verify interface has a valid MAC address"""
        rc, stdout, stderr = run_command(
            ["cat", f"/sys/class/net/{INTERFACE}/address"]
        )
        assert rc == 0, f"FAIL: Could not read MAC address"
        mac = stdout.strip()
        # MAC format: xx:xx:xx:xx:xx:xx
        parts = mac.split(":")
        assert len(parts) == 6, \
            f"FAIL: Invalid MAC format: {mac}"
        assert mac != "00:00:00:00:00:00", \
            f"FAIL: MAC address is all zeros"
