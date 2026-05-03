import subprocess
import json
import pytest
from conftest import run_command

LOOPBACK_IP = "127.0.0.1"
MIN_THROUGHPUT_GBPS = 10.0    # minimum acceptable loopback throughput
MAX_PACKET_LOSS_PCT = 0.5     # maximum acceptable UDP packet loss %
TEST_DURATION = 5             # seconds (short for test suite speed)

def start_iperf_server():
    """Start iperf3 server as background process"""
    server = subprocess.Popen(
        ["iperf3", "-s", "-1"],  # -1 = exit after one test
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return server

class TestPerformance:
    """Performance tests for network interface"""

    def test_tcp_throughput_baseline(self):
        """Verify TCP loopback throughput meets minimum threshold"""
        server = start_iperf_server()

        rc, stdout, stderr = run_command([
            "iperf3", "-c", LOOPBACK_IP,
            "-t", str(TEST_DURATION),
            "-J"    # JSON output for reliable parsing
        ])

        server.wait()

        assert rc == 0, f"FAIL: iperf3 client failed\n{stderr}"

        # Parse JSON output
        try:
            results = json.loads(stdout)
            bits_per_sec = results["end"]["sum_sent"]["bits_per_second"]
            gbps = bits_per_sec / 1e9
        except (KeyError, json.JSONDecodeError) as e:
            pytest.fail(f"FAIL: Could not parse iperf3 output: {e}")

        assert gbps >= MIN_THROUGHPUT_GBPS, \
            f"FAIL: Throughput {gbps:.1f} Gbps below threshold {MIN_THROUGHPUT_GBPS} Gbps"

    def test_udp_packet_loss(self):
        """Verify UDP packet loss is within acceptable threshold"""
        server = start_iperf_server()

        rc, stdout, stderr = run_command([
            "iperf3", "-c", LOOPBACK_IP,
            "-u",               # UDP mode
            "-b", "1G",         # 1 Gbps (conservative to avoid overflow)
            "-t", str(TEST_DURATION),
            "-J"
        ])

        server.wait()

        assert rc == 0, f"FAIL: iperf3 UDP test failed\n{stderr}"

        try:
            results = json.loads(stdout)
            lost = results["end"]["sum"]["lost_packets"]
            total = results["end"]["sum"]["packets"]
            loss_pct = (lost / total * 100) if total > 0 else 0
        except (KeyError, json.JSONDecodeError) as e:
            pytest.fail(f"FAIL: Could not parse iperf3 output: {e}")

        assert loss_pct <= MAX_PACKET_LOSS_PCT, \
            f"FAIL: UDP loss {loss_pct:.2f}% exceeds threshold {MAX_PACKET_LOSS_PCT}%"

    def test_tcp_zero_retransmits(self):
        """Verify TCP transmission has zero retransmits at moderate load"""
        server = start_iperf_server()

        rc, stdout, stderr = run_command([
            "iperf3", "-c", LOOPBACK_IP,
            "-b", "5G",         # moderate load
            "-t", str(TEST_DURATION),
            "-J"
        ])

        server.wait()

        assert rc == 0, f"FAIL: iperf3 failed\n{stderr}"

        try:
            results = json.loads(stdout)
            retransmits = results["end"]["sum_sent"]["retransmits"]
        except (KeyError, json.JSONDecodeError) as e:
            pytest.fail(f"FAIL: Could not parse iperf3 output: {e}")

        assert retransmits == 0, \
            f"FAIL: {retransmits} TCP retransmits detected under 5G load"
