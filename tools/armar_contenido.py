"""Arma el paquete de contenido de la semana de @sitioya.pty, listo para subir a Drive.

Uso: python3 tools/armar_contenido.py
Crea contenido/<fecha>/ (una carpeta por día de publicación) con la imagen o el video final
y al lado un .txt con el caption listo para copiar (o, en las stories, qué sticker va).
Las imágenes y videos se copian de redes/ (no se rehacen). contenido/ no va a Git ni a Vercel.

Plan semanal: lun post 3 cosas que pierde tu negocio sin página · mar video antes/después ·
mié post ejemplo de la semana + story encuesta · jue video cómo funciona · vie post giveaway ·
sáb y dom stories. El giveaway del viernes queda pendiente (falta definir el premio y las reglas):
el viernes 27 va el reel nuevo "A la medida" (Síguenos) con el post de Síguenos.
"""
import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "contenido"
H = "#Panamá #EmprendedoresPanamá #NegociosPanamá #PáginaWeb #SitioYa"


def cap(texto):
    return f"{texto}\n\n{H}\n"


STORY_MENCION = "Story. Agrega el sticker de mención @sitioya.pty."

PLAN = [
    ("2026-11-27", "viernes", [
        ("reel", "redes/videos/a-la-medida.mp4", cap(
            "¿Tu negocio todavía no tiene página web? Te la hacemos a la medida: Básica $99 o Completa $199. "
            "Antes de decidir, te armamos un ejemplo gratis para que veas cómo quedaría tu negocio. "
            "Escríbenos al WhatsApp 6919-7559 y síguenos para ver más ejemplos")),
        ("reel-portada", "redes/videos/a-la-medida.jpg", "Portada del reel a-la-medida.mp4 (súbela como portada al publicar el reel).\n"),
        ("post", "redes/posts/9-siguenos-tu-negocio-merece-pagina.png", cap(
            "Hacemos páginas web para negocios en Panamá. Síguenos para ver más ejemplos y tips para tu negocio")),
    ]),
    ("2026-11-28", "sábado", [
        ("story", "redes/promo/sitioya-promo-story.png", f"{STORY_MENCION}\nOpcional: sticker de enlace a https://sitioya.vercel.app\n"),
        ("story-video", "redes/videos/planes.mp4", f"{STORY_MENCION}\nTexto opcional encima: Básica $99 o Completa $199. Escríbenos al 6919-7559\n"),
    ]),
    ("2026-11-29", "domingo", [
        ("story-video", "redes/videos/tu-negocio-en-internet.mp4", f"{STORY_MENCION}\nSticker de preguntas: ¿Qué negocio tienes? Te decimos cómo quedaría tu página\n"),
        ("story", "redes/posts/12-ejemplo-gratis-de-tu-pagina.png", f"{STORY_MENCION}\nTexto opcional encima: Pídelo por DM o al 6919-7559\n"),
    ]),
    ("2026-11-30", "lunes", [
        ("post", "redes/posts/10-tres-cosas-que-pierde-tu-negocio.png", cap(
            "3 cosas que pierde tu negocio sin página: clientes que te buscan, tiempo contestando lo mismo y pedidos cuando estás ocupado. Guárdalo para cuando lo necesites")),
        ("post", "redes/posts/11-pagina-y-no-solo-instagram.png", cap(
            "Instagram para que te conozcan y tu página para que te compren: tus productos ordenados, tus precios y tu horario a la vista y todo siempre en el mismo lugar. ¿Tu negocio ya tiene página o solo redes? Cuéntanos en los comentarios")),
    ]),
    ("2026-12-01", "martes", [
        ("reel", "redes/videos/antes-despues.mp4", cap(
            "¿Sigues vendiendo solo por DM? Con tu página, tus precios, tu horario y cómo llegar ya están a la vista, y te escriben directo para pedir. Escríbenos por WhatsApp al 6919-7559")),
        ("reel-portada", "redes/videos/antes-despues.jpg", "Portada del reel antes-despues.mp4.\n"),
        ("post", "redes/posts/6-antes-y-despues.png", cap(
            "Antes: te buscan y no te encuentran. Después: tu página con tus precios, tu horario y tu link para compartir. ¿Quieres pasar al después? Escríbenos por WhatsApp al 6919-7559")),
    ]),
    ("2026-12-02", "miércoles", [
        ("carrusel-1", "redes/ejemplo-heladeria/heladeria-1-portada.png", None),
        ("carrusel-2", "redes/ejemplo-heladeria/heladeria-2-sabores.png", None),
        ("carrusel-3", "redes/ejemplo-heladeria/heladeria-3-pedidos.png", None),
        ("carrusel-4", "redes/ejemplo-heladeria/heladeria-4-cierre.png", cap(
            "Ejemplo de la semana: Heladería. Así podría quedar la página de tu negocio. Compártelo con alguien que tenga negocio")),
        ("story", "redes/ejemplo-heladeria/story-encuesta.png",
         "Story. En el recuadro grande va el sticker de encuesta: ¿Tu negocio tiene página web? con Sí / No.\n"
         "En el recuadro chico de abajo va el sticker de mención @sitioya.pty.\n"),
    ]),
    ("2026-12-03", "jueves", [
        ("reel", "redes/videos/como-funciona.mp4", cap(
            "Tu página web en 3 pasos: 1. Escríbenos 2. Te armamos un ejemplo de tu página 3. Lista en pocos días y compartes tu link. Escríbenos por WhatsApp al 6919-7559")),
        ("reel-portada", "redes/videos/como-funciona.jpg", "Portada del reel como-funciona.mp4.\n"),
        ("post", "redes/posts/2-como-funciona.png", cap(
            "¿Cómo funciona? 1. Escríbenos 2. Te armamos un ejemplo de tu página 3. Lista en pocos días y compartes tu link. Escríbenos por WhatsApp al 6919-7559 y empezamos")),
    ]),
]


def main():
    resumen = ["Contenido de @sitioya.pty, una carpeta por día de publicación.",
               "En cada carpeta: el archivo final y al lado un .txt con el caption listo para copiar.",
               "El carrusel del miércoles lleva su caption en el .txt de la slide 4.",
               "Pendiente: el post giveaway de los viernes (falta definir premio y reglas).", ""]
    for fecha, dia, items in PLAN:
        d = SALIDA / fecha
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
        resumen.append(f"{fecha} ({dia})")
        for i, (tipo, src, txt) in enumerate(items, 1):
            s = RAIZ / src
            if not s.is_file():
                raise SystemExit(f"Falta {src}")
            base = f"{i:02d}-{tipo}-{s.stem}"
            shutil.copy2(s, d / f"{base}{s.suffix}")
            if txt:
                (d / f"{base}.txt").write_text(txt, encoding="utf-8")
            resumen.append(f"  {base}{s.suffix}")
        resumen.append("")
    (SALIDA / "LEEME.txt").write_text("\n".join(resumen), encoding="utf-8")
    print("listo:", SALIDA)


if __name__ == "__main__":
    main()
