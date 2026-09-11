package com.kohliiq;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.stream.Collectors;

import org.junit.jupiter.api.BeforeAll;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.datasource.SingleConnectionDataSource;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.context.TestPropertySource;

/**
 * Integration tests run against the project-local MySQL on a throwaway
 * {@code kohliiq_test} database (created once per run, real V1 schema).
 * Requires the documented local MySQL to be reachable.
 */
@SpringBootTest
@TestPropertySource(properties = "spring.jpa.hibernate.ddl-auto=validate")
public abstract class ContainerBase {
    static final String TEST_DB = "kohliiq_test";

    static String host() {
        return env("KOHLIIQ_DB_HOST", "127.0.0.1");
    }

    static String port() {
        return env("KOHLIIQ_DB_PORT", "3307");
    }

    static String user() {
        return env("KOHLIIQ_DB_USER", "root");
    }

    static String password() {
        return env("KOHLIIQ_DB_PASSWORD", "kohliiq-dev");
    }

    private static String env(String key, String def) {
        String v = System.getenv(key);
        return v == null || v.isBlank() ? def : v;
    }

    @DynamicPropertySource
    static void datasource(DynamicPropertyRegistry registry) {
        ensureTestDatabase();
        registry.add("spring.datasource.url",
                () -> "jdbc:mysql://" + host() + ":" + port() + "/" + TEST_DB);
        registry.add("spring.datasource.username", ContainerBase::user);
        registry.add("spring.datasource.password", ContainerBase::password);
    }

    private static void ensureTestDatabase() {
        var url = "jdbc:mysql://" + host() + ":" + port()
                + "/mysql?allowPublicKeyRetrieval=true&useSSL=false";
        var ds = new SingleConnectionDataSource(url, user(), password(), true);
        try {
            new JdbcTemplate(ds).execute("CREATE DATABASE IF NOT EXISTS " + TEST_DB
                    + " CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci");
        } finally {
            ds.destroy();
        }
    }

    @Autowired
    protected JdbcTemplate jdbc;

    @BeforeAll
    static void createSchema() throws Exception {
        var url = "jdbc:mysql://" + host() + ":" + port() + "/" + TEST_DB;
        var ds = new SingleConnectionDataSource(url, user(), password(), true);
        JdbcTemplate tpl;
        try {
            tpl = new JdbcTemplate(ds);
            Path migration = Paths.get("..", "db", "migrations",
                    "V1__initial_schema.sql");
        String sql = Files.readString(migration);
        String noComments = Arrays.stream(sql.split("\n"))
                .filter(l -> !l.strip().startsWith("--"))
                .collect(Collectors.joining("\n"));
        for (String stmt : noComments.split(";\\s*\n")) {
            if (!stmt.isBlank()) {
                tpl.execute(stmt);
            }
        }
        } finally {
            ds.destroy();
        }
    }
}
