import subprocess
from conftest import run_command, GATEWAY_IP, EXTERNAL_IP

class TestConnectivity:
    """Tests that verify network connectivity"""

    def test_ping_loopback(self):
        """Verify loopback interface responds to ping"""
        rc, stdout, stderr = run_command(
            ["ping", "-c", "3", "-W", "2", "127.0.0.1"]
        )
        assert rc == 0, \
            f"FAIL: Loopback ping failed\n{stdout}"

    def test_ping_gateway(self):
        """Verify default gateway is reachable"""
        rc, stdout, stderr = run_command(
            ["ping", "-c", "3", "-W", "2", GATEWAY_IP]
        )
        assert rc == 0, \
            f"FAIL: Gateway {GATEWAY_IP} unreachable\n{stdout}"

    def test_ping_external(self):
        """Verify external internet connectivity"""
        rc, stdout, stderr = run_command(
            ["ping", "-c", "4", "-W", "3", EXTERNAL_IP]
        )
        assert rc == 0, \
            f"FAIL: External {EXTERNAL_IP} unreachable\n{stdout}"

    def test_zero_packet_loss(self):
        """Verify 0% packet loss to gateway"""
        rc, stdout, stderr = run_command(
            ["ping", "-c", "10", "-W", "2", GATEWAY_IP]
        )
        assert "0% packet loss" in stdout, \
            f"FAIL: Packet loss detected\n{stdout}"

    def test_default_route_exists(self):
        """Verify a default route exists in routing table"""
        rc, stdout, stderr = run_command(
            ["ip", "route", "show"]
        )
        assert "default" in stdout, \
            f"FAIL: No default route found\n{stdout}"
