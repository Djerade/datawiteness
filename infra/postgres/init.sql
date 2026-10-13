-- Extensions nécessaires à DataWitness
CREATE EXTENSION IF NOT EXISTS vector;     -- embeddings (pgvector)
CREATE EXTENSION IF NOT EXISTS pg_trgm;    -- recherche floue sur libellés
CREATE EXTENSION IF NOT EXISTS unaccent;   -- normalisation des libellés FR
