"""
TracePath Open GS1 Digital Link Validator
Syntax checking and normalization utility for GS1 Digital Link URIs (ESPR 2027 compliant).
"""

import re
from typing import Dict, Optional

GS1_DIGITAL_LINK_PATTERN = re.compile(
    r'^https?://[^/]+/01/(?P<gtin>\d{13,14})(?:/21/(?P<serial>[^/]+))?'
)

def validate_gs1_digital_link(url: str) -> Dict[str, Optional[str]]:
    match = GS1_DIGITAL_LINK_PATTERN.match(url)
    if not match:
        return {"valid": False, "error": "Invalid GS1 Digital Link URI syntax."}
    
    gtin = match.group("gtin")
    serial = match.group("serial")
    
    return {
        "valid": True,
        "gtin": gtin,
        "serial": serial,
        "standard": "GS1 Digital Link 1.2 Syntax"
    }

if __name__ == "__main__":
    sample_uri = "https://tracepath.eu/01/00292910038388/21/SN-948202"
    result = validate_gs1_digital_link(sample_uri)
    print("Validation Result:", result)
