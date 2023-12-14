CREATE TABLE words AS SELECT word FROM ts_stat('SELECT vector FROM algoritme_version');

CREATE OR REPLACE FUNCTION update_words()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO words (word)
    SELECT word
    FROM ts_stat('SELECT vector FROM algoritme_version')
    WHERE word NOT IN (SELECT word FROM words);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_words_trigger
AFTER INSERT ON algoritme_version
FOR EACH ROW
EXECUTE FUNCTION update_words();