# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
"""Tests d'integration des probers reseau, contre un serveur HTTP factice
(pytest-httpserver) plutot que le reseau reel."""
from __future__ import annotations

import re
import ssl
import threading

import trustme
from pytest_httpserver import HTTPServer
from werkzeug.wrappers import Request, Response

from omega_scan.domain.profiles.models import ScanProfile
from omega_scan.domain.targets.validation import parse_target
from omega_scan.infrastructure.network.httpx_connectivity_prober import HttpxConnectivityProber
from omega_scan.infrastructure.network.httpx_http_prober import HttpxHttpProber
from omega_scan.infrastructure.network.httpx_methods_prober import HttpxMethodsProber
from omega_scan.infrastructure.network.httpx_path_prober import HttpxPathProber
from omega_scan.infrastructure.network.httpx_tls_prober import HttpxTlsProber


def _fast_profile(**overrides):
    base = {
        "profile_name": "test",
        "timeout_connect": 2,
        "timeout_read": 2,
        "http_methods_tested": ["OPTIONS"],
        "path_checks_enabled": True,
        "path_probe_delay_ms": 0,
        "path_probe_max_targets": 1,
        "tls_checks_enabled": False,
        "follow_redirects": True,
        "max_redirects": 5,
        "user_agent": "Omega-scan/test",
    }
    base.update(overrides)
    return ScanProfile(**base)


def test_http_prober_captures_nominal_response(httpserver: HTTPServer):
    httpserver.expect_request("/").respond_with_data(
        "<html><head></head><body>ok</body></html>",
        content_type="text/html",
    )
    target = parse_target(f"http://{httpserver.host}:{httpserver.port}/")

    result = HttpxHttpProber().probe(target, _fast_profile(), errors=[])

    assert result["http"]["ok"] is True
    assert result["http"]["status_code"] == 200
    assert result["overview"]["preferred_scheme"] == "http"
    assert result["overview"]["content_profile"] == "html_page"


def test_http_prober_detects_wildcard_credentials_cors(httpserver: HTTPServer):
    httpserver.expect_request("/").respond_with_data(
        "ok",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
        },
    )
    target = parse_target(f"http://{httpserver.host}:{httpserver.port}/")

    result = HttpxHttpProber().probe(target, _fast_profile(), errors=[])

    assert result["cors"]["attempted"] is True
    assert result["cors"]["allow_origin"] == "*"
    assert result["cors"]["allow_credentials"] is True


def test_http_prober_detects_reflected_origin_cors(httpserver: HTTPServer):
    def _reflect_origin(request: Request) -> Response:
        return Response("ok", headers={"Access-Control-Allow-Origin": request.headers.get("Origin", "")})

    httpserver.expect_request("/").respond_with_handler(_reflect_origin)
    target = parse_target(f"http://{httpserver.host}:{httpserver.port}/")

    result = HttpxHttpProber().probe(target, _fast_profile(), errors=[])

    assert result["cors"]["attempted"] is True
    assert result["cors"]["reflects_arbitrary_origin"] is True


def test_http_prober_captures_cookie_httponly_and_samesite(httpserver: HTTPServer):
    httpserver.expect_request("/").respond_with_data(
        "ok",
        headers={"Set-Cookie": "session=abc; Path=/; HttpOnly; SameSite=Lax"},
    )
    target = parse_target(f"http://{httpserver.host}:{httpserver.port}/")

    result = HttpxHttpProber().probe(target, _fast_profile(), errors=[])

    cookie = result["http"]["cookies"][0]
    assert cookie["httponly"] is True
    assert cookie["samesite"] == "Lax"


def test_http_prober_skips_cors_probe_when_path_checks_disabled(httpserver: HTTPServer):
    httpserver.expect_request("/").respond_with_data("ok")
    target = parse_target(f"http://{httpserver.host}:{httpserver.port}/")

    result = HttpxHttpProber().probe(
        target, _fast_profile(path_checks_enabled=False), errors=[]
    )

    assert result["cors"]["attempted"] is False


def test_connectivity_prober_marks_http_reachable(httpserver: HTTPServer):
    httpserver.expect_request("/").respond_with_data("ok")
    target = parse_target(f"http://{httpserver.host}:{httpserver.port}/")

    result = HttpxConnectivityProber().probe(target, _fast_profile(), errors=[])

    assert result["http_reachable"] is True
    assert result["first_successful_scheme"] == "http"


def test_connectivity_prober_reports_unreachable_target():
    target = parse_target("http://127.0.0.1:1/")  # port improbable, connexion refusee attendue

    errors: list = []
    result = HttpxConnectivityProber().probe(target, _fast_profile(), errors)

    assert result["http_reachable"] is False


def test_methods_prober_reports_options_allow_header(httpserver: HTTPServer):
    httpserver.expect_request("/", method="OPTIONS").respond_with_data(
        "", headers={"Allow": "GET, HEAD, OPTIONS"}
    )
    httpserver.expect_request("/", method="GET").respond_with_data("ok")
    target = parse_target(f"http://{httpserver.host}:{httpserver.port}/")
    http_data = {"overview": {"preferred_scheme": "http"}, "http": {"final_url": httpserver.url_for("/")}}

    result = HttpxMethodsProber().probe(target, _fast_profile(http_methods_tested=["OPTIONS"]), http_data, errors=[])

    assert result["methods_tested"][0]["method"] == "OPTIONS"
    assert result["methods_tested"][0]["allow_header"] == "GET, HEAD, OPTIONS"


def test_path_prober_detects_catch_all_when_everything_returns_200(httpserver: HTTPServer):
    httpserver.expect_request(re.compile(r"^/.*$")).respond_with_data(
        "<html><head></head><body>catch-all</body></html>", content_type="text/html"
    )
    target = parse_target(f"http://{httpserver.host}:{httpserver.port}/")
    base_url = httpserver.url_for("/")
    http_data = {
        "overview": {"preferred_scheme": "http", "content_profile": "html_page"},
        "http": {"final_url": base_url},
    }

    result = HttpxPathProber().probe(target, _fast_profile(), http_data, errors=[])

    assert result["catch_all_suspected"] is True


def test_path_prober_does_not_flag_catch_all_on_404(httpserver: HTTPServer):
    httpserver.expect_request(re.compile(r"^/.*$")).respond_with_data("not found", status=404)
    target = parse_target(f"http://{httpserver.host}:{httpserver.port}/")
    base_url = httpserver.url_for("/")
    http_data = {
        "overview": {"preferred_scheme": "http", "content_profile": "unknown"},
        "http": {"final_url": base_url},
    }

    result = HttpxPathProber().probe(target, _fast_profile(), http_data, errors=[])

    assert result["catch_all_suspected"] is False


def test_tls_prober_reports_untrusted_certificate_without_raising():
    ca = trustme.CA()
    server_cert = ca.issue_cert("localhost")
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    server_cert.configure_cert(context)

    import socket

    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_socket.bind(("localhost", 0))
    raw_socket.listen(1)
    port = raw_socket.getsockname()[1]

    def _serve_once() -> None:
        try:
            client_socket, _ = raw_socket.accept()
            with context.wrap_socket(client_socket, server_side=True) as tls_client:
                tls_client.recv(1)
        except OSError:
            pass

    thread = threading.Thread(target=_serve_once, daemon=True)
    thread.start()

    target = parse_target(f"https://localhost:{port}/")
    profile = _fast_profile(tls_checks_enabled=True)

    result = HttpxTlsProber().probe(target, profile, errors=[])

    thread.join(timeout=2)

    # Le CA de trustme n'est pas dans le magasin de confiance du client :
    # le handshake TLS reussit techniquement mais la verification de la
    # chaine echoue (ssl.SSLCertVerificationError) - la meme branche que
    # v1 prend pour un certificat auto-signe ou une CA inconnue. Le detail
    # du certificat (certificate_present, etc.) n'est jamais extrait dans
    # ce cas : getpeercert() n'est atteint que sur le chemin de succes.
    assert result["attempted"] is True
    assert result["handshake_success"] is True
    assert result["validation_error"] is not None
    assert result["certificate_present"] is False
