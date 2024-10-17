ALTER TABLE IF EXISTS organisation_details
ADD COLUMN IF NOT EXISTS vector tsvector;

UPDATE organisation_details SET vector = to_tsvector((CASE WHEN language='ENG' THEN 'ENG' ELSE 'NLD' END)::regconfig,
    COALESCE(name,''));

CREATE OR REPLACE FUNCTION update_vector_org() RETURNS TRIGGER AS $$
BEGIN
  NEW.vector :=
    to_tsvector((CASE WHEN NEW.language='ENG' THEN 'ENG' ELSE 'NLD' END)::regconfig, COALESCE(NEW.name,''));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER vector_trigger_org BEFORE INSERT OR UPDATE 
ON organisation_details FOR EACH ROW EXECUTE FUNCTION
 update_vector_org();