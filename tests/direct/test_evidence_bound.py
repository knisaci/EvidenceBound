import json


CONTRACT = "contracts/evidence_bound.py"


def submit_example(contract):
    return contract.submit_claim(
        "Kirago funding-record audit",
        "Twenty claimed deals were checked and all funding records were verified.",
        "RECORD_SET_CLAIM_V1",
        json.dumps(["https://evidence.example/audit.json"]),
        "sha256:1234567890abcdef",
        json.dumps({"claimed_deals": 20, "verified_funding_records": 20}),
        1,
        2,
    )


def test_submit_claim_sets_pending_state(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy(CONTRACT)
    direct_vm.sender = direct_alice
    claim_id = submit_example(contract)
    claim = contract.get_claim(claim_id)
    assert claim_id == "claim-1"
    assert claim["verdict"] == "PENDING"
    assert claim["resolved"] is False
    assert contract.get_claim_count() == 1


def test_rejects_non_https_evidence(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy(CONTRACT)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("all evidence URLs must use HTTPS"):
        contract.submit_claim(
            "Invalid source",
            "This statement is intentionally long enough to pass validation.",
            "RECORD_SET_CLAIM_V1",
            json.dumps(["http://insecure.example/data"]),
            "sha256:1234567890abcdef",
            json.dumps({"count": 1}),
            1,
            2,
        )


def test_resolve_partial_verdict(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy(CONTRACT)
    direct_vm.sender = direct_alice
    claim_id = submit_example(contract)

    direct_vm.mock_web(
        r"evidence\.example/audit\.json",
        {
            "status": 200,
            "body": json.dumps(
                {
                    "records": 20,
                    "verified_funding_records": 20,
                    "statuses": {"claimed": 17, "locked": 3},
                }
            ),
        },
    )
    adjudication = {
        "verdict": "PARTIALLY_VERIFIED",
        "confidence_bucket": "HIGH",
        "reason_codes": ["COUNT_MATCH", "STATUS_SCOPE_MISMATCH"],
        "established_facts": {
            "terminal_deal_count": "20",
            "verified_funding_record_count": "20",
        },
        "critical_facts": {"claimed_count": "17", "locked_count": "3"},
        "unsupported_elements": ["All twenty records were claimed."],
        "contradictory_elements": ["Three records were locked."],
        "explanation": "Funding records verify, but status wording is too broad.",
    }
    direct_vm.mock_llm(r".*adjudicating a bounded evidence claim.*", adjudication)

    assert contract.resolve_claim(claim_id) == "PARTIALLY_VERIFIED"
    stored = contract.get_claim(claim_id)
    assert stored["resolved"] is True
    assert stored["reason_codes"] == ["COUNT_MATCH", "STATUS_SCOPE_MISMATCH"]


def test_cannot_resolve_twice(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy(CONTRACT)
    direct_vm.sender = direct_alice
    claim_id = submit_example(contract)
    direct_vm.mock_web(r"evidence\.example/audit\.json", {"status": 200, "body": "{}"})
    result = {
        "verdict": "INSUFFICIENT_EVIDENCE",
        "confidence_bucket": "HIGH",
        "reason_codes": ["MISSING_PRIMARY_SOURCE"],
        "established_facts": {},
        "critical_facts": {},
        "unsupported_elements": ["No records supplied."],
        "contradictory_elements": [],
        "explanation": "The source contains no usable records.",
    }
    direct_vm.mock_llm(r".*adjudicating a bounded evidence claim.*", result)
    contract.resolve_claim(claim_id)
    with direct_vm.expect_revert("claim is already resolved"):
        contract.resolve_claim(claim_id)


def test_validator_rejects_material_disagreement(
    direct_vm, direct_deploy, direct_alice
):
    contract = direct_deploy(CONTRACT)
    direct_vm.sender = direct_alice
    claim_id = submit_example(contract)
    direct_vm.mock_web(
        r"evidence\.example/audit\.json", {"status": 200, "body": "records: 20"}
    )
    leader_result = {
        "verdict": "VERIFIED",
        "confidence_bucket": "HIGH",
        "reason_codes": ["COUNT_MATCH"],
        "established_facts": {"record_count": "20"},
        "critical_facts": {"record_count": "20"},
        "unsupported_elements": [],
        "contradictory_elements": [],
        "explanation": "All material elements are supported.",
    }
    direct_vm.mock_llm(r".*adjudicating a bounded evidence claim.*", leader_result)
    contract.resolve_claim(claim_id)

    direct_vm.clear_mocks()
    direct_vm.mock_web(
        r"evidence\.example/audit\.json", {"status": 200, "body": "records: 20"}
    )
    validator_result = dict(leader_result)
    validator_result["verdict"] = "PARTIALLY_VERIFIED"
    validator_result["reason_codes"] = ["STATUS_SCOPE_MISMATCH"]
    direct_vm.mock_llm(r".*adjudicating a bounded evidence claim.*", validator_result)

    assert direct_vm.run_validator() is False
