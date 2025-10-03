# Testing the VSR Mock

## Postman
- Import `VSR-MOCK.postman_environment.json` and `VSR-MOCK.postman_collection.json`.
- Set the environment to **VSR Mock (Local)**.
- Run the requests in order: 1) Mint Claim → 2) Fund Escrow → 3) Submit QC → 4) Release Settlement → 5) Debug State.

## Pytest
```bash
# Terminal A
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python vsr_mock_server.py  # http://localhost:8080

# Terminal B
./RUN_TESTS.sh
# or
source .venv/bin/activate && pip install -r requirements.tests.txt && pytest -q
```

To target a different base URL:
```bash
VSR_BASE=http://127.0.0.1:8080 pytest -q
```
