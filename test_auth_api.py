"""
test_auth_api.py — API tests for the authentication endpoints.

Covers:
    POST /api/auth/register   – user registration
    POST /api/auth/login      – user login / JWT issuance
    GET  /api/documents       – protected-route access control

All tests are marked with ``@pytest.mark.api`` so they can be run in
isolation with ``pytest -m api``.
"""

import pytest
import requests
from faker import Faker

fake = Faker()

# Every test in this module is an API test
pytestmark = pytest.mark.api


# ═══════════════════════════════════════════════════════════════════════════════
#  Registration Tests
# ═══════════════════════════════════════════════════════════════════════════════


class TestRegister:
    """Tests for POST /api/auth/register."""

    def test_register_success(self, base_url, test_user):
        """Registering with valid, unique credentials should return 200 and a JWT token.

        Steps:
            1. POST a fresh user payload to /auth/register.
            2. Assert HTTP 200 (or 201).
            3. Assert the response body contains a 'token' key.
        """
        response = requests.post(
            f"{base_url}/auth/register",
            json=test_user,
            timeout=15,
        )

        assert response.status_code in (200, 201), (
            f"Expected 200/201 but got {response.status_code}: {response.text}"
        )

        data = response.json()
        # The backend should issue a token immediately upon registration
        assert "token" in data or "accessToken" in data, (
            f"Response missing 'token' key: {data}"
        )

    def test_register_duplicate_username(self, base_url, test_user):
        """Attempting to register the same username twice should return 400.

        Steps:
            1. Register a user.
            2. POST the same payload again.
            3. Assert HTTP 400 (duplicate / conflict).
        """
        # First registration — should succeed
        requests.post(f"{base_url}/auth/register", json=test_user, timeout=15)

        # Second registration — same username
        response = requests.post(
            f"{base_url}/auth/register",
            json=test_user,
            timeout=15,
        )

        assert response.status_code in (400, 409), (
            f"Expected 400/409 for duplicate but got {response.status_code}"
        )

    def test_register_missing_fields(self, base_url):
        """Sending an empty body to the registration endpoint should return 400.

        The server must validate that required fields (username, email,
        password) are present.
        """
        response = requests.post(
            f"{base_url}/auth/register",
            json={},
            timeout=15,
        )

        assert response.status_code == 400, (
            f"Expected 400 for empty body but got {response.status_code}"
        )

    def test_register_invalid_email(self, base_url):
        """Registering with a syntactically invalid email should return 400.

        Validates server-side email format checking.
        """
        payload = {
            "username": fake.user_name() + fake.bothify("##??"),
            "email": "not-a-valid-email",
            "password": fake.password(length=12),
        }

        response = requests.post(
            f"{base_url}/auth/register",
            json=payload,
            timeout=15,
        )

        assert response.status_code == 400, (
            f"Expected 400 for invalid email but got {response.status_code}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  Login Tests
# ═══════════════════════════════════════════════════════════════════════════════


class TestLogin:
    """Tests for POST /api/auth/login."""

    def test_login_success(self, base_url, registered_user):
        """Logging in with correct credentials should return 200 and a JWT.

        Steps:
            1. Use the ``registered_user`` fixture (already registered).
            2. POST username + password to /auth/login.
            3. Assert 200 and presence of 'token'.
        """
        login_payload = {
            "username": registered_user["username"],
            "password": registered_user["password"],
        }

        response = requests.post(
            f"{base_url}/auth/login",
            json=login_payload,
            timeout=15,
        )

        assert response.status_code == 200, (
            f"Expected 200 but got {response.status_code}: {response.text}"
        )

        data = response.json()
        assert "token" in data or "accessToken" in data, (
            f"Response missing 'token': {data}"
        )

    def test_login_wrong_password(self, base_url, registered_user):
        """Using the wrong password should return 401 Unauthorized.

        The server must not leak whether the username exists.
        """
        login_payload = {
            "username": registered_user["username"],
            "password": "Wr0ng_P@ssw0rd!",
        }

        response = requests.post(
            f"{base_url}/auth/login",
            json=login_payload,
            timeout=15,
        )

        assert response.status_code == 401, (
            f"Expected 401 but got {response.status_code}"
        )

    def test_login_nonexistent_user(self, base_url):
        """Logging in with a username that was never registered should return 401.

        Prevents user-enumeration attacks.
        """
        login_payload = {
            "username": f"nonexistent_{fake.bothify('????????')}",
            "password": fake.password(length=12),
        }

        response = requests.post(
            f"{base_url}/auth/login",
            json=login_payload,
            timeout=15,
        )

        assert response.status_code == 401, (
            f"Expected 401 but got {response.status_code}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  Protected Route Access Control
# ═══════════════════════════════════════════════════════════════════════════════


class TestProtectedAccess:
    """Verify that protected endpoints enforce authentication correctly."""

    def test_access_protected_without_token(self, base_url):
        """Accessing /api/documents without any Authorization header should be denied.

        Expected: 401 Unauthorized or 403 Forbidden.
        """
        response = requests.get(
            f"{base_url}/documents",
            timeout=15,
        )

        assert response.status_code in (401, 403), (
            f"Expected 401/403 but got {response.status_code}"
        )

    def test_access_protected_with_invalid_token(self, base_url):
        """Sending a garbage JWT should be rejected.

        The server must validate the token signature, not just its presence.
        """
        headers = {"Authorization": "Bearer this.is.not.a.valid.jwt.token"}

        response = requests.get(
            f"{base_url}/documents",
            headers=headers,
            timeout=15,
        )

        assert response.status_code in (401, 403), (
            f"Expected 401/403 but got {response.status_code}"
        )

    def test_access_protected_with_valid_token(self, base_url, auth_headers):
        """A valid JWT should grant access to the protected documents endpoint.

        Uses the ``auth_headers`` fixture which handles registration + login.
        """
        response = requests.get(
            f"{base_url}/documents",
            headers=auth_headers,
            timeout=15,
        )

        assert response.status_code == 200, (
            f"Expected 200 but got {response.status_code}: {response.text}"
        )
