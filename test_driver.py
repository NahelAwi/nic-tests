import subprocess
import os
from conftest import run_command, INTERFACE

EXPECTED_DRIVER = "e1000"

class TestDriver:
    """Tests that verify NIC driver state"""

    def test_driver_is_loaded(self):
        """Verify e1000 driver is loaded in kernel"""
        rc, stdout, stderr = run_command(["lsmod"])
        assert EXPECTED_DRIVER in stdout, \
            f"FAIL: Driver {EXPECTED_DRIVER} not found in lsmod"

    def test_driver_bound_to_interface(self):
        """Verify correct driver is bound to interface via /sys"""
        driver_path = f"/sys/class/net/{INTERFACE}/device/driver"
        assert os.path.exists(driver_path), \
            f"FAIL: No driver bound to {INTERFACE}"
        # Read the symlink target
        link_target = os.readlink(driver_path)
        assert EXPECTED_DRIVER in link_target, \
            f"FAIL: Wrong driver bound: {link_target}"

    def test_no_rx_errors(self):
        """Verify no receive errors on interface"""
        rc, stdout, stderr = run_command(
            ["cat", f"/proc/net/dev"]
        )
        for line in stdout.splitlines():
            if INTERFACE in line:
                parts = line.split()
                rx_errors = int(parts[3])
                assert rx_errors == 0, \
                    f"FAIL: {rx_errors} RX errors detected on {INTERFACE}"

    def test_no_tx_errors(self):
        """Verify no transmit errors on interface"""
        rc, stdout, stderr = run_command(
            ["cat", "/proc/net/dev"]
        )
        for line in stdout.splitlines():
            if INTERFACE in line:
                parts = line.split()
                tx_errors = int(parts[11])
                assert tx_errors == 0, \
                    f"FAIL: {tx_errors} TX errors detected on {INTERFACE}"

    def test_ethtool_link_detected(self):
        """Verify ethtool reports link detected"""
        rc, stdout, stderr = run_command(
            ["ethtool", INTERFACE]
        )
        assert "Link detected: yes" in stdout, \
            f"FAIL: ethtool reports no link detected"
