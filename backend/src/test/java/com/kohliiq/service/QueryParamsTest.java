package com.kohliiq.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

import com.kohliiq.exception.BadRequestException;

class QueryParamsTest {
    @Test
    void formatAcceptsKnownValuesCaseInsensitively() {
        assertEquals("ODI", QueryParams.formatOrNull("odi"));
        assertEquals("T20I", QueryParams.formatOrNull("T20I"));
        assertEquals("IPL", QueryParams.formatOrNull("IPL"));
        assertNull(QueryParams.formatOrNull(null));
        assertNull(QueryParams.formatOrNull("  "));
    }

    @Test
    void formatRejectsUnknown() {
        assertThrows(BadRequestException.class, () -> QueryParams.formatOrNull("TEST"));
        assertThrows(BadRequestException.class, () -> QueryParams.formatOrNull("T20"));
    }

    @Test
    void limits() {
        assertEquals(10, QueryParams.limitOrDefault(null, 10, 100));
        assertEquals(5, QueryParams.limitOrDefault(5, 10, 100));
        assertThrows(BadRequestException.class, () -> QueryParams.limitOrDefault(0, 10, 100));
        assertThrows(BadRequestException.class, () -> QueryParams.limitOrDefault(101, 10, 100));
    }
}
