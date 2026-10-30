package com.kanemullett.service;

import org.springframework.stereotype.Service;

@Service
public class RoundService {

    private final DatabaseQueryService queryService;

    public RoundService(DatabaseQueryService queryService) {
        this.queryService = queryService;
    }
}
