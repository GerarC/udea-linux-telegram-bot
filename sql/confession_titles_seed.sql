-- Template para cargar títulos de /confesar y /confesiones.
-- La tabla ya se crea (y se siembra con los 3 títulos base) sola al arrancar el bot
-- (confessions/infrastructure/output/postgres/schema/confession_titles.py),
-- así que este script es solo para agregar títulos nuevos.
-- ON CONFLICT (title) evita duplicados si corres el script más de una vez.

INSERT INTO confession_titles (emoji, title, footer) VALUES
    ('👻', 'Confesión fantasma', 'Un ejemplo - reemplaza esta fila por la tuya')
ON CONFLICT (title) DO NOTHING;
-- agrega más filas aquí, una por línea, separadas por coma, la última con ;
