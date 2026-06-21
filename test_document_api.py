"""
test_document_api.py — API tests for document management endpoints.

Covers:
    POST   /api/documents/upload     – file upload (PDF, DOCX)
    GET    /api/documents            – list all documents
    GET    /api/documents/{id}       – retrieve single document
    GET    /api/documents/search     – keyword search
    DELETE /api/documents/{id}       – delete a document
    GET    /api/documents/stats      – aggregate statistics

All tests are marked with ``@pytest.mark.api``.
"""

import os

import pytest
import requests

# Every test in this module is an API test
pytestmark = pytest.mark.api


# ═══════════════════════════════════════════════════════════════════════════════
#  Helper — Upload a file and return the response
# ═══════════════════════════════════════════════════════════════════════════════

def _upload_file(base_url: str, headers: dict, file_path: str) -> requests.Response:
    """Upload a file to the documents endpoint and return the raw response.

    Uses ``multipart/form-data`` with the field name ``file``.
    """
    filename = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        files = {"file": (filename, f, "application/octet-stream")}
        return requests.post(
            f"{base_url}/documents/upload",
            headers=headers,
            files=files,
            timeout=30,
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  Upload Tests
# ═══════════════════════════════════════════════════════════════════════════════


class TestDocumentUpload:
    """Tests for POST /api/documents/upload."""

    def test_upload_pdf(self, base_url, auth_headers, sample_pdf_path):
        """Uploading a valid PDF should return 201 with document metadata.

        Steps:
            1. POST the sample PDF as multipart form data.
            2. Assert 201 Created.
            3. Assert response contains document information (id, filename, etc.).
        """
        response = _upload_file(base_url, auth_headers, sample_pdf_path)

        assert response.status_code in (200, 201), (
            f"Expected 200/201 but got {response.status_code}: {response.text}"
        )

        data = response.json()
        # The response should include at least an id and a filename/name
        assert "id" in data or "documentId" in data, (
            f"Response missing document ID: {data}"
        )

    def test_upload_docx(self, base_url, auth_headers, sample_docx_path):
        """Uploading a valid DOCX should return 201 with document metadata.

        Mirrors test_upload_pdf but for the Word format.
        """
        response = _upload_file(base_url, auth_headers, sample_docx_path)

        assert response.status_code in (200, 201), (
            f"Expected 200/201 but got {response.status_code}: {response.text}"
        )

        data = response.json()
        assert "id" in data or "documentId" in data, (
            f"Response missing document ID: {data}"
        )

    def test_upload_no_file(self, base_url, auth_headers):
        """Submitting an upload request without attaching a file should return 400.

        Validates server-side request-body validation.
        """
        response = requests.post(
            f"{base_url}/documents/upload",
            headers=auth_headers,
            timeout=15,
        )

        assert response.status_code == 400, (
            f"Expected 400 for missing file but got {response.status_code}"
        )

    def test_upload_without_auth(self, base_url, sample_pdf_path):
        """Uploading without an Authorization header should be rejected (401/403).

        Confirms the endpoint is protected.
        """
        with open(sample_pdf_path, "rb") as f:
            files = {"file": ("sample.pdf", f, "application/pdf")}
            response = requests.post(
                f"{base_url}/documents/upload",
                files=files,
                timeout=15,
            )

        assert response.status_code in (401, 403), (
            f"Expected 401/403 but got {response.status_code}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  List / Get Tests
# ═══════════════════════════════════════════════════════════════════════════════


class TestDocumentRetrieval:
    """Tests for GET /api/documents and GET /api/documents/{id}."""

    def test_list_documents(self, base_url, auth_headers, sample_pdf_path, sample_docx_path):
        """After uploading two files the document list should contain at least 2 entries.

        Steps:
            1. Upload a PDF and a DOCX.
            2. GET /api/documents.
            3. Assert 200 and list length >= 2.
        """
        # Upload two distinct documents
        _upload_file(base_url, auth_headers, sample_pdf_path)
        _upload_file(base_url, auth_headers, sample_docx_path)

        response = requests.get(
            f"{base_url}/documents",
            headers=auth_headers,
            timeout=15,
        )

        assert response.status_code == 200
        data = response.json()

        # The response might be a list directly or wrapped in a key
        doc_list = data if isinstance(data, list) else data.get("documents", data.get("content", []))
        assert len(doc_list) >= 2, (
            f"Expected >= 2 documents but got {len(doc_list)}"
        )

    def test_get_document_by_id(self, base_url, auth_headers, sample_pdf_path):
        """Fetching a single document by its ID should return the correct record.

        Steps:
            1. Upload a file and capture its ID.
            2. GET /api/documents/{id}.
            3. Assert 200 and the returned ID matches.
        """
        upload_resp = _upload_file(base_url, auth_headers, sample_pdf_path)
        upload_data = upload_resp.json()
        doc_id = upload_data.get("id") or upload_data.get("documentId")

        response = requests.get(
            f"{base_url}/documents/{doc_id}",
            headers=auth_headers,
            timeout=15,
        )

        assert response.status_code == 200, (
            f"Expected 200 but got {response.status_code}"
        )

        data = response.json()
        returned_id = data.get("id") or data.get("documentId")
        assert str(returned_id) == str(doc_id), (
            f"ID mismatch: expected {doc_id}, got {returned_id}"
        )

    def test_get_nonexistent_document(self, base_url, auth_headers):
        """Requesting a document ID that does not exist should return 404.

        Uses a very high ID that is unlikely to exist in the database.
        """
        response = requests.get(
            f"{base_url}/documents/99999",
            headers=auth_headers,
            timeout=15,
        )

        assert response.status_code == 404, (
            f"Expected 404 but got {response.status_code}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  Search Tests
# ═══════════════════════════════════════════════════════════════════════════════


class TestDocumentSearch:
    """Tests for GET /api/documents/search."""

    def test_search_documents(self, base_url, auth_headers, sample_pdf_path):
        """Searching with a keyword present in the uploaded PDF should return results.

        The sample PDF contains the word 'automation'.
        """
        # Ensure the searchable document exists
        _upload_file(base_url, auth_headers, sample_pdf_path)

        response = requests.get(
            f"{base_url}/documents/search",
            params={"keyword": "automation"},
            headers=auth_headers,
            timeout=15,
        )

        assert response.status_code == 200, (
            f"Expected 200 but got {response.status_code}"
        )

        data = response.json()
        results = data if isinstance(data, list) else data.get("results", data.get("documents", []))
        assert len(results) >= 1, (
            f"Expected at least 1 search result for 'automation', got {len(results)}"
        )

    def test_search_no_results(self, base_url, auth_headers):
        """Searching for a gibberish keyword should return 200 with an empty list.

        The API should never 404 on a valid search — an empty result set is
        the correct behaviour.
        """
        response = requests.get(
            f"{base_url}/documents/search",
            params={"keyword": "xyzzy_nonexistent_keyword_42"},
            headers=auth_headers,
            timeout=15,
        )

        assert response.status_code == 200

        data = response.json()
        results = data if isinstance(data, list) else data.get("results", data.get("documents", []))
        assert len(results) == 0, (
            f"Expected 0 results for gibberish keyword, got {len(results)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  Delete Tests
# ═══════════════════════════════════════════════════════════════════════════════


class TestDocumentDeletion:
    """Tests for DELETE /api/documents/{id}."""

    def test_delete_document(self, base_url, auth_headers, sample_pdf_path):
        """Deleting an existing document should return 204 (or 200) and the
        document should no longer be retrievable.

        Steps:
            1. Upload a document.
            2. DELETE /api/documents/{id} → 200/204.
            3. GET /api/documents/{id} → 404 (confirm removal).
        """
        upload_resp = _upload_file(base_url, auth_headers, sample_pdf_path)
        upload_data = upload_resp.json()
        doc_id = upload_data.get("id") or upload_data.get("documentId")

        # Delete the document
        del_response = requests.delete(
            f"{base_url}/documents/{doc_id}",
            headers=auth_headers,
            timeout=15,
        )

        assert del_response.status_code in (200, 204), (
            f"Expected 200/204 but got {del_response.status_code}"
        )

        # Verify it is actually gone
        get_response = requests.get(
            f"{base_url}/documents/{doc_id}",
            headers=auth_headers,
            timeout=15,
        )

        assert get_response.status_code == 404, (
            f"Document still exists after deletion: {get_response.status_code}"
        )

    def test_delete_nonexistent_document(self, base_url, auth_headers):
        """Attempting to delete a non-existent document should return 404."""
        response = requests.delete(
            f"{base_url}/documents/99999",
            headers=auth_headers,
            timeout=15,
        )

        assert response.status_code == 404, (
            f"Expected 404 but got {response.status_code}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  Stats Tests
# ═══════════════════════════════════════════════════════════════════════════════


class TestDocumentStats:
    """Tests for GET /api/documents/stats."""

    def test_get_stats(self, base_url, auth_headers, sample_pdf_path, sample_docx_path):
        """The stats endpoint should return aggregate document counts and type breakdowns.

        Steps:
            1. Upload a PDF and a DOCX to ensure data exists.
            2. GET /api/documents/stats.
            3. Assert 200 and the presence of ``totalDocuments`` and ``typeCounts``.
        """
        # Seed the database with at least two documents
        _upload_file(base_url, auth_headers, sample_pdf_path)
        _upload_file(base_url, auth_headers, sample_docx_path)

        response = requests.get(
            f"{base_url}/documents/stats",
            headers=auth_headers,
            timeout=15,
        )

        assert response.status_code == 200, (
            f"Expected 200 but got {response.status_code}"
        )

        data = response.json()

        # The stats payload must include total count and per-type breakdown
        assert "totalDocuments" in data or "total" in data, (
            f"Stats response missing totalDocuments: {data}"
        )
        assert "typeCounts" in data or "types" in data or "fileTypes" in data, (
            f"Stats response missing typeCounts: {data}"
        )
