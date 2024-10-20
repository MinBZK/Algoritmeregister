CREATE TEXT SEARCH CONFIGURATION FRY (copy = pg_catalog.dutch);

-- Frisian abbreviation configuration
CREATE TEXT SEARCH DICTIONARY frisian_syn_thesaurus (
    TEMPLATE = thesaurus,
	DictFile = fy_synonyms,
	Dictionary = pg_catalog.dutch_stem
);

ALTER TEXT SEARCH CONFIGURATION FRY
	ALTER MAPPING FOR asciiword, asciihword, hword_asciipart, word, hword, hword_part
	WITH frisian_syn_thesaurus, dutch_stem, dutch_opentaal_hunspell;

DROP INDEX IF EXISTS gin_idx;

CREATE INDEX gin_idx ON algoritme_version USING gin (vector);

ALTER TABLE IF EXISTS organisation_details
ADD COLUMN IF NOT EXISTS vector tsvector;

-- Adding Frisian organisation names to vector
UPDATE organisation_details SET vector = to_tsvector((CASE WHEN language='ENG' THEN 'ENG' WHEN language='FRY' THEN 'FRY' ELSE 'NLD' END)::regconfig,
    COALESCE(name,''));

CREATE OR REPLACE FUNCTION update_vector_org() RETURNS TRIGGER AS $$
BEGIN
  NEW.vector :=
    to_tsvector((CASE WHEN NEW.language='ENG' THEN 'ENG' WHEN NEW.language='FRY' THEN 'FRY' ELSE 'NLD' END)::regconfig, COALESCE(NEW.name,''));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER vector_trigger_org BEFORE INSERT OR UPDATE 
ON organisation_details FOR EACH ROW EXECUTE FUNCTION
 update_vector_org();

--re-calculate vector column
UPDATE algoritme_version SET vector = to_tsvector((CASE WHEN language='ENG' THEN 'ENG' WHEN language='FRY' THEN 'FRY' ELSE 'NLD' END)::regconfig,
    COALESCE(name,'') || ' ' || COALESCE(organization,'') || ' ' || COALESCE(department,'') || ' ' || 
    COALESCE(description_short,'') || ' ' || COALESCE(type,'') || ' ' ||  COALESCE(category,'') || ' ' ||
    COALESCE(website,'') || ' ' || COALESCE(status,'') || ' ' || COALESCE(goal,'') || ' ' || COALESCE(impact,'') || ' ' || 
    COALESCE(proportionality,'') || ' ' || COALESCE(decision_making_process,'') || ' ' || COALESCE(documentation,'') || ' ' ||
    COALESCE(competent_authority,'') || ' ' || COALESCE(lawful_basis,'') || ' ' || COALESCE(iama,'') || ' ' ||
    COALESCE(iama_description,'') || ' ' || COALESCE(dpia_description,'') || ' ' || COALESCE(objection_procedure,'') || ' ' ||
    COALESCE(standard_version,'') || ' ' || COALESCE(url,'') || ' ' || COALESCE(contact_email,'') || ' ' ||
    COALESCE(area,'') || ' ' || COALESCE(lang,'') || ' ' || COALESCE(revision_date,'') || ' ' || 
    COALESCE(description,'') || ' ' || COALESCE(application_url,'') || ' ' || COALESCE(publiccode,'') || ' ' ||
    COALESCE(source_data,'') || ' ' || COALESCE(methods_and_models,'') || ' ' || COALESCE(monitoring,'') || ' ' ||
    COALESCE(human_intervention,'') || ' ' || COALESCE(risks,'') || ' ' || COALESCE(performance_standard,'') || ' ' ||
    COALESCE(provider,'') || ' ' || COALESCE(process_index_url,'') || ' ' || COALESCE(tags,'') || ' ' ||
    COALESCE(begin_date,'') || ' ' || COALESCE(end_date,'') || ' ' || COALESCE(lawful_basis_link,'') || ' ' ||
    COALESCE(impacttoetsen,'') || ' ' || COALESCE(source_data_link,'')  || ' ' || COALESCE(publication_category,'') || ' ' ||
    COALESCE(lawful_basis_grouping,'[]') || ' ' || COALESCE(impacttoetsen_grouping,'[]') || ' ' || COALESCE(source_data_grouping,'[]'));

-- replace trigger to contain Frisian language
CREATE OR REPLACE FUNCTION update_vector() RETURNS TRIGGER AS $$
BEGIN
  NEW.vector :=
    to_tsvector((CASE WHEN NEW.language='ENG' THEN 'ENG' WHEN NEW.language='FRY' THEN 'FRY' ELSE 'NLD' END)::regconfig, COALESCE(NEW.name,'') || ' ' || COALESCE(NEW.organization,'') || ' ' || COALESCE(NEW.department,'') || ' ' || 
    COALESCE(NEW.description_short,'') || ' ' || COALESCE(NEW.type,'') || ' ' ||  COALESCE(NEW.category,'') || ' ' ||
    COALESCE(NEW.website,'') || ' ' || COALESCE(NEW.status,'') || ' ' || COALESCE(NEW.goal,'') || ' ' || COALESCE(NEW.impact,'') || ' ' || 
    COALESCE(NEW.proportionality,'') || ' ' || COALESCE(NEW.decision_making_process,'') || ' ' || COALESCE(NEW.documentation,'') || ' ' ||
    COALESCE(NEW.competent_authority,'') || ' ' || COALESCE(NEW.lawful_basis,'') || ' ' || COALESCE(NEW.iama,'') || ' ' ||
    COALESCE(NEW.iama_description,'') || ' ' || COALESCE(NEW.dpia_description,'') || ' ' || COALESCE(NEW.objection_procedure,'') || ' ' ||
    COALESCE(NEW.standard_version,'') || ' ' || COALESCE(NEW.url,'') || ' ' || COALESCE(NEW.contact_email,'') || ' ' ||
    COALESCE(NEW.area,'') || ' ' || COALESCE(NEW.lang,'') || ' ' || COALESCE(NEW.revision_date,'') || ' ' || 
    COALESCE(NEW.description,'') || ' ' || COALESCE(NEW.application_url,'') || ' ' || COALESCE(NEW.publiccode,'') || ' ' ||
    COALESCE(NEW.source_data,'') || ' ' || COALESCE(NEW.methods_and_models,'') || ' ' || COALESCE(NEW.monitoring,'') || ' ' ||
    COALESCE(NEW.human_intervention,'') || ' ' || COALESCE(NEW.risks,'') || ' ' || COALESCE(NEW.performance_standard,'') || ' ' ||
    COALESCE(NEW.provider,'') || ' ' || COALESCE(NEW.process_index_url,'') || ' ' || COALESCE(NEW.tags,'') || ' ' ||
    COALESCE(NEW.begin_date,'') || ' ' || COALESCE(NEW.end_date,'') || ' ' || COALESCE(NEW.lawful_basis_link,'') || ' ' ||
    COALESCE(NEW.impacttoetsen,'') || ' ' || COALESCE(NEW.source_data_link,'') || ' ' || COALESCE(NEW.publication_category,'') || ' ' || 
    COALESCE(NEW.lawful_basis_grouping,'[]') || ' ' || COALESCE(NEW.impacttoetsen_grouping,'[]') || ' ' || COALESCE(NEW.source_data_grouping,'[]'));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER vector_trigger BEFORE INSERT OR UPDATE 
ON algoritme_version FOR EACH ROW EXECUTE FUNCTION
 update_vector();

ANALYZE algoritme_version;