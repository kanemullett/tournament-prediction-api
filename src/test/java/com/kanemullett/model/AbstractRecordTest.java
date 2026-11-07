package com.kanemullett.model;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.kanemullett.model.type.SqlDataType;

public abstract class AbstractRecordTest {

    /**
     * Asserts a NOT NULL column.
     */
    protected static void assertColumnDefinition(String expectedName, SqlDataType expectedDataType, boolean expectedPrimaryKey, ColumnDefinition actual) {
        assertColumnDefinition(expectedName, expectedDataType, expectedPrimaryKey, false, actual);
    }

    protected static void assertColumnDefinition(String expectedName, SqlDataType expectedDataType, boolean expectedPrimaryKey, boolean expectedNullable, ColumnDefinition actual) {
        assertEquals(expectedName, actual.getName());
        assertEquals(expectedDataType, actual.getDataType());
        assertEquals(expectedPrimaryKey, actual.getPrimaryKey());
        assertEquals(expectedNullable, actual.isNullable(), () -> "nullability of column " + expectedName);
    }
}
