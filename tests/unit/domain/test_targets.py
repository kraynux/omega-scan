# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
import pytest

from omega_scan.domain.targets.exceptions import TargetParseError
from omega_scan.domain.targets.service import is_authorized, pin_target
from omega_scan.domain.targets.validation import parse_target


def test_parse_target_hostname_with_path():
    target = parse_target("intranet.lan:8080/admin")
    assert target.normalized_host == "intranet.lan"
    assert target.requested_port == 8080
    assert target.requested_path == "/admin"
    assert target.target_kind == "hostname"
    assert target.scope_kind == "hostname"
    assert target.scan_modes == "both"


def test_parse_target_ipv4_private_lan():
    target = parse_target("192.168.1.10:8080")
    assert target.is_ip is True
    assert target.ip_version == 4
    assert target.target_kind == "ipv4"
    assert target.scope_kind == "private_lan"


def test_parse_target_ipv6_bracketed_with_port():
    target = parse_target("[2001:db8::10]:8443")
    assert target.is_ip is True
    assert target.ip_version == 6
    assert target.target_kind == "ipv6"


def test_parse_target_ipv6_without_brackets():
    target = parse_target("::1")
    assert target.is_ip is True
    assert target.scope_kind == "loopback"


def test_parse_target_url_with_scheme():
    target = parse_target("https://example.org/api")
    assert target.requested_scheme == "https"
    assert target.scan_modes == "https"
    assert target.requested_path == "/api"


def test_parse_target_empty_raises():
    with pytest.raises(TargetParseError):
        parse_target("   ")


def test_pin_target_then_is_authorized():
    target = parse_target("example.org")
    pinned = pin_target(target, now_iso="2026-08-26T10:00:00Z", note="autorise par le client")
    assert pinned.authorized is True
    assert pinned.normalized_host == "example.org"
    assert is_authorized([pinned], target) is True


def test_is_authorized_false_when_not_pinned():
    target = parse_target("unknown.example.org")
    assert is_authorized([], target) is False
