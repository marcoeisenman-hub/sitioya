# Genera los posts del feed de @sitioya.pty (1080x1350) con el mismo estilo
# del carrusel de la Heladería, en el orden para publicar (ver FEED abajo),
# y la galería redes/posts/index.html con los captions.
# Uso: python3 tools/redes_posts.py  -> redes/posts/*.png + index.html
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from redes_heladeria import (  # noqa: E402
    BLANCO, BLUSH, CORAL, CORAL_D, CREMA, MENTA, NAVY, SOFT, RAIZ,
    base, envolver, foto, fuente, kicker, logo_sitioya, pantalla_portada, parrafo, pastilla,
    puntos_fondo, sombra, texto_ancho,
)

SALIDA = os.path.join(RAIZ, 'redes', 'posts')
SHOTS = os.path.join(RAIZ, 'img', 'shots')
os.makedirs(SALIDA, exist_ok=True)
MENTA_CLARO = '#DDF4EC'


def captura(nombre):
    """Captura de celular de una página de ejemplo, sin el botón flotante de abajo."""
    im = Image.open(os.path.join(SHOTS, nombre + '_mob.jpg')).convert('RGBA')
    im = im.crop((0, 0, im.width, 712))
    # franja arriba (del color de la página) para que la muesca del celular no tape el nombre
    franja = 48
    con_franja = Image.new('RGBA', (im.width, im.height + franja), im.getpixel((2, 2)))
    con_franja.paste(im, (0, franja))
    return con_franja


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


# ---------- 6. 3 cosas que tu página debe tener ----------

TRES_COSAS = [
    ('Tus productos con foto', 'Que vean lo que vendes sin tener que preguntarte.'),
    ('Un botón para escribirte', 'Que te pidan o te consulten con un toque.'),
    ('Horario y cómo llegar', 'Que sepan cuándo abres y dónde encontrarte.'),
]


def post_tres_cosas():
    im = base(1080, 1350)
    d = ImageDraw.Draw(im)
    d.ellipse((-260, 760, 420, 1440), fill=BLUSH)
    kicker(d, (70, 80), 'Tip para tu negocio')
    f = fuente(92, 900)
    d.text((66, 134), '3 cosas que', font=f, fill=NAVY)
    d.text((66, 234), 'tu página', font=f, fill=CORAL)
    d.text((66, 334), 'debe tener', font=f, fill=CORAL)
    y = 480
    ft, fd = fuente(38, 900), fuente(27, 500)
    for n, (titulo, desc) in enumerate(TRES_COSAS, 1):
        ld = envolver(d, desc, fd, 700)
        alto = 34 + 48 + 8 + len(ld) * 36 + 32
        sombra(im, (70, y, 1010, y + alto), 34, desp=(0, 12), difuso=22, alfa=28)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((70, y, 1010, y + alto), 34, fill=BLANCO)
        cy = y + alto / 2
        d.ellipse((104, cy - 52, 208, cy + 52), fill=MENTA)
        fnum = fuente(60, 900)
        s = str(n)
        d.text((156 - texto_ancho(d, s, fnum) / 2, cy - 38), s, font=fnum, fill=NAVY)
        d.text((248, y + 34), titulo, font=ft, fill=NAVY)
        ty = y + 34 + 48 + 8
        for linea in ld:
            d.text((248, ty), linea, font=fd, fill=SOFT); ty += 36
        y += alto + 22
    fin = boton_pagina(d, y + 18)
    assert fin < 1200, fin
    pie_simple(im)
    return im


# ---------- 7. Antes y después ----------

GRIS = '#EDE5DC'
GRIS_D = '#B9AFA6'


def icono(d, cx, cy, ok):
    """Círculo con ✓ (después) o ✕ (antes), dibujado con líneas."""
    r = 19
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=MENTA if ok else GRIS_D)
    c = NAVY if ok else BLANCO
    if ok:
        d.line((cx - 9, cy + 1, cx - 2, cy + 8, cx + 10, cy - 7), fill=c, width=6, joint='curve')
    else:
        d.line((cx - 7, cy - 7, cx + 7, cy + 7), fill=c, width=5)
        d.line((cx - 7, cy + 7, cx + 7, cy - 7), fill=c, width=5)


def lupa(d, cx, cy, r, color, ancho):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=ancho)
    d.line((cx + r * 0.7, cy + r * 0.7, cx + r * 1.5, cy + r * 1.5), fill=color, width=ancho)


def pantalla_sin_pagina(w, h):
    """'Antes': te buscan y no aparece nada."""
    im = Image.new('RGBA', (w, h), '#F6F1EB')
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((30, 90, w - 30, 170), 40, fill=BLANCO, outline='#E2D8CE', width=3)
    lupa(d, 78, 128, 14, GRIS_D, 5)
    d.text((112, 110), 'tu negocio', font=fuente(30, 500), fill=GRIS_D)
    cy = 420
    d.ellipse((w / 2 - 110, cy - 110, w / 2 + 110, cy + 110), fill=GRIS)
    lupa(d, w / 2 - 12, cy - 12, 46, GRIS_D, 14)
    parrafo(d, (w / 2, cy + 160), 'No encontramos tu página', fuente(38, 800), '#8E847B', w - 80, 1.25, centrado=True)
    y = cy + 290
    for ancho in (0.8, 0.62, 0.7):
        d.rounded_rectangle((60, y, 60 + (w - 120) * ancho, y + 28), 14, fill=GRIS); y += 56
    return im


def post_antes_despues():
    im = base(1080, 1350)
    d = ImageDraw.Draw(im)
    d.ellipse((600, 300, 1360, 1060), fill=MENTA_CLARO)
    kicker(d, (70, 80), 'Tu negocio sin y con página')
    f = fuente(112, 900)
    d.text((66, 136), 'Antes', font=f, fill=NAVY)
    d.text((66 + texto_ancho(d, 'Antes ', f), 136), 'y después', font=f, fill=CORAL)
    cols = [
        (70, 'ANTES', GRIS, '#8E847B', pantalla_sin_pagina(600, 1170), False,
         ('No te encuentran', 'Precios solo por mensaje', 'Sin link para compartir')),
        (560, 'DESPUÉS', CORAL, NAVY, captura('reposteria'), True,
         ('Tu página con tu nombre', 'Precios y horario a la vista', 'Tu link para compartir')),
    ]
    for x, etiqueta, fondo_et, color_et, pantalla, ok, items in cols:
        d = ImageDraw.Draw(im)
        pastilla(d, (x + 225, 300), etiqueta, fuente(28, 900), fondo_et, color_et if not ok else NAVY, pad=(28, 12),
                 centro=True)
        celular_chico(im, (x + 95, 378), pantalla, 260)
        d = ImageDraw.Draw(im)
        y = 916
        fi = fuente(30, 700)
        for t in items:
            icono(d, x + 30, y + 18, ok)
            ty = parrafo(d, (x + 64, y), t, fi, NAVY if ok else SOFT, 370, 1.2)
            y = max(ty, y + 40) + 18
        assert y < 1150, (etiqueta, y)
    # flecha entre los dos celulares
    d = ImageDraw.Draw(im)
    d.ellipse((498, 604, 582, 688), fill=NAVY)
    d.line((520, 646, 560, 646), fill=CREMA, width=8)
    d.polygon([(560, 630), (574, 646), (560, 662)], fill=CREMA)
    d.text((72, 1160), 'Negocio y datos de ejemplo', font=fuente(24, 500), fill=SOFT)
    pie_simple(im)
    return im


# ---------- 8. ¿Vendes por Instagram? (pedidos por DM vs página) ----------
# Tienda ficticia "brisa." (la misma de la página de ejemplo de tienda), sin
# precios, sin cifras de seguidores y sin logos: el perfil es genérico.

TIENDA_FOTOS = [
    ('1664515226058-03952a19bd76.jpg', 'Vestido rojo'),
    ('1628667970085-82d3731ef568.jpg', 'Set blanco y rojo'),
    ('1659522761084-79196b64abe4.jpg', 'Vestido blanco'),
    ('1661705150795-b608b9fe58c6.jpg', 'Camisa azul'),
    ('1678884399113-0a2b079a31f5.jpg', 'Chaqueta blanca'),
    ('1516762689617-e1cffcef479d.jpg', 'Look casual'),
]
T_INK = '#161616'
T_SOFT = '#6B6B6B'


def logo_brisa(d, xy, tam, color=T_INK):
    d.text(xy, 'brisa.', font=fuente(tam, 800), fill=color)


def pantalla_perfil(w, h):
    """Perfil genérico de una tienda que vende por mensajes (sin logo de ninguna red)."""
    im = Image.new('RGBA', (w, h), BLANCO)
    d = ImageDraw.Draw(im)
    # cabecera: foto de perfil + nombre + bio
    av = 150
    d.ellipse((34, 96, 34 + av, 96 + av), fill='#F3EEE8')
    logo_brisa(d, (34 + 26, 96 + 50), 38)
    d.text((216, 112), 'brisa.', font=fuente(40, 900), fill=T_INK)
    parrafo(d, (216, 168), 'Ropa fresca · Panamá. Pedidos por mensaje', fuente(25, 500), T_SOFT, w - 250, 1.3)
    d.rounded_rectangle((34, 276, w - 34, 344), 18, fill='#EFEFEF')
    t = 'Mensaje'
    fb = fuente(27, 800)
    d.text(((w - texto_ancho(d, t, fb)) / 2, 293), t, font=fb, fill=T_INK)
    # cuadrícula de fotos
    lado = (w - 6) // 3
    for i, (img, _) in enumerate(TIENDA_FOTOS):
        x = (i % 3) * (lado + 3)
        y = 372 + (i // 3) * (lado + 3)
        im.alpha_composite(foto(img, (lado, lado)).convert('RGBA'), (x, y))
    # mensajes que llegan uno por uno
    d = ImageDraw.Draw(im)
    y = 372 + 2 * (lado + 3) + 34
    fm = fuente(28, 600)
    for i, t in enumerate(('¿Precio?', '¿Tienen talla M?', '¿Hacen envíos?', '¿Precio del azul?')):
        tw = texto_ancho(d, t, fm) + 52
        x = 30 if i % 2 == 0 else 70
        d.rounded_rectangle((x, y, x + tw, y + 70), 35, fill='#EFEFEF')
        d.text((x + 26, y + 18), t, font=fm, fill=T_INK)
        y += 88
    return im


def pantalla_tienda(w, h):
    """La página de la misma tienda: catálogo con foto y botón para pedir por WhatsApp."""
    im = Image.new('RGBA', (w, h), '#FAF8F5')
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w, 178), fill=BLANCO)
    logo_brisa(d, (34, 96), 50)
    d.text((34, 214), 'Ropa fresca', font=fuente(54, 900), fill=T_INK)
    d.text((34, 276), 'para los días de calor', font=fuente(34, 700), fill=T_SOFT)
    chips = ('Todo', 'Vestidos', 'Tops', 'Looks')
    x = 34
    for i, c in enumerate(chips):
        fc = fuente(24, 700)
        x2, _ = pastilla(d, (x, 346), c, fc, T_INK if i == 0 else '#ECE8E2', BLANCO if i == 0 else T_INK, pad=(22, 12))
        x = x2 + 12
    cw = (w - 34 * 2 - 20) // 2
    ih = int(cw * 0.78)
    y0 = 430
    for i, (img, nombre) in enumerate(TIENDA_FOTOS[:4]):
        col, fila = i % 2, i // 2
        x = 34 + col * (cw + 20)
        y = y0 + fila * (ih + 112)
        im.alpha_composite(foto(img, (cw, ih), 22), (x, y))
        d = ImageDraw.Draw(im)
        d.text((x + 4, y + ih + 14), nombre, font=fuente(25, 800), fill=T_INK)
        fb = fuente(21, 800)
        d.rounded_rectangle((x + 4, y + ih + 56, x + 4 + texto_ancho(d, 'Lo quiero', fb) + 36, y + ih + 98), 21,
                            outline=T_INK, width=3)
        d.text((x + 22, y + ih + 63), 'Lo quiero', font=fb, fill=T_INK)
    # botón fijo para pedir (sin logo, solo texto)
    fb = fuente(30, 900)
    t = 'Pedir por WhatsApp'
    bw = texto_ancho(d, t, fb) + 80
    d.rounded_rectangle(((w - bw) / 2, h - 104, (w + bw) / 2, h - 20), 42, fill=MENTA)
    d.text(((w - texto_ancho(d, t, fb)) / 2, h - 83), t, font=fb, fill=NAVY)
    return im


def post_vendes_instagram():
    im = base(1080, 1350)
    d = ImageDraw.Draw(im)
    d.ellipse((560, 380, 1340, 1160), fill=BLUSH)
    d.text((66, 76), '¿Vendes por Instagram?', font=fuente(78, 900), fill=NAVY)
    d.text((66, 172), 'Así se vería tu negocio', font=fuente(60, 900), fill=CORAL)
    d.text((66, 244), 'con página', font=fuente(60, 900), fill=CORAL)
    cols = [
        (70, 'SOLO MENSAJES', GRIS, '#8E847B', pantalla_perfil(600, 1170)),
        (560, 'CON PÁGINA', CORAL, NAVY, pantalla_tienda(600, 1170)),
    ]
    for x, etiqueta, fondo_et, color_et, pantalla in cols:
        d = ImageDraw.Draw(im)
        pastilla(d, (x + 225, 352), etiqueta, fuente(26, 900), fondo_et, color_et, pad=(26, 12), centro=True)
        celular_chico(im, (x + 75, 424), pantalla, 300)
    d = ImageDraw.Draw(im)
    d.ellipse((498, 690, 582, 774), fill=NAVY)
    d.line((520, 732, 560, 732), fill=CREMA, width=8)
    d.polygon([(560, 716), (574, 732), (560, 748)], fill=CREMA)
    d = ImageDraw.Draw(im)
    parrafo(d, (540, 1060), 'Todo en un solo lugar y te piden directo.', fuente(34, 800), NAVY, 940, 1.25,
            centrado=True)
    # texto chico de abajo: 'Hacemos páginas para negocios en Panamá. @sitioya.pty'
    fs = fuente(28, 600)
    partes = (('Hacemos páginas para negocios en Panamá. ', SOFT), ('@sitioya.pty', CORAL_D))
    x = (1080 - sum(texto_ancho(d, t, fs) for t, _ in partes)) / 2
    for t, c in partes:
        d.text((x, 1150), t, font=fs, fill=c)
        x += texto_ancho(d, t, fs)
    # pie: logo a la izquierda y el aviso de que la tienda es de ejemplo a la derecha
    logo_sitioya(im, (70, 1350 - 120), 58)
    d = ImageDraw.Draw(im)
    t = 'Tienda y datos de ejemplo'
    fe = fuente(24, 500)
    d.text((1080 - 70 - texto_ancho(d, t, fe), 1350 - 102), t, font=fe, fill=SOFT)
    return im


# ---------- 10. 3 cosas que pierde tu negocio sin página ----------

PIERDE = [
    ('Clientes que te buscan', 'Si te buscan en internet, puede que no te encuentren.'),
    ('Tiempo', 'Contestas lo mismo todo el día: precio, horario y dónde estás.'),
    ('Pedidos cuando estás ocupado', 'Si no contestas a tiempo, el cliente puede irse a otro lado.'),
]


def post_pierde_sin_pagina():
    im = base(1080, 1350)
    d = ImageDraw.Draw(im)
    d.ellipse((640, -260, 1340, 440), fill=BLUSH)
    d.ellipse((-240, 980, 300, 1520), fill=MENTA_CLARO)
    kicker(d, (70, 80), 'Ojo con esto')
    f = fuente(92, 900)
    for i, (linea, c) in enumerate((('3 cosas que', NAVY), ('pierde tu negocio', CORAL), ('sin página', CORAL))):
        assert 66 + texto_ancho(d, linea, f) < 1030, linea
        d.text((66, 134 + i * 100), linea, font=f, fill=c)
    y = 470
    ft, fd = fuente(38, 900), fuente(27, 500)
    for n, (titulo, desc) in enumerate(PIERDE, 1):
        ld = envolver(d, desc, fd, 730)
        alto = 30 + 48 + 6 + len(ld) * 36 + 28
        sombra(im, (70, y, 1010, y + alto), 34, desp=(0, 12), difuso=22, alfa=28)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((70, y, 1010, y + alto), 34, fill=BLANCO)
        cy = y + alto / 2
        d.ellipse((104, cy - 52, 208, cy + 52), fill=BLUSH)
        fnum = fuente(60, 900)
        s = str(n)
        d.text((156 - texto_ancho(d, s, fnum) / 2, cy - 38), s, font=fnum, fill=CORAL_D)
        d.text((248, y + 30), titulo, font=ft, fill=NAVY)
        ty = y + 30 + 48 + 6
        for linea in ld:
            d.text((248, ty), linea, font=fd, fill=SOFT); ty += 36
        y += alto + 20
    fin = boton_pagina(d, y + 16)
    assert fin < 1200, fin
    pie_simple(im)
    return im


# ---------- 11. Por qué tu negocio necesita página y no solo Instagram ----------

COMPARA = [
    ('Tus productos se pierden entre posts', 'Tus productos ordenados en un catálogo'),
    ('Te preguntan todo por mensaje', 'Precios, horario y ubicación a la vista'),
    ('Lo importante se pierde en historias de 24 horas', 'Lo importante siempre en el mismo lugar'),
    ('Dependes de una sola red', 'Un lugar en internet que es tuyo'),
]


def post_no_solo_instagram():
    im = base(1080, 1350)
    d = ImageDraw.Draw(im)
    d.ellipse((620, -280, 1340, 420), fill=MENTA_CLARO)
    f = fuente(76, 900)
    for i, (linea, c) in enumerate((('¿Por qué tu negocio', NAVY), ('necesita página', CORAL),
                                    ('y no solo Instagram?', NAVY))):
        assert 66 + texto_ancho(d, linea, f) < 1030, linea
        d.text((66, 80 + i * 86), linea, font=f, fill=c)
    # encabezados de las dos columnas
    pastilla(d, (305, 372), 'SOLO INSTAGRAM', fuente(26, 900), GRIS, '#8E847B', pad=(26, 12), centro=True)
    pastilla(d, (775, 372), 'CON PÁGINA', fuente(26, 900), CORAL, NAVY, pad=(26, 12), centro=True)
    y = 450
    fi = fuente(28, 700)
    for antes, despues in COMPARA:
        la = envolver(d, antes, fi, 362)
        lb = envolver(d, despues, fi, 362)
        alto = 30 + max(len(la), len(lb)) * 36 + 26
        sombra(im, (70, y, 1010, y + alto), 30, desp=(0, 10), difuso=20, alfa=26)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((70, y, 1010, y + alto), 30, fill=BLANCO)
        d.rounded_rectangle((540, y, 1010, y + alto), 30, fill='#FFF1EC')
        d.rectangle((540, y, 580, y + alto), fill='#FFF1EC')
        cy = y + alto / 2
        for x, lineas, ok in ((70, la, False), (540, lb, True)):
            icono(d, x + 46, cy, ok)
            ty = cy - len(lineas) * 36 / 2 - 2
            for linea in lineas:
                d.text((x + 86, ty), linea, font=fi, fill=NAVY if ok else SOFT); ty += 36
        y += alto + 16
    y += 18
    y = parrafo(d, (540, y), 'Usa los dos: Instagram para que te conozcan', fuente(31, 800), NAVY, 940, 1.3,
                centrado=True)
    y = parrafo(d, (540, y), 'y tu página para que te compren.', fuente(31, 800), CORAL_D, 940, 1.3, centrado=True)
    assert y < 1200, y
    pie_simple(im)
    return im


# ---------- 12. Te armamos un ejemplo gratis de tu página ----------

PASOS_EJEMPLO = [
    'Nos cuentas de tu negocio',
    'Te armamos un ejemplo con tu nombre y tus colores',
    'Lo ves y decides si la quieres',
]


def post_ejemplo_gratis():
    im = base(1080, 1350)
    d = ImageDraw.Draw(im)
    d.ellipse((520, 520, 1340, 1340), fill=BLUSH)
    pastilla(d, (70, 80), 'PARA TU NEGOCIO', fuente(30, 900), CORAL, NAVY, pad=(30, 16))
    f = fuente(98, 900)
    for i, (linea, c) in enumerate((('Te armamos', NAVY), ('un ejemplo gratis', NAVY), ('de tu página', CORAL))):
        assert 66 + texto_ancho(d, linea, f) < 1030, linea
        d.text((66, 160 + i * 106), linea, font=f, fill=c)
    parrafo(d, (72, 498), 'Para que veas cómo quedaría tu negocio en internet antes de decidir.', fuente(34, 500),
            SOFT, 900, 1.32)
    # pasos a la izquierda
    y = 640
    ft = fuente(34, 800)
    for n, t in enumerate(PASOS_EJEMPLO, 1):
        lt = envolver(d, t, ft, 420)
        alto = max(84, len(lt) * 44)
        cy = y + alto / 2
        d.ellipse((72, cy - 36, 144, cy + 36), fill=MENTA)
        fnum = fuente(42, 900)
        d.text((108 - texto_ancho(d, str(n), fnum) / 2, cy - 27), str(n), font=fnum, fill=NAVY)
        ty = cy - len(lt) * 44 / 2 - 4
        for linea in lt:
            d.text((172, ty), linea, font=ft, fill=NAVY); ty += 44
        y += alto + 34
    x2, yb = pastilla(d, (72, y + 6), 'Comenta PÁGINA y te contamos', fuente(30, 900), CORAL, NAVY, pad=(30, 18))
    assert x2 < 660 and yb < 1140, (x2, yb)
    # celular con una página de ejemplo a la derecha
    _, h = celular_chico(im, (700, 600), pantalla_portada(600, 1170), 300, girar=4)
    assert 600 + h < 1200, h
    d = ImageDraw.Draw(im)
    d.text((72, 1156), 'Negocio y datos de ejemplo', font=fuente(24, 500), fill=SOFT)
    pie_simple(im)
    return im


# ---------- 13. Síguenos: Tu negocio merece una página web ----------
# Celulares con dos páginas de ejemplo: la Heladería del carrusel "Ejemplo de la
# semana" (Nieve & Co) y el menú de Mesa Lunar (plantillas/menu.html).

def post_merece_pagina():
    im = base(1080, 1350)
    d = ImageDraw.Draw(im)
    d.ellipse((-260, 420, 520, 1200), fill=BLUSH)
    d.ellipse((600, 500, 1380, 1280), fill=MENTA_CLARO)
    pastilla(d, (70, 74), 'SÍGUENOS', fuente(30, 900), CORAL, NAVY, pad=(30, 16))
    f = fuente(100, 900)
    for i, (linea, c) in enumerate((('Tu negocio merece', NAVY), ('una página web', CORAL))):
        assert 66 + texto_ancho(d, linea, f) < 1010, linea
        d.text((66, 152 + i * 108), linea, font=f, fill=c)
    # dos celulares, un poco girados
    ancho = 304
    telefonos = (
        (130, 404, pantalla_portada(600, 1170), -4, 'Heladería'),
        (640, 390, captura('menu'), 4, 'Menú de restaurante'),
    )
    for x, y, pantalla, giro, nombre in telefonos:
        w, h = celular_chico(im, (x, y), pantalla, ancho, girar=giro)
        d = ImageDraw.Draw(im)
        x2, y2 = pastilla(d, (x + w / 2, y + h - 34), nombre, fuente(28, 900), NAVY, CREMA, pad=(24, 12), centro=True)
        assert y2 < 1064, (nombre, y2)
    # texto de abajo
    y = parrafo(d, (540, 1082), 'Hacemos páginas para negocios en Panamá.', fuente(34, 800), NAVY, 960, 1.25,
                centrado=True)
    fs = fuente(34, 800)
    partes = (('Síguenos en ', NAVY), ('@sitioya.pty', CORAL_D), (' y mira ejemplos', NAVY))
    x = (1080 - sum(texto_ancho(d, t, fs) for t, _ in partes)) / 2
    for t, c in partes:
        d.text((x, y), t, font=fs, fill=c)
        x += texto_ancho(d, t, fs)
    assert y + 44 < 1170, y
    d.text((72, 1180), 'Negocios y datos de ejemplo', font=fuente(22, 500), fill=SOFT)
    pie_simple(im)
    return im


# Orden sugerido de publicación (el último en salir queda arriba en el perfil).
# El 4 es el carrusel de la Heladería, que sale de tools/redes_heladeria.py.
HELADERIA = 'heladeria'
FEED = [
    ('1-tu-negocio-en-internet.png', post_tu_negocio, 'Tu negocio en internet, ya',
     'Tu negocio en internet, ya. Hacemos páginas web para negocios en Panamá, listas en pocos días. '
     '¿Tu negocio ya tiene página? Sí o no, te leemos en los comentarios'),
    ('2-como-funciona.png', post_como_funciona, '¿Cómo funciona?',
     '¿Cómo funciona? 1. Escríbenos 2. Te armamos un ejemplo de tu página 3. Lista en pocos días y compartes '
     'tu link. Escríbenos por WhatsApp al 6919-7559 y empezamos'),
    ('3-paginas-de-ejemplo.png', post_ejemplos, '4 páginas de ejemplo',
     '4 páginas de ejemplo: panadería, barbería, tienda y repostería. ¿Cuál estilo va con tu negocio? '
     'Dinos en los comentarios'),
    (HELADERIA, None, 'Carrusel: Ejemplo de la semana, Heladería',
     'Ejemplo de la semana: Heladería. Así podría quedar la página de tu negocio. Compártelo con alguien que '
     'tenga negocio'),
    ('5-tres-cosas-que-tu-pagina-debe-tener.png', post_tres_cosas, '3 cosas que tu página debe tener',
     '3 cosas que tu página debe tener: tus productos con foto, un botón para escribirte y tu horario y cómo '
     'llegar. ¿La tuya las tiene? Guárdalo para cuando armes la tuya'),
    ('6-antes-y-despues.png', post_antes_despues, 'Antes y después',
     'Antes: te buscan y no te encuentran. Después: tu página con tus precios, tu horario y tu link para '
     'compartir. ¿Quieres pasar al después? Escríbenos por WhatsApp al 6919-7559'),
    ('7-vendes-por-instagram.png', post_vendes_instagram, '¿Vendes por Instagram?',
     '¿Vendes solo por Instagram? Con una página tus clientes ven todo en un solo lugar y te piden directo. '
     'Compártelo con alguien que venda por mensajes'),
    ('8-precios.png', post_precios, 'Precios',
     'Precios claros: Básica $99, Completa $199 y Diseño único desde $369. Pagas una sola vez y el '
     'mantenimiento de $15/mes es opcional. Comenta PÁGINA y te contamos'),
    ('9-siguenos.png', post_siguenos, 'Síguenos para más',
     'Síguenos para ver páginas de ejemplo, precios claros y tips para tu negocio. Hacemos páginas web para '
     'negocios en Panamá'),
    # extra (se publican después del 9, así el 12 queda arriba en el perfil)
    ('10-tres-cosas-que-pierde-tu-negocio.png', post_pierde_sin_pagina, '3 cosas que pierde tu negocio sin página',
     '3 cosas que pierde tu negocio sin página: clientes que te buscan, tiempo contestando lo mismo y pedidos '
     'cuando estás ocupado. Guárdalo para cuando lo necesites'),
    ('11-pagina-y-no-solo-instagram.png', post_no_solo_instagram, 'Por qué página y no solo Instagram',
     'Instagram para que te conozcan y tu página para que te compren: tus productos ordenados, tus precios y tu '
     'horario a la vista y todo siempre en el mismo lugar. ¿Tu negocio ya tiene página o solo redes? '
     'Cuéntanos en los comentarios'),
    ('12-ejemplo-gratis-de-tu-pagina.png', post_ejemplo_gratis, 'Te armamos un ejemplo gratis de tu página',
     'Te armamos un ejemplo gratis de tu página para que veas cómo quedaría tu negocio antes de decidir. '
     'Comenta PÁGINA y te contamos'),
    ('13-siguenos-tu-negocio-merece-pagina.png', post_merece_pagina, 'Síguenos: Tu negocio merece una página web',
     'Hacemos páginas web para negocios en Panamá. Síguenos para ver más ejemplos y tips para tu '
     'negocio'),
]
STORY = ('/redes/ejemplo-heladeria/story-encuesta.png', 'Story: ¿Tu negocio tiene página web?',
         'En el recuadro de arriba va el sticker de encuesta con la pregunta "¿Tu negocio tiene página web?" y '
         'las opciones Sí / No (o, en otra story, la cajita de preguntas: "¿Qué quieres saber de tener tu '
         'página?"). En el recuadro de abajo va el sticker de mención @sitioya.pty.')
SLIDES_HELADERIA = ['heladeria-1-portada.png', 'heladeria-2-sabores.png', 'heladeria-3-pedidos.png',
                    'heladeria-4-cierre.png']


def galeria():
    """redes/posts/index.html: los posts en orden + la story, con su caption y botón para descargar."""
    from html import escape as e
    tarjetas = []
    for n, (nombre, _, titulo, caption) in enumerate(FEED, 1):
        if nombre == HELADERIA:
            rutas = ['/redes/ejemplo-heladeria/' + s for s in SLIDES_HELADERIA]
            img, alt = rutas[0], titulo
            botones = ' '.join(f'<a class="b" href="{r}" download>Slide {i}</a>' for i, r in enumerate(rutas, 1))
        else:
            img, alt = nombre, titulo
            botones = f'<a class="b" href="{nombre}" download>Descargar</a>'
        tarjetas.append(
            f'<figure><a href="{img}" download><img src="{img}" alt="{e(alt)}" loading="lazy"></a>'
            f'<figcaption><b>{n}. {e(titulo)}</b><p>{e(caption)}</p>{botones}</figcaption></figure>')
    s_img, s_titulo, s_texto = STORY
    tarjetas.append(
        f'<figure><a href="{s_img}" download><img src="{s_img}" alt="{e(s_titulo)}" loading="lazy"></a>'
        f'<figcaption><b>{e(s_titulo)}</b><p>{e(s_texto)}</p><a class="b" href="{s_img}" download>Descargar</a>'
        f'</figcaption></figure>')
    total = len(FEED)
    html = (
        '<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" '
        'content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Posts de '
        '@sitioya.pty</title><link rel="icon" href="/favicon.svg">\n<style>body{margin:0;font-family:system-ui,'
        '-apple-system,sans-serif;background:#FFF6EC;color:#1B2A4A}main{max-width:1100px;margin:0 auto;padding:32px '
        '20px}h1{margin:0 0 6px}.s{color:#5B6680;margin:0 0 28px}.g{display:grid;grid-template-columns:repeat('
        'auto-fill,minmax(min(100%,300px),1fr));gap:24px}figure{margin:0;background:#fff;border-radius:22px;'
        'overflow:hidden;box-shadow:0 10px 30px rgba(27,42,74,.08)}img{width:100%;display:block}figcaption{padding:'
        '16px 18px 20px}figcaption p{color:#5B6680;margin:8px 0 14px;line-height:1.4}.b{display:inline-block;'
        'background:#FF6B5B;color:#1B2A4A;font-weight:800;padding:10px 18px;border-radius:99px;text-decoration:'
        f'none;margin:0 6px 6px 0}}</style></head>\n<body><main><h1>Posts de @sitioya.pty</h1><p class="s">Los '
        f'{total} en el orden para publicar (del 1 al {total}). El último en salir queda arriba en el perfil. El 4 '
        f'es un carrusel de 4 slides. Al final, la story de la encuesta (1080x1920).</p><div class="g">\n'
        + '\n'.join(tarjetas) + '\n</div></main></body></html>\n')
    with open(os.path.join(SALIDA, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    for nombre, hacer, _, _ in FEED:
        if hacer is None:
            continue
        im = hacer()
        assert im.size == (1080, 1350), (nombre, im.size)
        im.convert('RGB').save(os.path.join(SALIDA, nombre), optimize=True)
        print(nombre, im.size)
    galeria()
    print('index.html')


if __name__ == '__main__':
    main()
