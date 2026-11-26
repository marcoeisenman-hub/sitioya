# Genera los posts del feed de @sitioya.pty (1080x1350) con el mismo estilo
# del carrusel de la Heladería: precios, 4 páginas de ejemplo, cómo funciona,
# "Tu negocio en internet, ya" y "Síguenos para más".
# Uso: python3 tools/redes_posts.py  -> redes/posts/*.png
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from redes_heladeria import (  # noqa: E402
    BLANCO, BLUSH, CORAL, CORAL_D, CREMA, MENTA, NAVY, SOFT, RAIZ,
    base, envolver, fuente, kicker, logo_sitioya, pantalla_portada, parrafo, pastilla,
    puntos_fondo, sombra, texto_ancho,
)

SALIDA = os.path.join(RAIZ, 'redes', 'posts')
SHOTS = os.path.join(RAIZ, 'img', 'shots')
os.makedirs(SALIDA, exist_ok=True)
MENTA_CLARO = '#DDF4EC'


def captura(nombre):
    """Captura de celular de una página de ejemplo, sin el botón flotante de abajo."""
    im = Image.open(os.path.join(SHOTS, nombre + '_mob.jpg')).convert('RGBA')
    return im.crop((0, 0, im.width, 760))


def celular_chico(lienzo, xy, pantalla, ancho, girar=0):
    """Marco de celular proporcional al tamaño (sirve para celulares chicos)."""
    marco = max(10, int(ancho * 0.05))
    sw = ancho - marco * 2
    sh = int(sw * pantalla.height / pantalla.width)
    W, H = ancho, sh + marco * 2
    radio = int(ancho * 0.15)
    tel = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(tel)
    g.rounded_rectangle((0, 0, W - 1, H - 1), radio, fill=NAVY)
    pant = pantalla.resize((sw, sh), Image.LANCZOS)
    m = Image.new('L', (sw, sh), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, sw - 1, sh - 1), radio - marco, fill=255)
    tel.paste(pant, (marco, marco), m)
    nw, nh = ancho * 0.24, ancho * 0.06
    g.rounded_rectangle((W / 2 - nw / 2, marco + nh * 0.4, W / 2 + nw / 2, marco + nh * 1.4), nh / 2, fill=NAVY)
    if girar:
        tel = tel.rotate(girar, resample=Image.BICUBIC, expand=True)
    x, y = xy
    sombra(lienzo, (x + 12, y + 20, x + tel.width - 12, y + tel.height - 6), radio, desp=(0, 22), difuso=28, alfa=70)
    lienzo.alpha_composite(tel, (int(x), int(y)))
    return tel.size


def pie_simple(im, oscuro=False):
    d = ImageDraw.Draw(im)
    W, H = im.size
    logo_sitioya(im, (70, H - 120), 58, oscuro)
    d = ImageDraw.Draw(im)
    f = fuente(28, 700)
    t = '@sitioya.pty'
    d.text((W - 70 - texto_ancho(d, t, f), H - 106), t, font=f, fill=CREMA if oscuro else SOFT)


def boton_pagina(d, cy, fondo=CORAL, color=NAVY, tam=42):
    """Botón 'Comenta PÁGINA y te contamos' centrado, con PÁGINA subrayada."""
    f = fuente(tam, 900)
    t1, t2, t3 = 'Comenta ', 'PÁGINA', ' y te contamos'
    ancho_total = texto_ancho(d, t1 + t2 + t3, f) + 80
    x = (1080 - ancho_total) / 2
    alto = tam + 54
    d.rounded_rectangle((x, cy, x + ancho_total, cy + alto), alto / 2, fill=fondo)
    tx = x + 40
    for parte in (t1, t2, t3):
        d.text((tx, cy + 22), parte, font=f, fill=color)
        if parte == t2:
            d.rounded_rectangle((tx, cy + tam + 34, tx + texto_ancho(d, parte, f), cy + tam + 40), 3, fill=color)
        tx += texto_ancho(d, parte, f)
    return cy + alto


# ---------- 1. Precios ----------

PLANES = [
    ('Básica', '', '$99', 'Lo esencial: tus fotos, textos y precios, botón de WhatsApp, mapa y horario.', None),
    ('Completa', '', '$199', 'Todo lo de Básica, más menú o catálogo completo y formulario de pedidos o citas.', None),
    ('Diseño único', 'desde', '$369', 'Diseñada desde cero con tus colores y tu estilo. Incluye 2 rondas de cambios.',
     '100% original'),
]


def post_precios():
    im = base(1080, 1350)
    d = ImageDraw.Draw(im)
    d.ellipse((640, -260, 1340, 440), fill=BLUSH)
    kicker(d, (70, 80), 'Precios claros')
    d.text((66, 138), '¿Cuánto cuesta', font=fuente(92, 900), fill=NAVY)
    d.text((66, 238), 'tu página?', font=fuente(92, 900), fill=CORAL)
    d.text((72, 358), 'Pagas una sola vez. Elige el plan para tu negocio.', font=fuente(32, 500), fill=SOFT)
    y = 432
    for nombre, desde, precio, desc, etiqueta in PLANES:
        alto = 176
        sombra(im, (70, y, 1010, y + alto), 34, desp=(0, 12), difuso=22, alfa=28)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((70, y, 1010, y + alto), 34, fill=BLANCO)
        fn = fuente(44, 900)
        d.text((108, y + 30), nombre, font=fn, fill=NAVY)
        if etiqueta:
            pastilla(d, (108 + texto_ancho(d, nombre, fn) + 18, y + 34), etiqueta, fuente(22, 800), BLUSH, CORAL_D,
                     pad=(16, 9))
        parrafo(d, (108, y + 94), desc, fuente(25, 500), SOFT, 560, 1.32)
        fp = fuente(84, 900)
        px = 972 - texto_ancho(d, precio, fp)
        d.text((px, y + (alto - 84) / 2 - 8 + (14 if desde else 0)), precio, font=fp, fill=CORAL_D)
        if desde:
            fd = fuente(26, 700)
            d.text((972 - texto_ancho(d, desde, fd), y + 26), desde, font=fd, fill=SOFT)
        y += alto + 20
    # mantenimiento opcional
    y += 6
    d.rounded_rectangle((70, y, 1010, y + 150), 34, fill=MENTA_CLARO)
    d.text((108, y + 26), 'Mantenimiento opcional', font=fuente(36, 900), fill=NAVY)
    parrafo(d, (108, y + 76), 'Te cambiamos precios, fotos y horarios cuando lo necesites.', fuente(24, 500), SOFT,
            560, 1.3)
    fp = fuente(56, 900)
    t = '$15/mes'
    d.text((972 - texto_ancho(d, t, fp), y + 44), t, font=fp, fill=NAVY)
    pie_simple(im)
    return im


# ---------- 2. 4 páginas de ejemplo ----------

EJEMPLOS = [('panaderia', 'Panadería'), ('barberia', 'Barbería'), ('tienda', 'Tienda'), ('reposteria', 'Repostería')]


def post_ejemplos():
    im = base(1080, 1350)
    d = ImageDraw.Draw(im)
    d.ellipse((-220, 520, 560, 1300), fill=BLUSH)
    d.ellipse((620, 640, 1360, 1380), fill=MENTA_CLARO)
    pastilla(d, (70, 80), 'NUEVOS EJEMPLOS', fuente(30, 900), CORAL, NAVY, pad=(30, 16))
    d.text((66, 166), '4 páginas', font=fuente(130, 900), fill=NAVY)
    d.text((66, 300), 'de ejemplo', font=fuente(130, 900), fill=CORAL)
    parrafo(d, (72, 466), '¿Cuál estilo va con tu negocio? La hacemos con tus fotos, tus productos y tus colores.',
            fuente(34, 500), SOFT, 920, 1.32)
    ancho, hueco = 226, 25
    x0 = (1080 - (ancho * 4 + hueco * 3)) / 2
    for i, (slug, nombre) in enumerate(EJEMPLOS):
        x = x0 + i * (ancho + hueco)
        y = 600 + (44 if i % 2 else 0)
        _, h = celular_chico(im, (x, y), captura(slug), ancho)
        d = ImageDraw.Draw(im)
        f = fuente(32, 800)
        d.text((x + (ancho - texto_ancho(d, nombre, f)) / 2, y + h + 22), nombre, font=f, fill=NAVY)
    d.text((72, 1156), 'Negocios y datos de ejemplo', font=fuente(24, 500), fill=SOFT)
    pie_simple(im)
    return im


# ---------- 3. ¿Cómo funciona? ----------

PASOS = [
    ('Escríbenos', 'Por WhatsApp o Instagram y nos cuentas de tu negocio.'),
    ('Te armamos un ejemplo de tu página', 'Con tus fotos y tus colores, para que veas cómo queda.'),
    ('Lista en pocos días', 'Y compartes tu link con tus clientes.'),
]


def post_como_funciona():
    im = base(1080, 1350)
    d = ImageDraw.Draw(im)
    d.ellipse((660, -240, 1360, 460), fill=MENTA_CLARO)
    kicker(d, (70, 80), 'Así de fácil')
    d.text((66, 140), '¿Cómo', font=fuente(112, 900), fill=NAVY)
    d.text((66, 258), 'funciona?', font=fuente(112, 900), fill=CORAL)
    y = 430
    ft, fd = fuente(36, 900), fuente(27, 500)
    for n, (titulo, desc) in enumerate(PASOS, 1):
        # alto según cuántas líneas ocupe el texto
        lt = envolver(d, titulo, ft, 724)
        ld = envolver(d, desc, fd, 724)
        alto = 40 + len(lt) * 44 + 12 + len(ld) * 36 + 36
        sombra(im, (70, y, 1010, y + alto), 34, desp=(0, 12), difuso=22, alfa=28)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((70, y, 1010, y + alto), 34, fill=BLANCO)
        cy = y + alto / 2
        d.ellipse((104, cy - 56, 216, cy + 56), fill=CORAL)
        fnum = fuente(64, 900)
        s = str(n)
        d.text((160 - texto_ancho(d, s, fnum) / 2, cy - 40), s, font=fnum, fill=NAVY)
        ty = y + 40
        for linea in lt:
            d.text((256, ty), linea, font=ft, fill=NAVY); ty += 44
        ty += 12
        for linea in ld:
            d.text((256, ty), linea, font=fd, fill=SOFT); ty += 36
        y += alto + 22
    fin = boton_pagina(d, y + 24)
    assert fin < 1200, fin
    pie_simple(im)
    return im


# ---------- 4. Tu negocio en internet, ya ----------

def post_tu_negocio():
    im = base(1080, 1350)
    d = ImageDraw.Draw(im)
    d.ellipse((480, 560, 1300, 1380), fill=BLUSH)
    d.ellipse((-200, 1060, 200, 1460), fill=MENTA_CLARO)
    f = fuente(124, 900)
    y = 84
    for linea, c in (('Tu negocio', NAVY), ('en internet,', NAVY), ('ya.', CORAL)):
        d.text((64, y), linea, font=f, fill=c); y += 132
    parrafo(d, (72, y + 22), 'Hacemos páginas web para negocios en Panamá. Listas en pocos días.', fuente(38, 600),
            SOFT, 900, 1.3)
    yb = 700
    for t in ('Tus productos con foto', 'Pedidos por WhatsApp', 'Horario y ubicación', 'Tu link para compartir'):
        d.rounded_rectangle((72, yb, 92, yb + 20), 6, fill=MENTA)
        d.text((112, yb - 14), t, font=fuente(34, 700), fill=NAVY)
        yb += 66
    celular_chico(im, (548, 700), captura('panaderia'), 240, girar=-5)
    celular_chico(im, (784, 650), pantalla_portada(600, 1170), 240, girar=4)
    d = ImageDraw.Draw(im)
    d.text((72, 1156), 'Negocios y datos de ejemplo', font=fuente(24, 500), fill=SOFT)
    pie_simple(im)
    return im


# ---------- 5. Síguenos para más ----------

def post_siguenos():
    im = base(1080, 1350, NAVY)
    puntos_fondo(im, (36, 54, 90, 255), paso=80, r=5)
    d = ImageDraw.Draw(im)
    tam = 110
    fl = fuente(int(tam * 0.62), 900)
    ancho_logo = tam + tam * 0.22 + texto_ancho(d, 'SitioYa', fl)
    logo_sitioya(im, ((1080 - ancho_logo) / 2, 150), tam, oscuro=True)
    d = ImageDraw.Draw(im)
    f = fuente(150, 900)
    y = 340
    for linea, c in (('Síguenos', CREMA), ('para más', CORAL)):
        d.text(((1080 - texto_ancho(d, linea, f)) / 2, y), linea, font=f, fill=c); y += 160
    y += 40
    fi = fuente(40, 700)
    items = ('Páginas de ejemplo', 'Precios claros', 'Tips para tu negocio')
    ancho_lista = max(texto_ancho(d, t, fi) for t in items) + 50
    x = (1080 - ancho_lista) / 2
    for t in items:
        d.rounded_rectangle((x, y + 14, x + 24, y + 38), 7, fill=MENTA)
        d.text((x + 50, y), t, font=fi, fill=CREMA)
        y += 74
    y += 40
    pastilla(d, (540, y), '@sitioya.pty', fuente(56, 900), CORAL, NAVY, pad=(48, 24), centro=True)
    parrafo(d, (540, 1200), 'Hacemos páginas web para negocios en Panamá', fuente(30, 500), '#C9D1E3', 900, 1.3,
            centrado=True)
    return im


POSTS = [
    ('1-tu-negocio-en-internet.png', post_tu_negocio),
    ('2-como-funciona.png', post_como_funciona),
    ('3-paginas-de-ejemplo.png', post_ejemplos),
    ('4-precios.png', post_precios),
    ('5-siguenos.png', post_siguenos),
]


def main():
    for nombre, hacer in POSTS:
        im = hacer()
        assert im.size == (1080, 1350), (nombre, im.size)
        im.convert('RGB').save(os.path.join(SALIDA, nombre), optimize=True)
        print(nombre, im.size)


if __name__ == '__main__':
    main()
