package com.docintel;

import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * DocIntelApplication - Entry point for the Document Intelligence & QA Automation Platform.
 *
 * @SpringBootApplication is a convenience annotation that combines:
 *   - @Configuration: Marks this class as a source of bean definitions
 *   - @EnableAutoConfiguration: Tells Spring Boot to auto-configure based on dependencies
 *   - @ComponentScan: Scans the current package and sub-packages for Spring components
 *
 * When you run this class, Spring Boot:
 *   1. Starts an embedded Tomcat server on port 8080
 *   2. Connects to the MySQL database
 *   3. Creates/updates database tables based on our @Entity classes
 *   4. Registers all our controllers, services, and repositories
 */
@SpringBootApplication
public class DocIntelApplication {

    // Logger instance for this class - used to print informational messages
    private static final Logger logger = LoggerFactory.getLogger(DocIntelApplication.class);

    // Inject the upload directory path from application.yml
    // The @Value annotation reads the 'file.upload-dir' property
    @Value("${file.upload-dir:./uploads}")
    private String uploadDir;

    /**
     * The main method - Java's standard entry point.
     * SpringApplication.run() bootstraps the entire Spring Boot application.
     *
     * @param args command-line arguments (passed through to Spring Boot)
     */
    public static void main(String[] args) {
        SpringApplication.run(DocIntelApplication.class, args);
    }

    /**
     * This method runs automatically after the application starts up.
     *
     * @PostConstruct methods are called once the bean is fully initialized.
     * We use it here to ensure the file upload directory exists on disk.
     * If it doesn't exist, we create it.
     */
    @PostConstruct
    public void init() {
        try {
            Path uploadPath = Paths.get(uploadDir);
            if (!Files.exists(uploadPath)) {
                Files.createDirectories(uploadPath);
                logger.info("Created upload directory: {}", uploadPath.toAbsolutePath());
            } else {
                logger.info("Upload directory already exists: {}", uploadPath.toAbsolutePath());
            }
        } catch (IOException e) {
            logger.error("Could not create upload directory: {}", e.getMessage());
            throw new RuntimeException("Could not create upload directory!", e);
        }
    }
}
