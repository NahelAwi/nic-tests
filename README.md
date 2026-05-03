# NIC Automated Test Suite

Automated validation suite for Linux NIC drivers and network interfaces,
built with Python and pytest.

## What It Tests

| Module | Tests | Description |
|---|---|---|
| test_interface.py | 5 | Interface state, speed, MTU, MAC address |
| test_connectivity.py | 5 | Ping, routing, packet loss validation |
| test_driver.py | 5 | Driver load, binding, RX/TX error counters |
| test_performance.py | 3 | TCP throughput, UDP packet loss, retransmits |

## Tech Stack
- Python 3.14 / pytest
- subprocess (shell command execution)
- iperf3 (performance testing)
- Linux /sys, /proc, ethtool, ip

## How to Run

Install dependencies:
```bash
pip3 install pytest --break-system-packages
sudo apt install -y iperf3
```

Run full suite:
```bash
pytest -v
```

Run specific module:
```bash
pytest -v test_performance.py
```

## Test Environment
- Ubuntu 26.04, Kernel 7.0.0-15-generic
- Intel e1000 NIC driver
