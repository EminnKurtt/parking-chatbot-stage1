from guardrails.pii_filter import PIIGuardrail

def test_pii_detection():
    guardrail = PIIGuardrail()
    assert guardrail.contains_sensitive_data("My credit card is 4111-1111-1111-1111") is True

def test_pii_masking():
    guardrail = PIIGuardrail()
    masked = guardrail.analyze_and_mask("Call me at 555-123-4567")
    assert "555-123-4567" not in masked
    assert "<PHONE_NUMBER>" in masked