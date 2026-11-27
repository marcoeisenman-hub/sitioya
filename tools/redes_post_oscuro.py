# Post oscuro para el medio del grid de @sitioya.pty (1080x1350).
# Uso: python3 tools/redes_post_oscuro.py -> redes/posts/oscuro-tu-pagina-a-la-medida.png
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from redes_heladeria import CORAL, CORAL_D, CREMA, NAVY, RAIZ, fuente, pantalla_portada, pastilla, texto_ancho  # noqa: E402
from redes_posts import captura, celular_chico, pie_simple  # noqa: E402


def post_oscuro():
    im = Image.new('RGBA', (1080, 1350), NAVY)
    d = ImageDraw.Draw(im)
    d.ellipse((560, -260, 1400, 580), fill='#243a63')
    d.ellipse((-300, 900, 420, 1620), fill='#22365c')
    pastilla(d, (70, 74), 'HECHA A LA MEDIDA', fuente(28, 900), CORAL, NAVY, pad=(28, 15))
    f = fuente(92, 900)
    for i, (linea, c) in enumerate((('Tu negocio,', CREMA), ('en una página', CREMA), ('que vende', CORAL))):
        assert 66 + texto_ancho(d, linea, f) < 1010, linea
        d.text((66, 150 + i * 100), linea, font=f, fill=c)
    ancho = 232
    for x, y, pant, giro in ((572, 500, pantalla_portada(600, 1170), -5), (776, 540, captura('menu'), 5)):
        celular_chico(im, (x, y), pant, ancho, girar=giro)
    d = ImageDraw.Draw(im)
    y = 520
    for nombre, precio, detalle in (('Básica', '$99', 'Lo esencial y tu WhatsApp'),
                                    ('Completa', '$199', 'Menú, pagos, reservas y dominio')):
        d.rounded_rectangle((70, y, 520, y + 170), 30, fill='#2a4170')
        d.text((104, y + 26), nombre, font=fuente(40, 900), fill=CREMA)
        d.text((104, y + 84), detalle, font=fuente(24, 600), fill='#c8d2e6')
        fp = fuente(50, 900)
        d.text((490 - texto_ancho(d, precio, fp), y + 22), precio, font=fp, fill=CORAL)
        y += 196
    d.text((70, y + 20), 'Te hacemos un ejemplo', font=fuente(34, 800), fill=CREMA)
    d.text((70, y + 70), 'gratis antes de decidir.', font=fuente(34, 800), fill=CREMA)
    pastilla(d, (70, 1086), 'Escríbenos al 6919-7559', fuente(32, 900), CORAL, NAVY, pad=(30, 18))
    d.text((72, 1180), 'Negocios y datos de ejemplo', font=fuente(22, 500), fill='#9fb0cf')
    pie_simple(im, oscuro=True)
    return im


if __name__ == '__main__':
    out = os.path.join(RAIZ, 'redes', 'posts', 'oscuro-tu-pagina-a-la-medida.png')
    post_oscuro().convert('RGB').save(out, optimize=True)
    print(out)
