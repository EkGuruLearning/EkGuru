"""Classification for Apps Script GET probes used in CI."""

from urllib.error import HTTPError


def is_unverified_appscript_403(error: BaseException) -> bool:
    """Return true for HTTP 403, whose cause cannot be established from CI.

    A 403 may be Google anti-abuse gating a datacenter runner or an actual
    access/deployment problem. It is never evidence of a healthy endpoint;
    callers should report it as unverified while keeping independent checks
    (such as the published Sheet data/schema checks) authoritative.
    """
    return isinstance(error, HTTPError) and error.code == 403
