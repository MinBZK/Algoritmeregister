-- Custom collation, does not work, should be activated in database cluster bootstrap
-- initdb --lc-collate=C
SET client_encoding = 'UTF8';

CREATE TABLE IF NOT EXISTS algemene_informatie (
    id  SERIAL PRIMARY KEY,
    name varchar (1024) NOT NULL,
    organization varchar (1024) NOT NULL,
    department varchar (1024) NOT NULL,
    description_short varchar (5000) NOT NULL,
    type varchar (1024) NOT NULL,
    category varchar (1024) NOT NULL,
    website varchar (1024) ,
    status varchar (1024) NOT NULL
);


CREATE TABLE IF NOT EXISTS inzet (
    id  SERIAL PRIMARY KEY,
    goal varchar (5000) NOT NULL,
    impact varchar (5000) NOT NULL,
    proportionality varchar (5000) NOT NULL,
    decision_making_process varchar (5000) NOT NULL,
    documentation varchar (1024) ,
    algoritme_id integer,
    CONSTRAINT fk_algoritme_inzet
      FOREIGN KEY (algoritme_id) 
	  REFERENCES algemene_informatie (id)
	  ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS toepassing (
    id  SERIAL PRIMARY KEY,
    description varchar (10000),
    application_url varchar (1024),
    publiccode varchar (1024),
    mprd boolean,
    source_data varchar (5000),
    methods_and_models varchar (5000),
    algoritme_id integer,
    CONSTRAINT fk_algoritme_toepassing
      FOREIGN KEY (algoritme_id) 
	  REFERENCES algemene_informatie (id)
	  ON DELETE CASCADE    
);


CREATE TABLE IF NOT EXISTS toezicht (
    id  SERIAL PRIMARY KEY,
    monitoring varchar (5000),
    human_intervention varchar(5000) NOT NULL, 
    risks varchar(5000),
    performance_standard varchar(5000),
    algoritme_id integer,
    CONSTRAINT fk_algoritme_toezicht
      FOREIGN KEY (algoritme_id) 
	  REFERENCES algemene_informatie (id)
	  ON DELETE CASCADE    
);


CREATE TABLE IF NOT EXISTS juridisch (
    id  SERIAL PRIMARY KEY,
    competent_authority varchar (1024),
    lawful_basis varchar (5000) NOT NULL,
    dpia boolean, 
    dpia_description varchar (5000),
    objection_procedure varchar (5000) NOT NULL,
    algoritme_id integer,
    CONSTRAINT fk_algoritme_juridisch
      FOREIGN KEY (algoritme_id) 
	  REFERENCES algemene_informatie (id)
	  ON DELETE CASCADE 
);


CREATE TABLE IF NOT EXISTS metadata (
    id  SERIAL PRIMARY KEY,
    schema varchar (1024),
    uuid varchar (1024),
    url varchar (1024),
    contact_email varchar (1024) NOT NULL,
    area varchar (1024),
    lang varchar (1024),
    revision_date varchar (1024),
    algoritme_id integer,
    CONSTRAINT fk_algoritme_metadata
      FOREIGN KEY (algoritme_id) 
	  REFERENCES algemene_informatie (id)
	  ON DELETE CASCADE 
);


