# Genera el carrusel "Ejemplo de la semana: Heladería" (4 slides 1080x1350)
# y la story de encuesta (1080x1920) para @sitioya.pty.
# Uso: python3 tools/redes_heladeria.py  -> redes/ejemplo-heladeria/*.png
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOTOS = os.path.join(RAIZ, 'img', 'f')
SALIDA = os.path.join(RAIZ, 'redes', 'ejemplo-heladeria')
os.makedirs(SALIDA, exist_ok=True)

# Colores SitioYa
CREMA = '#FFF6EC'; NAVY = '#1B2A4A'; SOFT = '#5B6680'; CORAL = '#FF6B5B'; CORAL_D = '#E2503F'
MENTA = '#7ED6C1'; BLUSH = '#FFE3DC'; LINEA = '#F0DFCC'; BLANCO = '#FFFFFF'
# Colores de la página de ejemplo (heladería)
H_BG = '#FFF8F2'; H_INK = '#3A2440'; H_SOFT = '#7A6380'; H_ROSA = '#FF5C8A'; H_ROSA_D = '#E0427A'
H_AMARILLO = '#FFC53D'; H_MENTA = '#BFEBDD'; H_LILA = '#3A2440'

SF = '/System/Library/Fonts/SFNS.ttf'
SFR = '/System/Library/Fonts/SFNSRounded.ttf'
_cache = {}


def fuente(tam, peso=800, redonda=False):
    clave = (tam, peso, redonda)
    if clave not in _cache:
        f = ImageFont.truetype(SFR if redonda else SF, tam)
        ejes = f.get_variation_axes()
        valores = []
        for e in ejes:
            n = e['name']
            if n == b'Weight':
                valores.append(peso)
            elif n == b'Optical Size':
                valores.append(min(96, max(17, tam // 2)))
            else:
                valores.append(e['default'])
        f.set_variation_by_axes(valores)
        _cache[clave] = f
    return _cache[clave]


def foto(nombre, tam, radio=0):
    im = Image.open(os.path.join(FOTOS, nombre)).convert('RGB')
    w, h = tam
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r + 1), int(im.height * r + 1)), Image.LANCZOS)
    x = (im.width - w) // 2; y = (im.height - h) // 2
    im = im.crop((x, y, x + w, y + h))
    if radio:
        m = Image.new('L', (w, h), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radio, fill=255)
        im.putalpha(m)
    return im


def foto_circulo(nombre, d):
    im = foto(nombre, (d, d))
    m = Image.new('L', (d, d), 0)
    ImageDraw.Draw(m).ellipse((0, 0, d - 1, d - 1), fill=255)
    im.putalpha(m)
    return im


def sombra(lienzo, caja, radio, desp=(0, 22), difuso=36, alfa=70):
    x0, y0, x1, y1 = caja
    capa = Image.new('RGBA', lienzo.size, (0, 0, 0, 0))
    ImageDraw.Draw(capa).rounded_rectangle((x0 + desp[0], y0 + desp[1], x1 + desp[0], y1 + desp[1]), radio,
                                           fill=(27, 42, 74, alfa))
    capa = capa.filter(ImageFilter.GaussianBlur(difuso))
    lienzo.alpha_composite(capa)


def texto_ancho(d, s, f):
    return d.textlength(s, font=f)


def envolver(d, s, f, ancho):
    lineas, actual = [], ''
    for p in s.split():
        prueba = (actual + ' ' + p).strip()
        if texto_ancho(d, prueba, f) <= ancho:
            actual = prueba
        else:
            lineas.append(actual); actual = p
    if actual:
        lineas.append(actual)
    return lineas


def parrafo(d, xy, s, f, color, ancho, interlineado=1.25, centrado=False):
    x, y = xy
    for linea in envolver(d, s, f, ancho):
        lx = x - texto_ancho(d, linea, f) / 2 if centrado else x
        d.text((lx, y), linea, font=f, fill=color)
        y += int(f.size * interlineado)
    return y


def pastilla(d, xy, s, f, fondo, color, pad=(26, 14), centro=False):
    x, y = xy
    w = texto_ancho(d, s, f) + pad[0] * 2
    alto = f.size + pad[1] * 2
    if centro:
        x = x - w / 2
    d.rounded_rectangle((x, y, x + w, y + alto), alto / 2, fill=fondo)
    d.text((x + pad[0], y + pad[1] - f.size * 0.08), s, font=f, fill=color)
    return x + w, y + alto


def logo_sitioya(lienzo, xy, tam=64, oscuro=False):
    """Logo SitioYa dibujado (ventana + cursor) + texto SitioYa."""
    x, y = xy
    s = tam / 100
    capa = Image.new('RGBA', (tam, tam), (0, 0, 0, 0))
    g = ImageDraw.Draw(capa)
    g.rounded_rectangle((0, 0, tam - 1, tam - 1), 26 * s, fill=CORAL)
    g.rounded_rectangle((16 * s, 20 * s, 76 * s, 67 * s), 7 * s, fill=CREMA, outline=NAVY, width=max(2, int(6 * s)))
    g.line((16 * s, 33 * s, 76 * s, 33 * s), fill=NAVY, width=max(2, int(6 * s)))
    g.line((25 * s, 44.5 * s, 45 * s, 44.5 * s), fill=NAVY, width=max(2, int(6 * s)))
    g.line((25 * s, 56 * s, 37 * s, 56 * s), fill=NAVY, width=max(2, int(6 * s)))
    cursor = [(54, 46), (54, 84), (63.5, 74.5), (70, 88), (76.5, 85), (70, 71.5), (83.5, 71.5)]
    pts = [(a * s, b * s) for a, b in cursor]
    g.line(pts + [pts[0]], fill=CORAL, width=max(3, int(9 * s)), joint='curve')
    g.polygon(pts, fill=NAVY)
    lienzo.alpha_composite(capa, (int(x), int(y)))
    d = ImageDraw.Draw(lienzo)
    f = fuente(int(tam * 0.62), 900)
    tx = x + tam + tam * 0.22
    ty = y + tam / 2 - f.size * 0.62
    d.text((tx, ty), 'Sitio', font=f, fill=CREMA if oscuro else NAVY)
    d.text((tx + texto_ancho(d, 'Sitio', f) - f.size * 0.07, ty), 'Ya', font=f, fill=CORAL)
    return tx + texto_ancho(d, 'SitioYa', f)


def puntos_fondo(lienzo, color=(240, 223, 204, 255), paso=90, r=7, offset=0):
    d = ImageDraw.Draw(lienzo)
    for fy, y in enumerate(range(-paso, lienzo.height + paso, paso)):
        for x in range(-paso, lienzo.width + paso, paso):
            xx = x + (paso // 2 if fy % 2 else 0) + offset
            d.ellipse((xx - r, y - r, xx + r, y + r), fill=color)


# ---------- Pantalla de celular: la página de la heladería ----------

def logo_nieve(d, xy, tam):
    f = fuente(tam, 900, redonda=True)
    x, y = xy
    for parte, color in (('nieve', H_INK), ('&', H_ROSA), ('co', H_INK)):
        d.text((x, y), parte, font=f, fill=color)
        x += texto_ancho(d, parte, f)
    return x


def pantalla_portada(w, h):
    im = Image.new('RGBA', (w, h), H_BG)
    puntos_fondo(im, (246, 232, 226, 255), paso=56, r=5)
    d = ImageDraw.Draw(im)
    # barra
    d.rounded_rectangle((22, 84, w - 22, 172), 44, fill=BLANCO)
    logo_nieve(d, (52, 106), 40)
    fb = fuente(22, 800, redonda=True)
    pastilla(d, (w - 22 - 16 - texto_ancho(d, 'Pedir helado', fb) - 44, 104), 'Pedir helado', fb, H_ROSA, BLANCO,
             pad=(22, 13))
    # titular
    y = 214
    for linea in ('Helado', 'artesanal'):
        d.text((32, y), linea, font=fuente(74, 900, True), fill=H_INK); y += 78
    for linea in ('hecho cada', 'mañana'):
        d.text((32, y), linea, font=fuente(74, 900, True), fill=H_ROSA_D); y += 78
    y += 14
    y = parrafo(d, (32, y), 'Sabores con fruta de verdad, conos waffle recién hechos y potes para llevar. ¿Fiesta? Te llevamos el carrito.',
                fuente(27, 500), H_SOFT, w - 64, 1.4)
    y += 24
    f2 = fuente(26, 800, True)
    x1, _ = pastilla(d, (32, y), 'Pedir helado', f2, H_ROSA, BLANCO, pad=(30, 20))
    pastilla(d, (x1 + 18, y), 'Ver sabores', f2, H_AMARILLO, H_INK, pad=(30, 20))
    # foto en círculo
    dcir = w - 90
    cy = y + 110
    d.ellipse((45 - 10, cy - 10, 45 + dcir + 10, cy + dcir + 10), fill=BLANCO)
    im.alpha_composite(foto_circulo('1497034825429-c343d7c6a68f.jpg', dcir), (45, cy))
    d = ImageDraw.Draw(im)
    fs = fuente(24, 800, True)
    pastilla(d, (w / 2, cy - 30), '♥ Carrito para fiestas', fs, H_MENTA, H_INK, pad=(22, 13), centro=True)
    pastilla(d, (20, cy + 90), 'Fruta de verdad', fs, H_AMARILLO, H_INK, pad=(22, 13))
    pastilla(d, (w - 300, cy + dcir - 120), 'Delivery en potes', fs, '#FFD3E0', H_INK, pad=(22, 13))
    return im


SABORES = [
    ('1562790879-dfde82829db0.jpg', 'Chocolate belga', 'Cono o vaso', '$3.50', '#FFE3EC'),
    ('1782861162217-a69b974cacb6.jpg', 'Pistacho', 'Con trocitos', '$4', '#E3F5EE'),
    ('1629385701021-fcd568a743e8.jpg', 'Fresa con chispas', 'Para los niños', '$3.50', '#FFF1CC'),
    ('1774113351718-cdd37ec6b1e8.jpg', 'Mango maracuyá', 'Sorbete sin lácteos', '$3.50', '#FFE3DC'),
]


def pantalla_sabores(w, h):
    im = Image.new('RGBA', (w, h), H_LILA)
    d = ImageDraw.Draw(im)
    f = fuente(60, 900, True)
    t = 'Sabores favoritos'
    d.text(((w - texto_ancho(d, t, f)) / 2, 60), t, font=f, fill=BLANCO)
    cw = (w - 32 * 2 - 24) // 2
    chh = int(cw * 1.34)
    ih = int((cw - 24) * 0.72)
    for i, (img, nom, sub, precio, fondo) in enumerate(SABORES):
        col, fila = i % 2, i // 2
        x = 32 + col * (cw + 24)
        y = 170 + fila * (chh + 26)
        d.rounded_rectangle((x, y, x + cw, y + chh), 30, fill=fondo)
        im.alpha_composite(foto(img, (cw - 24, ih), 22), (x + 12, y + 12))
        d = ImageDraw.Draw(im)
        ty = y + ih + 26
        ty = parrafo(d, (x + 20, ty), nom, fuente(29, 900, True), H_INK, cw - 36, 1.1)
        d.text((x + 20, ty + 2), sub, font=fuente(21, 500), fill=H_SOFT)
        d.text((x + 20, y + chh - 62), precio, font=fuente(36, 900, True), fill=H_INK)
        fb = fuente(20, 800)
        bw = texto_ancho(d, 'Pedir', fb) + 36
        d.rounded_rectangle((x + cw - 20 - bw, y + chh - 62, x + cw - 20, y + chh - 22), 20, fill=H_INK)
        d.text((x + cw - 20 - bw + 18, y + chh - 57), 'Pedir', font=fb, fill=BLANCO)
    return im


def pantalla_pedido(w, h):
    im = Image.new('RGBA', (w, h), H_BG)
    d = ImageDraw.Draw(im)
    d.text((34, 100), 'Pide tu helado', font=fuente(60, 900, True), fill=H_INK)
    y = parrafo(d, (34, 178), 'Potes de 1 litro, conos para fiestas o el carrito para tu evento.', fuente(26, 500), H_SOFT,
                w - 68, 1.35)
    y += 20
    d.rounded_rectangle((22, y, w - 22, y + 610), 34, fill=BLANCO)
    fy = y + 28
    etiquetas = [('Nombre', 'Tu nombre'), ('Pedido', 'Pote de 1 litro  ▾'), ('Sabores', 'Mango, fresa…'), ('Día y hora', 'Sábado · 4:00 pm')]
    for et, val in etiquetas:
        d.text((50, fy), et, font=fuente(22, 800), fill=H_INK)
        d.rounded_rectangle((50, fy + 34, w - 50, fy + 34 + 74), 18, fill='#FBF3EE', outline='#EADBD5', width=2)
        d.text((72, fy + 54), val, font=fuente(25, 500), fill=H_SOFT)
        fy += 120
    fb = fuente(28, 900, True)
    t = 'Enviar pedido'
    d.rounded_rectangle((50, fy + 4, w - 50, fy + 84), 40, fill=H_ROSA)
    d.text(((w - texto_ancho(d, t, fb)) / 2, fy + 25), t, font=fb, fill=BLANCO)
    y = y + 632
    # horario y ubicación, lado a lado
    cw = (w - 44 - 16) // 2
    for i, (titulo, linea1, linea2) in enumerate((('Horario', 'Todos los días', '11 am – 10 pm'), ('Dónde estamos', 'Bella Vista,', 'Ciudad de Panamá'))):
        x = 22 + i * (cw + 16)
        d.rounded_rectangle((x, y, x + cw, y + 160), 30, fill=BLANCO)
        d.text((x + 24, y + 22), titulo, font=fuente(28, 900, True), fill=H_INK)
        d.text((x + 24, y + 70), linea1, font=fuente(22, 500), fill=H_SOFT)
        d.text((x + 24, y + 104), linea2, font=fuente(22, 700), fill=H_INK)
    return im


def celular(lienzo, xy, pantalla, ancho=520, alto=None, girar=0):
    """Mete una pantalla (diseñada a 600 px de ancho) dentro de un marco de celular."""
    alto = alto or int(ancho * 2.05)
    marco = 18
    W, H = ancho, alto
    tel = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(tel)
    g.rounded_rectangle((0, 0, W - 1, H - 1), 70, fill=NAVY)
    sw, sh = W - marco * 2, H - marco * 2
    r = sw / pantalla.width
    pant = pantalla.resize((sw, int(pantalla.height * r)), Image.LANCZOS).crop((0, 0, sw, sh))
    m = Image.new('L', (sw, sh), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, sw - 1, sh - 1), 54, fill=255)
    tel.paste(pant, (marco, marco), m)
    g.rounded_rectangle((W / 2 - 62, marco + 14, W / 2 + 62, marco + 46), 16, fill=NAVY)
    if girar:
        tel = tel.rotate(girar, resample=Image.BICUBIC, expand=True)
    x, y = xy
    sombra(lienzo, (x + 20, y + 30, x + tel.width - 20, y + tel.height - 10), 70, desp=(0, 30), difuso=40, alfa=80)
    lienzo.alpha_composite(tel, (int(x), int(y)))


def laptop(lienzo, xy, pantalla, ancho=760):
    x, y = xy
    sw = ancho - 40
    sh = int(sw * 0.625)
    sombra(lienzo, (x, y, x + ancho, y + sh + 60), 30, desp=(0, 30), difuso=40, alfa=70)
    d = ImageDraw.Draw(lienzo)
    d.rounded_rectangle((x, y, x + ancho, y + sh + 40), 28, fill=NAVY)
    r = sw / pantalla.width
    pant = pantalla.resize((sw, int(pantalla.height * r)), Image.LANCZOS).crop((0, 0, sw, sh))
    lienzo.alpha_composite(pant, (x + 20, y + 20))
    d = ImageDraw.Draw(lienzo)
    d.rounded_rectangle((x - 60, y + sh + 40, x + ancho + 60, y + sh + 72), 16, fill='#2C3D63')
    d.rounded_rectangle((x + ancho / 2 - 80, y + sh + 40, x + ancho / 2 + 80, y + sh + 52), 6, fill='#22314F')


def pantalla_escritorio(w=1200, h=750):
    im = Image.new('RGBA', (w, h), H_BG)
    puntos_fondo(im, (246, 232, 226, 255), paso=60, r=5)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 28, w - 60, 108), 40, fill=BLANCO)
    logo_nieve(d, (96, 46), 38)
    fn = fuente(22, 700)
    x = 530
    for t in ('Sabores', 'Pedido', 'Fotos', 'Ubicación'):
        d.text((x, 55), t, font=fn, fill=H_INK); x += texto_ancho(d, t, fn) + 26
    pastilla(d, (x + 6, 44), 'Pedir helado', fuente(22, 800, True), H_ROSA, BLANCO, pad=(24, 12))
    y = 180
    for linea, c in (('Helado', H_INK), ('artesanal', H_INK), ('hecho cada', H_ROSA_D), ('mañana', H_ROSA_D)):
        d.text((90, y), linea, font=fuente(80, 900, True), fill=c); y += 84
    y = parrafo(d, (90, y + 16), 'Sabores con fruta de verdad, conos waffle recién hechos y potes para llevar.', fuente(26, 500), H_SOFT, 520, 1.4)
    f2 = fuente(24, 800, True)
    x1, _ = pastilla(d, (90, y + 22), 'Pedir helado', f2, H_ROSA, BLANCO, pad=(28, 18))
    pastilla(d, (x1 + 16, y + 22), 'Ver sabores', f2, H_AMARILLO, H_INK, pad=(28, 18))
    dc = 470
    d.ellipse((680 - 10, 150 - 10, 680 + dc + 10, 150 + dc + 10), fill=BLANCO)
    im.alpha_composite(foto_circulo('1497034825429-c343d7c6a68f.jpg', dc), (680, 150))
    d = ImageDraw.Draw(im)
    pastilla(d, (640, 250), 'Fruta de verdad', fuente(22, 800, True), H_AMARILLO, H_INK, pad=(20, 12))
    pastilla(d, (860, 130), '♥ Carrito para fiestas', fuente(22, 800, True), H_MENTA, H_INK, pad=(20, 12))
    return im


# ---------- Piezas comunes de los slides ----------

def base(w, h, fondo=CREMA):
    im = Image.new('RGBA', (w, h), fondo)
    return im


def pie(im, n, total=4, oscuro=False):
    d = ImageDraw.Draw(im)
    W, H = im.size
    logo_sitioya(im, (70, H - 120), 58, oscuro)
    d = ImageDraw.Draw(im)
    f = fuente(28, 700)
    t = '@sitioya.pty'
    d.text((W - 70 - texto_ancho(d, t, f), H - 106), t, font=f, fill=CREMA if oscuro else SOFT)
    # puntitos de página
    x = W / 2 - (total * 26) / 2
    for i in range(total):
        c = CORAL if i == n - 1 else ('#3A4A6C' if oscuro else LINEA)
        d.ellipse((x + i * 26, H - 98, x + i * 26 + 14, H - 84), fill=c)


def kicker(d, xy, s, oscuro=False):
    f = fuente(28, 800)
    x, y = xy
    d.ellipse((x, y + 12, x + 16, y + 28), fill=CORAL)
    d.text((x + 30, y), s, font=f, fill=CORAL if oscuro else CORAL_D)


def slide1():
    im = base(1080, 1350)
    d = ImageDraw.Draw(im)
    d.ellipse((560, 460, 1280, 1180), fill=BLUSH)
    d.ellipse((-160, 1010, 220, 1390), fill='#DDF4EC')
    pastilla(d, (70, 80), 'EJEMPLO DE LA SEMANA', fuente(30, 900), CORAL, NAVY, pad=(30, 16))
    d.text((66, 170), 'Heladería', font=fuente(150, 900), fill=NAVY)
    parrafo(d, (72, 348), 'Así podría quedar la página de tu negocio.', fuente(46, 700), SOFT, 900, 1.25)
    y = 560
    for t in ('Sabores con foto', 'Pedidos en un toque', 'Horario y ubicación'):
        d.rounded_rectangle((72, y, 92, y + 20), 6, fill=MENTA)
        d.text((112, y - 14), t, font=fuente(36, 700), fill=NAVY)
        y += 70
    d.text((72, 820), 'Desliza →', font=fuente(36, 800), fill=CORAL_D)
    celular(im, (590, 470), pantalla_portada(600, 1240), ancho=400, alto=690, girar=-4)
    d = ImageDraw.Draw(im)
    d.text((72, 1150), 'Negocio y datos de ejemplo', font=fuente(24, 500), fill=SOFT)
    pie(im, 1)
    return im


def slide2():
    im = base(1080, 1350)
    d = ImageDraw.Draw(im)
    d.ellipse((-260, 420, 520, 1200), fill=BLUSH)
    kicker(d, (70, 80), 'Ejemplo de la semana · Heladería')
    d.text((66, 140), 'Sabores con foto', font=fuente(86, 900), fill=NAVY)
    d.text((66, 236), 'y precio a la vista', font=fuente(86, 900), fill=CORAL)
    parrafo(d, (72, 360), 'Tus clientes ven qué hay y cuánto cuesta sin tener que preguntar por mensaje.',
            fuente(36, 500), SOFT, 900, 1.35)
    d.text((72, 466), 'Precios de ejemplo', font=fuente(24, 500), fill=SOFT)
    celular(im, (300, 520), pantalla_sabores(600, 1300), ancho=480, alto=680)
    pie(im, 2)
    return im


def slide3():
    im = base(1080, 1350)
    d = ImageDraw.Draw(im)
    d.ellipse((620, 380, 1340, 1100), fill='#DDF4EC')
    kicker(d, (70, 80), 'Ejemplo de la semana · Heladería')
    d.text((66, 140), 'Pedidos y', font=fuente(86, 900), fill=NAVY)
    d.text((66, 236), 'ubicación claros', font=fuente(86, 900), fill=CORAL)
    y = 380
    for t, s in (('Formulario de pedido', 'Potes, conos para fiestas o el carrito para eventos.'),
                 ('Horario a mano', 'Nadie tiene que preguntar a qué hora abres.'),
                 ('Dónde estamos', 'Tu zona siempre a la vista para que lleguen.')):
        d.rounded_rectangle((72, y + 10, 96, y + 34), 7, fill=CORAL)
        d.text((118, y), t, font=fuente(36, 800), fill=NAVY)
        y = parrafo(d, (118, y + 48), s, fuente(28, 500), SOFT, 380, 1.3) + 34
    celular(im, (560, 380), pantalla_pedido(600, 1300), ancho=460, alto=840, girar=3)
    d = ImageDraw.Draw(im)
    d.text((72, 1150), 'Horario y ubicación de ejemplo', font=fuente(24, 500), fill=SOFT)
    pie(im, 3)
    return im


def slide4():
    im = base(1080, 1350, NAVY)
    d = ImageDraw.Draw(im)
    puntos_fondo(im, (36, 54, 90, 255), paso=80, r=5)
    d = ImageDraw.Draw(im)
    laptop(im, (160, 120), pantalla_escritorio(), ancho=760)
    d = ImageDraw.Draw(im)
    y = 690
    for linea, c in (('Así podría quedar', CREMA), ('la página de', CREMA), ('tu negocio', CORAL)):
        t = linea
        f = fuente(84, 900)
        d.text(((1080 - texto_ancho(d, t, f)) / 2, y), t, font=f, fill=c); y += 92
    y += 30
    parrafo(d, (540, y), 'Con tus fotos, tus productos y tu estilo.', fuente(34, 500), '#C9D1E3', 820, 1.3, centrado=True)
    f = fuente(42, 900)
    t1, t2, t3 = 'Comenta ', 'PÁGINA', ' y te contamos'
    ancho_total = texto_ancho(d, t1 + t2 + t3, f) + 80
    x = (1080 - ancho_total) / 2
    by = y + 90
    d.rounded_rectangle((x, by, x + ancho_total, by + 96), 48, fill=CORAL)
    tx = x + 40
    for parte in (t1, t2, t3):
        d.text((tx, by + 22), parte, font=f, fill=NAVY)
        if parte == t2:  # subrayado para resaltar la palabra que hay que comentar
            d.rounded_rectangle((tx, by + 76, tx + texto_ancho(d, parte, f), by + 82), 3, fill=NAVY)
        tx += texto_ancho(d, parte, f)
    pie(im, 4, oscuro=True)
    return im


def caja_punteada(d, caja, radio, color, guion=22, hueco=16, ancho=4):
    x0, y0, x1, y1 = caja
    # lados rectos punteados (las esquinas se dibujan como arcos)
    def linea(a, b, horizontal):
        pos = a
        while pos < b:
            fin = min(pos + guion, b)
            if horizontal is not None:
                yield pos, fin
            pos = fin + hueco
    for a, b in linea(x0 + radio, x1 - radio, True):
        d.line((a, y0, b, y0), fill=color, width=ancho); d.line((a, y1, b, y1), fill=color, width=ancho)
    for a, b in linea(y0 + radio, y1 - radio, True):
        d.line((x0, a, x0, b), fill=color, width=ancho); d.line((x1, a, x1, b), fill=color, width=ancho)
    for (cx, cy, ini) in ((x0, y0, 180), (x1 - 2 * radio, y0, 270), (x1 - 2 * radio, y1 - 2 * radio, 0), (x0, y1 - 2 * radio, 90)):
        d.arc((cx, cy, cx + 2 * radio, cy + 2 * radio), ini, ini + 90, fill=color, width=ancho)


def story():
    im = base(1080, 1920)
    d = ImageDraw.Draw(im)
    d.ellipse((620, -220, 1380, 540), fill=BLUSH)
    d.ellipse((-300, 1500, 420, 2220), fill='#DDF4EC')
    logo_sitioya(im, (80, 250), 76)
    d = ImageDraw.Draw(im)
    y = 420
    f = fuente(112, 900)
    for linea, c in (('¿Tu negocio', NAVY), ('tiene página', NAVY), ('web?', CORAL)):
        d.text((76, y), linea, font=f, fill=c); y += 122
    # espacio para el sticker de encuesta (Sí / No)
    caja_punteada(d, (110, 860, 970, 1180), 44, '#E9CDB4')
    # texto de abajo
    y = 1250
    y = parrafo(d, (80, y), 'Hacemos páginas web para negocios en Panamá.', fuente(52, 800), NAVY, 920, 1.2)
    y = parrafo(d, (80, y + 18), 'Síguenos en @sitioya.pty y mira ejemplos', fuente(40, 500), SOFT, 920, 1.3)
    # espacio para el sticker de mención
    caja_punteada(d, (300, y + 40, 780, y + 170), 40, '#E9CDB4')
    return im


def main():
    piezas = {
        'heladeria-1-portada.png': slide1(),
        'heladeria-2-sabores.png': slide2(),
        'heladeria-3-pedidos.png': slide3(),
        'heladeria-4-cierre.png': slide4(),
        'story-encuesta.png': story(),
    }
    for nombre, im in piezas.items():
        im.convert('RGB').save(os.path.join(SALIDA, nombre), optimize=True)
        print(nombre, im.size)


if __name__ == '__main__':
    main()
