import json


CONTRACT = "contracts/evidence_bound.py"


def submit_example(contract):
    return contract.submit_claim(
        "Kirago funding-record audit",
        "Twenty claimed deals were checked and all funding records were verified.",
        "RECORD_SET_CLAIM_V1",
        json.dumps(["https://evidence.example/audit.json"]),
        "sha256:1234567890abcdef",
        json.dumps({"claimed_records": 20, "funding_records_verified": 20}),
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
    extracted_facts = {
        "total_records": 20,
        "claimed_records": 17,
        "locked_records": 3,
        "other_records": 0,
        "funding_records_verified": 20,
        "funding_mismatches": 0,
        "source_sufficient": True,
    }
    direct_vm.mock_llm(r".*Extract a fixed set of numeric facts.*", extracted_facts)

    assert contract.resolve_claim(claim_id) == "PARTIALLY_VERIFIED"
    stored = contract.get_claim(claim_id)
    assert stored["resolved"] is True
    assert stored["confidence_bucket"] == "HIGH"
    assert stored["reason_codes"] == ["CLAIMED_RECORDS_MISMATCH"]
    assert stored["established_facts"]["locked_records"] == 3


def test_cannot_resolve_twice(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy(CONTRACT)
    direct_vm.sender = direct_alice
    claim_id = submit_example(contract)
    direct_vm.mock_web(r"evidence\.example/audit\.json", {"status": 200, "body": "{}"})
    result = {
        "total_records": 0,
        "claimed_records": 0,
        "locked_records": 0,
        "other_records": 0,
        "funding_records_verified": 0,
        "funding_mismatches": 0,
        "source_sufficient": False,
    }
    direct_vm.mock_llm(r".*Extract a fixed set of numeric facts.*", result)
    contract.resolve_claim(claim_id)
    with direct_vm.expect_revert("claim is already resolved"):
        contract.resolve_claim(claim_id)


def test_validator_rejects_material_disagreement(
    direct_vm, direct_deploy, direct_alice, monkeypatch
):
    contract = direct_deploy(CONTRACT)
    direct_vm.sender = direct_alice
    claim_id = submit_example(contract)
    direct_vm.mock_web(
        r"evidence\.example/audit\.json", {"status": 200, "body": "records: 20"}
    )
    leader_result = {
        "total_records": 20,
        "claimed_records": 17,
        "locked_records": 3,
        "other_records": 0,
        "funding_records_verified": 20,
        "funding_mismatches": 0,
        "source_sufficient": True,
    }
    direct_vm.mock_llm(r".*Extract a fixed set of numeric facts.*", leader_result)
    contract.resolve_claim(claim_id)

    direct_vm.clear_mocks()
    direct_vm.mock_web(
        r"evidence\.example/audit\.json", {"status": 200, "body": "records: 20"}
    )
    validator_result = dict(leader_result)
    validator_result["claimed_records"] = 18
    direct_vm.mock_llm(r".*Extract a fixed set of numeric facts.*", validator_result)

    # Direct mode does not implement GenVM's isolated spawn_sandbox response
    # protocol. Execute the captured extraction function directly while keeping
    # strict_eq's production comparison unchanged.
    import genlayer.gl.vm as gl_vm

    monkeypatch.setattr(
        gl_vm, "spawn_sandbox", lambda fn: gl_vm.Return(calldata=fn())
    )

    assert direct_vm.run_validator() is False
