package com.kohliiq.repository;

import java.util.Optional;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import com.kohliiq.entity.Player;

public interface PlayerRepository extends JpaRepository<Player, Long> {
    Optional<Player> findByPlayerCode(String playerCode);

    @Query("SELECT p FROM Player p WHERE LOWER(p.displayName) LIKE LOWER(CONCAT('%', :q, '%'))")
    Page<Player> searchByName(@Param("q") String query, Pageable pageable);
}
