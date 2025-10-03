import os, time, requests

BASE = os.environ.get("VSR_BASE", "http://localhost:8080")

def test_e2e_claim_to_settlement():
    # 1) Mint claim
    r = requests.post(f"{BASE}/claims", json={
        "poId":"PO-2025-0001","buyerId":"M-001","sellerId":"FPO-001",
        "items":[{"sku":"cotton-bale","qty":20,"uom":"bale"}]
    })
    assert r.status_code == 201, r.text
    claimTokenId = r.json()["claimTokenId"]

    # 2) Fund escrow
    r = requests.post(f"{BASE}/escrow/fund", json={"claimTokenId":claimTokenId,"bankAccountRef":"ESCROW-XYZ","amountINR":500000,"currency":"INR"})
    assert r.ok, r.text

    # 3) Submit QC
    r = requests.post(f"{BASE}/qc/submit", json={"claimTokenId":claimTokenId,"labId":"LAB-9","reports":[
        {"test":"staple","value":28.5,"units":"mm","evidenceHash":"0xabc"},
        {"test":"moisture","value":7.1,"units":"%","evidenceHash":"0xdef"}
    ]})
    assert r.ok, r.text

    # 4) Release settlement
    r = requests.post(f"{BASE}/settlement/release", json={"claimTokenId":claimTokenId,
        "beneficiaries":[{"id":"F-001","amountINR":300000},{"id":"FPO-001","amountINR":200000}],
        "mspTopupINR":0
    })
    assert r.ok, r.text

    # 5) Debug
    s = requests.get(f"{BASE}/_debug/state").json()
    assert s["claims"][claimTokenId]["status"] == "settled"
