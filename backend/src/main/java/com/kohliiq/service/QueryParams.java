package com.kohliiq.service;

import java.util.Set;

import com.kohliiq.exception.BadRequestException;

public final class QueryParams {
    public static final Set<String> FORMATS = Set.of("ODI", "T20I", "IPL");

    private QueryParams() {
    }

    /** Null when absent (all formats); 400 on unknown values. */
    public static String formatOrNull(String format) {
        if (format == null || format.isBlank()) {
            return null;
        }
        String upper = format.toUpperCase();
        if (!FORMATS.contains(upper)) {
            throw new BadRequestException(
                    "Invalid format '" + format + "'. Supported: ODI, T20I, IPL.");
        }
        return upper;
    }

    public static int limitOrDefault(Integer limit, int def, int max) {
        if (limit == null) {
            return def;
        }
        if (limit < 1 || limit > max) {
            throw new BadRequestException(
                    "limit must be between 1 and " + max + ".");
        }
        return limit;
    }
}
