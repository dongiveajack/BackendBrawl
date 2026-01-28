# Java Service (Spring Boot)

## Prerequisites
- Java 17+
- Maven
- Redis running on `localhost:6379`

## Run
```bash
# Run using Maven wrapper (not included here) or local maven
mvn spring-boot:run
```

The service listens on port 8081 (to avoid conflict with Go on 8080).
Endpoints:
- `GET /cache`: Get value from Redis
- `GET /actuator/prometheus`: Prometheus metrics
