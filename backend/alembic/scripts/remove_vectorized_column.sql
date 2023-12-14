ALTER TABLE algoritme_version DROP COLUMN vector;

DROP INDEX IF EXISTS gin_idx;

DROP TRIGGER vector_trigger ON algoritme_version;