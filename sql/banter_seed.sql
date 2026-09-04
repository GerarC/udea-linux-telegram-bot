-- Template para cargar frases de /insultar y /cumplido.
-- Las tablas ya se crean solas al arrancar el bot (banter/infrastructure/output/postgres/schema.py),
-- así que este script es solo para poblarlas con contenido.

INSERT INTO banter_insults (phrase) VALUES
    ('tienes la personalidad de un CAPTCHA mal resuelto'),
    ('programas como si el punto y coma te hubiera hecho algo'),
    ('eres el ''undefined is not a function'' de la vida real');
    -- agrega más filas aquí, una por línea, separadas por coma, la última con ;

INSERT INTO banter_compliments (phrase) VALUES
    ('tienes el código más limpio que he visto en producción'),
    ('eres el rubber duck que todos necesitan'),
    ('tu commit history es pura poesía');
    -- agrega más filas aquí, una por línea, separadas por coma, la última con ;
