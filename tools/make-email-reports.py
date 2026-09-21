#!/usr/bin/env python3
"""Write credential-free mail inventory from tracked release behavior."""
import json
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/"reports"; NOW=datetime.now(timezone.utc).isoformat()
providers=[
 {"provider":"Google Apps Script","id":"appsscript","status":"CONFIGURED_TOKEN_UNWIRED","sendable_in_tracked_release":False,"delivery_verification":"NOT_RUN"},
 {"provider":"Web3Forms","id":"web3forms","status":"CONFIGURED_NOT_LIVE_VERIFIED","sendable_in_tracked_release":True,"delivery_verification":"NOT_RUN"},
 {"provider":"StaticForms","id":"staticforms","status":"RETIRED","sendable_in_tracked_release":False,"delivery_verification":"NOT_APPLICABLE"},
 {"provider":"FormSubmit","id":"formsubmit","status":"RETIRED","sendable_in_tracked_release":False,"delivery_verification":"NOT_APPLICABLE"},
 {"provider":"EmailJS","id":"emailjs","status":"NOT_CONFIGURED","sendable_in_tracked_release":False,"delivery_verification":"NOT_RUN"},
]
inv={"generated":NOW,"evidence_scope":"tracked configuration and static suites only","limitations":["No inbox receipt was verified.","The tracked Apps Script token is intentionally empty.","ACCEPTED is not proof of delivery.","No credential or relay key is serialized."],"providers":providers}
roles={x:["appsscript","web3forms"] for x in ["booking_student","booking_tutor","booking_internal","contact_visitor","contact_internal","admin_outbound","admin_internal_copy"]}
mat={"generated":NOW,"release_state":"STATIC_TESTS_PASS_LIVE_DELIVERY_NOT_VERIFIED","roles":roles,"providers":[{"provider":p["provider"],"id":p["id"],"status":p["status"],"delivery_verification":p["delivery_verification"],"credential_values_in_report":False} for p in providers]}
OUT.mkdir(exist_ok=True)
(OUT/"email-provider-inventory.json").write_text(json.dumps(inv,indent=2)+"\n")
(OUT/"email-provider-matrix.json").write_text(json.dumps(mat,indent=2)+"\n")
print("email provider reports: credential-free; live delivery NOT_RUN")
