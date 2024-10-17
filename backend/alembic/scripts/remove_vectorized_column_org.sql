ALTER TABLE organisation_details DROP COLUMN vector;

DROP INDEX IF EXISTS gin_idx;

DROP TRIGGER vector_trigger ON organisation_details;