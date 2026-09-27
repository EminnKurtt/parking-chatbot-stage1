import re
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine


class PIIGuardrail:
    def __init__(self):
        # Regex patterns as a reliable first layer of defense
        self.patterns = {
            "CREDIT_CARD": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
            "PHONE_NUMBER": re.compile(r"\b(?:\+?\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}\b"),
            "EMAIL_ADDRESS": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
            "US_SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
        }

        # Try to initialize Presidio (NLP layer) - fallback to regex only if it fails
        try:
            self.analyzer = AnalyzerEngine()
            self.anonymizer = AnonymizerEngine()
            self._presidio_available = True
            print("[PIIGuardrail] Presidio NLP engine initialized successfully.")
        except Exception as e:
            self.analyzer = None
            self.anonymizer = None
            self._presidio_available = False
            print(f"[PIIGuardrail] Presidio failed to initialize ({e}). Using regex-only mode.")

    def contains_sensitive_data(self, text: str) -> bool:
        """Returns True if any sensitive data pattern is matched (regex or NLP)."""
        # Layer 1: Regex check (fast and reliable)
        for entity_type, pattern in self.patterns.items():
            if pattern.search(text):
                return True

        # Layer 2: Presidio NLP check (if available)
        if self._presidio_available:
            try:
                results = self.analyzer.analyze(text=text, language='en')
                sensitive_entities = ["CREDIT_CARD", "PHONE_NUMBER", "EMAIL_ADDRESS", "US_SSN"]
                return any(result.entity_type in sensitive_entities for result in results)
            except Exception as e:
                # Silently fall back to regex result if Presidio errors
                print(f"[PIIGuardrail] Presidio analyze error (ignored): {e}")
                return False

        return False

    def analyze_and_mask(self, text: str) -> str:
        """Masks any detected PII in the given text."""
        masked_text = text

        # Layer 1: Regex masking
        for entity_type, pattern in self.patterns.items():
            masked_text = pattern.sub(f"<{entity_type}>", masked_text)

        # Layer 2: Presidio NLP masking (if available)
        if self._presidio_available:
            try:
                results = self.analyzer.analyze(text=masked_text, language='en')
                if results:
                    anonymized = self.anonymizer.anonymize(text=masked_text, analyzer_results=results)
                    return anonymized.text
            except Exception as e:
                print(f"[PIIGuardrail] Presidio anonymize error (ignored): {e}")
                return masked_text

        return masked_text