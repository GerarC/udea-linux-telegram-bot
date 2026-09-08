-- Template para cargar frases de /horoscopo.
-- La tabla ya se crea sola al arrancar el bot (horoscope/infrastructure/output/postgres/schema/),
-- así que este script es solo para poblarla con contenido.

INSERT INTO horoscope_phrases (phrase) VALUES
    ('hoy Mercurio retrógrado hace que tu SSH se cuelgue justo cuando más lo necesitas'),
    ('las estrellas se alinean para que por fin encuentres ese punto y coma faltante'),
    ('tu carta astral indica un merge conflict inevitable antes del mediodía'),
    ('Saturno en tu casa 10 sugiere revisar los logs antes de culpar a Mercury'),
    ('el universo conspira para que tu build pase a la primera, no te acostumbres'),
    ('hoy es un buen día para hacer ese `sudo rm -rf` que llevas posponiendo... con cuidado'),
    ('las energías cósmicas favorecen encontrar wifi gratis, no encontrar la contraseña del router'),
    ('tu aura hoy tiene el color exacto de un kernel panic: intensa e inesperada'),
    ('Venus en tránsito anuncia que hoy alguien por fin va a leer tu documentación'),
    ('el destino te tiene preparado un ticket de soporte que en realidad era el modem apagado'),
    ('hoy tus decisiones binarias (0 o 1) definirán si el deploy es un éxito o un incidente'),
    ('la alineación planetaria de hoy es ideal para actualizar el sistema... y romper todo'),
    ('el oráculo indica que tu próximo commit se llamará "fix" y arreglará poco'),
    ('las cartas revelan que hoy vas a entender un stack trace a la primera, disfrútalo'),
    ('tu horóscopo dice que hoy el café rinde como root: sin límites');
    -- agrega más filas aquí, una por línea, separadas por coma, la última con ;
