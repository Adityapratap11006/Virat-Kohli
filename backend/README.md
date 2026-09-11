# KohliIQ Backend (Spring Boot)

Frontend-facing API. Owns business logic, MySQL access, request validation,
and aggregation (ML prediction-context construction arrives later).

- Java 21, Spring Boot 3.5, Spring Data JPA, Maven.
- Run: `mvn spring-boot:run` (from `backend/`). DB via `MYSQL_URL` /
  `MYSQL_USER` / `MYSQL_PASSWORD` (defaults target the project MySQL on
  `127.0.0.1:3307`).
- Test: `mvn test`. Unit + MockMvc tests plus integration tests on a
  throwaway `kohliiq_test` database (needs local MySQL reachable).
- API reference: `docs/backend-api.md`. Frontend field contract:
  `docs/frontend-contract.md`.
- Phase 4 slice: players, career/format summaries, recent form, top
  knocks, minimal match detail. No ML, no auth.
