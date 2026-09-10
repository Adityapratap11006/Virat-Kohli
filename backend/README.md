# KohliIQ Backend (Spring Boot)

Frontend-facing API. Owns business logic, MySQL access, request validation,
and ML prediction-context construction (Phase 4+).

- Java 21, Spring Boot 3.5.x, Maven.
- Run: `mvn spring-boot:run` (from `backend/`).
- DB config arrives in Phase 3 via `MYSQL_URL` / `MYSQL_USER` / `MYSQL_PASSWORD`.
- JPA entities, repositories, controllers arrive in Phase 4. No domain code yet.
