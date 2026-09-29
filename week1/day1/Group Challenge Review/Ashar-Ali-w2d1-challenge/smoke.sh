
#testing 
#!/usr/bin/env bash
# Smoke test: proves the endpoints are working. Exits 0 on success.
set -eu
python -m pytest tests/test_endpoints.py -q