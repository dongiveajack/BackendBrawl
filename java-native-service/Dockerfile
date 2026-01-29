# Build Stage
FROM ghcr.io/graalvm/native-image-community:21 AS builder
WORKDIR /app

# Copy configuration
COPY pom.xml .
COPY src ./src

# Build Native Image
# -Pnative unlocks the native profile in Spring Boot parent
RUN ./mvnw -Pnative native:compile

# Runtime Stage
# Use a lightweight base image for the binary
FROM ubuntu:jammy
WORKDIR /app

# Copy the binary from the builder stage (target name matches artifactId in pom.xml)
COPY --from=builder /app/target/bench-native .

EXPOSE 8083

# Run the native binary directly
CMD ["./bench-native"]
