package com.kohliiq.dto;

import java.util.List;

public record FormatSummaryDto(PlayerDto player, List<PerFormatDto> formats) {
    public record PerFormatDto(
            String format,
            long innings,
            long runs,
            Integer highestScore,
            Double average) {
    }
}
