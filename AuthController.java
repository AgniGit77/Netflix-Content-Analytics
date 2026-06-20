package com.docintel.controller;

import com.docintel.dto.AuthRequest;
import com.docintel.dto.AuthResponse;
import com.docintel.model.User;
import com.docintel.repository.UserRepository;
import com.docintel.security.JwtUtil;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

/**
 * AuthController - Handles user authentication (login and registration).
 *
 * This controller provides two public endpoints:
 *   POST /api/auth/register  → Create a new user account
 *   POST /api/auth/login     → Authenticate and get a JWT token
 *
 * These endpoints are PUBLIC (no JWT required) because:
 *   - You can't send a token if you don't have one yet!
 *   - Registration creates the account
 *   - Login gives you the token for future requests
 *
 * @RestController = @Controller + @ResponseBody
 *   This means all return values are automatically serialized to JSON.
 *
 * @RequestMapping("/api/auth") sets the base URL for all endpoints in this controller.
 */
@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private static final Logger logger = LoggerFactory.getLogger(AuthController.class);

    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private JwtUtil jwtUtil;

    /**
     * Register a new user account.
     *
     * FLOW:
     *   1. Validate the request body (@Valid triggers bean validation)
     *   2. Check for duplicate username and email
     *   3. Hash the password with BCrypt
     *   4. Save the user to the database
     *   5. Generate a JWT token for immediate login
     *   6. Return the token and success message
     *
     * Example request:
     *   POST /api/auth/register
     *   Content-Type: application/json
     *   {
     *     "username": "john",
     *     "password": "secret123",
     *     "email": "john@example.com"
     *   }
     *
     * Example response (200 OK):
     *   {
     *     "token": "eyJhbGci...",
     *     "username": "john",
     *     "message": "Registration successful"
     *   }
     *
     * @param request the registration data (validated with @Valid)
     * @return AuthResponse with JWT token on success
     */
    @PostMapping("/register")
    public ResponseEntity<AuthResponse> register(@Valid @RequestBody AuthRequest request) {
        logger.info("Registration attempt for username: {}", request.getUsername());

        // Check if username is already taken
        if (userRepository.existsByUsername(request.getUsername())) {
            throw new IllegalArgumentException("Username is already taken: " + request.getUsername());
        }

        // Check if email is already registered
        if (request.getEmail() != null && userRepository.existsByEmail(request.getEmail())) {
            throw new IllegalArgumentException("Email is already registered: " + request.getEmail());
        }

        // Create the new user with BCrypt-hashed password
        // NEVER store passwords in plain text!
        User user = User.builder()
                .username(request.getUsername())
                .email(request.getEmail() != null ? request.getEmail() : request.getUsername() + "@docintel.com")
                .password(passwordEncoder.encode(request.getPassword()))
                .build();

        // Save the user to the database
        userRepository.save(user);
        logger.info("User registered successfully: {}", user.getUsername());

        // Generate a JWT token so the user is immediately logged in
        String token = jwtUtil.generateToken(user.getUsername());

        // Build and return the response
        AuthResponse response = AuthResponse.builder()
                .token(token)
                .username(user.getUsername())
                .message("Registration successful")
                .build();

        return ResponseEntity.ok(response);
    }

    /**
     * Authenticate a user and return a JWT token.
     *
     * FLOW:
     *   1. Validate the request body
     *   2. Attempt authentication via Spring Security's AuthenticationManager
     *      - This calls CustomUserDetailsService.loadUserByUsername()
     *      - Then compares BCrypt hashes of the submitted and stored passwords
     *   3. If authentication succeeds, generate a JWT token
     *   4. Return the token
     *
     * If authentication fails (wrong username or password), Spring Security
     * throws BadCredentialsException, which our GlobalExceptionHandler
     * catches and returns as a 401 Unauthorized response.
     *
     * Example request:
     *   POST /api/auth/login
     *   Content-Type: application/json
     *   {
     *     "username": "john",
     *     "password": "secret123"
     *   }
     *
     * Example response (200 OK):
     *   {
     *     "token": "eyJhbGci...",
     *     "username": "john",
     *     "message": "Login successful"
     *   }
     *
     * @param request the login credentials
     * @return AuthResponse with JWT token on success
     * @throws BadCredentialsException if username or password is wrong
     */
    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@Valid @RequestBody AuthRequest request) {
        logger.info("Login attempt for username: {}", request.getUsername());

        // Authenticate using Spring Security
        // This internally:
        //   1. Calls CustomUserDetailsService.loadUserByUsername()
        //   2. Compares the BCrypt hash of the submitted password with the stored hash
        //   3. Throws BadCredentialsException if they don't match
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        request.getUsername(),
                        request.getPassword()
                )
        );

        // If we reach here, authentication was successful
        // Generate a JWT token for the authenticated user
        String token = jwtUtil.generateToken(request.getUsername());

        logger.info("User logged in successfully: {}", request.getUsername());

        AuthResponse response = AuthResponse.builder()
                .token(token)
                .username(request.getUsername())
                .message("Login successful")
                .build();

        return ResponseEntity.ok(response);
    }
}
