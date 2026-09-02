"""
TracePath GS1 Digital Link Basic Syntax & Check-Digit Validator
Syntax checking and GTIN check-digit verification utility for a limited subset of GS1 Digital Link URIs used in TracePath DPP examples.
"""

import re
from typing import Dict, Optional, Union

# Fullmatch regex for GS1 Digital Link URIs (/01/{gtin}/21/{serial}) with optional query parameters
GS1_DIGITAL_LINK_PATTERN = re.compile(
    r'^https?://[^/]+/01/(?P<gtin>\d{8}|\d{12}|\d{13}|\d{14})(?:/21/(?P<serial>[^/?#]+))?(?:[?#].*)?$'
)

def verify_gtin_check_digit(gtin: str) -> bool:
    """Calculates Modulo 10 check digit for GTIN-8, GTIN-12, GTIN-13, and GTIN-14."""
    if not gtin.isdigit() or len(gtin) not in (8, 12, 13, 14):
        return False
    
    digits = [int(d) for d in gtin]
    check_digit = digits[-1]
    payload_digits = digits[:-1]
    
    # Reverse payload digits for alternating weights (3, 1, 3, 1...)
    payload_digits.reverse()
    total_sum = sum(d * 3 if idx % 2 == 0 else d * 1 for idx, d in enumerate(payload_digits))
    
    calculated_check_digit = (10 - (total_sum % 10)) % 10
    return calculated_check_digit == check_digit

def validate_gs1_digital_link(url: str) -> Dict[str, Union[bool, Optional[str]]]:
    """Validates GS1 Digital Link URI syntax and GTIN check-digit."""
    if not url or not isinstance(url, str):
        return {"valid": False, "error": "URL must be a non-empty string."}

    match = GS1_DIGITAL_LINK_PATTERN.fullmatch(url.strip())
    if not match:
        return {
            "valid": False,
            "error": "Invalid GS1 Digital Link URI syntax. Expected pattern: https://domain/01/{gtin}/21/{serial}"
        }
    
    gtin = match.group("gtin")
    serial = match.group("serial")
    
    if not verify_gtin_check_digit(gtin):
        return {
            "valid": False,
            "error": f"Invalid GTIN check digit for GTIN: {gtin}",
            "gtin": gtin
        }

    return {
        "valid": True,
        "gtin": gtin,
        "serial": serial,
        "check_digit_verified": True,
        "standard": "TracePath GS1 Digital Link Basic Syntax Checker"
    }

if __name__ == "__main__":
    # Test valid GTIN-14 with valid Modulo 10 check digit
    sample_uri = "https://tracepath.eu/01/00292910038388/21/SN-948202"
    result = validate_gs1_digital_link(sample_uri)
    print("Validation Result:", result)
