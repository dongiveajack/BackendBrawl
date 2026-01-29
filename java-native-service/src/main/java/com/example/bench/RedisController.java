package com.example.bench;

import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Collections;
import java.util.Map;

@RestController
public class RedisController {

    private final StringRedisTemplate redisTemplate;

    // Constructor Injection
    public RedisController(StringRedisTemplate redisTemplate) {
        this.redisTemplate = redisTemplate;
    }

    @GetMapping("/cache")
    public Map<String, String> getCache() {
        // Single responsibility: HTTP -> Redis GET -> Response
        String value = redisTemplate.opsForValue().get("test_key");
        
        // Minimal JSON overhead: Returning Map<String, String> is handled by Jackson efficiently
        // If value is null, Jackson will serialize it as null or missing depending on config,
        // but for Map value it will be null.
        // { "value": <value> }
        return Collections.singletonMap("value", value);
    }
}
