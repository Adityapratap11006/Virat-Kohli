package com.kohliiq.dto;

import com.kohliiq.entity.Player;

public record PlayerDto(Long id, String name, String registryId, boolean ambiguous) {
    public static PlayerDto from(Player p) {
        String registryId = Boolean.TRUE.equals(p.getHasRegistryId())
                && p.getPlayerCode() != null
                && p.getPlayerCode().startsWith("REG:")
                ? p.getPlayerCode().substring(4)
                : null;
        return new PlayerDto(p.getId(), p.getDisplayName(), registryId,
                Boolean.TRUE.equals(p.getAmbiguous()));
    }
}
