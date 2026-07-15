package com.kanemullett.model;

import static org.junit.Assert.assertEquals;

import com.kanemullett.model.type.SqlDataType;

public abstract class AbstractRecordTest {

    protected static void assertColumnDefinition(String expectedName, SqlDataType expectedDataType, boolean expectedPrimaryKey, ColumnDefinition actual) {
        assertEquals(expectedName, actual.getName());
        assertEquals(expectedDataType, actual.getDataType());
        assertEquals(expectedPrimaryKey, actual.getPrimaryKey());
    }
}
