package com.kanemullett.service;

import org.springframework.stereotype.Service;

@Service
public class GroupService {

    private final DatabaseQueryService queryService;

    public GroupService(DatabaseQueryService queryService) {
        this.queryService = queryService;
    }
}
