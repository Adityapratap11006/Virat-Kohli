# KohliIQ Backend (Spring Boot)

Frontend-facing API. Owns business logic, MySQL access, request validation,
and aggregation (ML prediction-context construction arrives later).

- Java 21, Spring Boot 3.5, Spring Data JPA, Maven (via wrapper — no global
  install needed).
- Phase 4 slice: players, career/format summaries, recent form, top
  knocks, minimal match detail. No ML, no auth.

## Run locally (Windows, from `backend/`)

```bat
.\mvnw.cmd spring-boot:run
```

Requires JDK 21 (`JAVA_HOME` pointing at it) and the project MySQL
reachable (defaults: `127.0.0.1:3307`, see `MYSQL_URL` / `MYSQL_USER` /
`MYSQL_PASSWORD`). Then: `http://localhost:8080/api/players?search=kohli`.

## Test (Windows, from `backend/`)

```bat
.\mvnw.cmd test
```

Unit + MockMvc tests plus integration tests on a throwaway `kohliiq_test`
database (needs local MySQL reachable).

## Docs

- API reference: `docs/backend-api.md`. Frontend field contract:
  `docs/frontend-contract.md`.
