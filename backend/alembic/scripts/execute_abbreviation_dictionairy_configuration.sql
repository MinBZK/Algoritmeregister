-- Dutch abbreviation configuration
CREATE TEXT SEARCH DICTIONARY dutch_syn_thesaurus (
    TEMPLATE = thesaurus,
	DictFile = nl_synonyms,
	Dictionary = pg_catalog.dutch_stem
);

ALTER TEXT SEARCH CONFIGURATION NLD
	ALTER MAPPING FOR asciiword, asciihword, hword_asciipart, word, hword, hword_part
	WITH dutch_syn_thesaurus, dutch_stem, dutch_opentaal_hunspell;

-- English abbreviation configuration
CREATE TEXT SEARCH DICTIONARY english_syn_thesaurus (
    TEMPLATE = thesaurus,
	DictFile = en_synonyms,
	Dictionary = pg_catalog.english_stem
);

ALTER TEXT SEARCH CONFIGURATION ENG
	ALTER MAPPING FOR asciiword, asciihword, hword_asciipart, word, hword, hword_part
	WITH english_syn_thesaurus, english_stem, english_hunspell;

-- Drop the existing index
DROP INDEX IF EXISTS gin_idx;

-- Recreate the index
CREATE INDEX gin_idx ON algoritme_version USING gin (vector);

-- Perform tsvector generation on data with thesaurus knowledge of abbreviation
UPDATE algoritme_version SET vector = to_tsvector((CASE WHEN language='ENG' THEN 'ENG' ELSE 'NLD' END)::regconfig,
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


ANALYZE algoritme_version;
