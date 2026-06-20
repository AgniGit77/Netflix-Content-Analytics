package com.docintel.controller;

import com.docintel.dto.DocumentDTO;
import com.docintel.dto.StatsDTO;
import com.docintel.model.User;
import com.docintel.repository.UserRepository;
import com.docintel.service.DocumentService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

/**
 * DocumentController - REST API endpoints for document management.
 *
 * All endpoints in this controller REQUIRE authentication (a valid JWT token
 * in the Authorization header). This is enforced by Spring Security config.
 *
 * ENDPOINTS:
 *   POST   /api/documents/upload     → Upload a new document
 *   GET    /api/documents            → List all documents for the logged-in user
 *   GET    /api/documents/{id}       → Get a single document by ID
 *   GET    /api/documents/search     → Search documents by keyword
 *   DELETE /api/documents/{id}       → Delete a document
 *   GET    /api/documents/stats      → Get dashboard statistics
 *
 * HOW AUTHENTICATION WORKS IN CONTROLLERS:
 *   The @AuthenticationPrincipal annotation injects the currently authenticated
 *   user's details. This is set by our JwtAuthFilter earlier in the request chain.
 *
 *   We then look up the full User entity from the database using the username
 *   from the UserDetails (since UserDetails only contains username + password).
 */
@RestController
@RequestMapping("/api/documents")
public class DocumentController {

    private static final Logger logger = LoggerFactory.getLogger(DocumentController.class);

    @Autowired
    private DocumentService documentService;

    @Autowired
    private UserRepository userRepository;

    /**
     * Upload a new document.
     *
     * Accepts a multipart file upload (PDF or DOCX). The file is:
     *   1. Saved to disk with a unique name
     *   2. Parsed to extract text content
     *   3. Stored in the database with metadata
     *
     * @RequestParam("file") tells Spring to extract the file from the
     * multipart form data field named "file".
     *
     * Returns HTTP 201 (Created) on success, which is the standard
     * status code for resource creation.
     *
     * Example request (using curl):
     *   curl -X POST http://localhost:8080/api/documents/upload \
     *     -H "Authorization: Bearer eyJ..." \
     *     -F "file=@report.pdf"
     *
     * @param file        the uploaded file
     * @param userDetails the authenticated user (injected by Spring Security)
     * @return DocumentDTO with the created document's information
     */
    @PostMapping("/upload")
    public ResponseEntity<DocumentDTO> uploadDocument(
            @RequestParam("file") MultipartFile file,
            @AuthenticationPrincipal UserDetails userDetails) {

        logger.info("Upload request from user: {}, file: {}", userDetails.getUsername(), file.getOriginalFilename());

        // Look up the full User entity from the database
        User user = getCurrentUser(userDetails);

        // Delegate to the service layer
        DocumentDTO document = documentService.uploadDocument(file, user);

        // Return 201 Created with the document data
        return ResponseEntity.status(HttpStatus.CREATED).body(document);
    }

    /**
     * Get all documents for the authenticated user.
     *
     * Returns a list of DocumentDTOs sorted by upload date (newest first).
     * Each DTO includes a text preview (first 500 chars) instead of
     * the full extracted text.
     *
     * @param userDetails the authenticated user
     * @return list of DocumentDTOs
     */
    @GetMapping
    public ResponseEntity<List<DocumentDTO>> getAllDocuments(
            @AuthenticationPrincipal UserDetails userDetails) {

        logger.debug("List documents request from user: {}", userDetails.getUsername());

        User user = getCurrentUser(userDetails);
        List<DocumentDTO> documents = documentService.getAllDocuments(user);

        return ResponseEntity.ok(documents);
    }

    /**
     * Get a single document by its ID.
     *
     * Returns the full document data including ALL extracted text
     * (not just the 500-char preview). Ownership is verified in the service.
     *
     * @PathVariable extracts the {id} from the URL path.
     * Example: GET /api/documents/42 → id = 42
     *
     * @param id          the document ID
     * @param userDetails the authenticated user
     * @return DocumentDTO with full document data
     */
    @GetMapping("/{id}")
    public ResponseEntity<DocumentDTO> getDocument(
            @PathVariable Long id,
            @AuthenticationPrincipal UserDetails userDetails) {

        logger.debug("Get document {} request from user: {}", id, userDetails.getUsername());

        User user = getCurrentUser(userDetails);
        DocumentDTO document = documentService.getDocument(id, user);

        return ResponseEntity.ok(document);
    }

    /**
     * Search documents by keyword.
     *
     * Searches across both file names and extracted text content.
     * The search is case-insensitive and supports partial matches.
     *
     * @RequestParam("keyword") extracts the query parameter from the URL.
     * Example: GET /api/documents/search?keyword=quarterly → keyword = "quarterly"
     *
     * @param keyword     the search term
     * @param userDetails the authenticated user
     * @return list of matching DocumentDTOs
     */
    @GetMapping("/search")
    public ResponseEntity<List<DocumentDTO>> searchDocuments(
            @RequestParam("keyword") String keyword,
            @AuthenticationPrincipal UserDetails userDetails) {

        logger.info("Search request for '{}' from user: {}", keyword, userDetails.getUsername());

        User user = getCurrentUser(userDetails);
        List<DocumentDTO> documents = documentService.searchDocuments(keyword, user);

        return ResponseEntity.ok(documents);
    }

    /**
     * Delete a document by its ID.
     *
     * Deletes both the physical file and the database record.
     * Ownership is verified in the service layer.
     *
     * Returns HTTP 204 (No Content) on success, which is the standard
     * status code for successful deletion with no response body.
     *
     * @param id          the document ID to delete
     * @param userDetails the authenticated user
     * @return empty response with 204 status
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteDocument(
            @PathVariable Long id,
            @AuthenticationPrincipal UserDetails userDetails) {

        logger.info("Delete document {} request from user: {}", id, userDetails.getUsername());

        User user = getCurrentUser(userDetails);
        documentService.deleteDocument(id, user);

        // 204 No Content - standard response for successful deletion
        return ResponseEntity.noContent().build();
    }

    /**
     * Get dashboard statistics for the authenticated user.
     *
     * Returns aggregated data:
     *   - Total document count
     *   - Total storage size
     *   - Documents by type (for pie charts)
     *   - Uploads over time (for line charts)
     *
     * @param userDetails the authenticated user
     * @return StatsDTO with all dashboard metrics
     */
    @GetMapping("/stats")
    public ResponseEntity<StatsDTO> getStats(
            @AuthenticationPrincipal UserDetails userDetails) {

        logger.debug("Stats request from user: {}", userDetails.getUsername());

        User user = getCurrentUser(userDetails);
        StatsDTO stats = documentService.getStats(user);

        return ResponseEntity.ok(stats);
    }

    /**
     * Helper method to get the full User entity from Spring Security's UserDetails.
     *
     * @AuthenticationPrincipal gives us a UserDetails object (username + password),
     * but we need our full User entity (with id, email, etc.) for database queries.
     * This method bridges that gap.
     *
     * @param userDetails the Spring Security UserDetails
     * @return the full User entity from the database
     * @throws RuntimeException if the user is not found (shouldn't happen if JWT is valid)
     */
    private User getCurrentUser(UserDetails userDetails) {
        return userRepository.findByUsername(userDetails.getUsername())
                .orElseThrow(() -> new RuntimeException("User not found: " + userDetails.getUsername()));
    }
}
