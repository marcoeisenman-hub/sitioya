# Posts del feed de @sitioya.pty

Salen de `tools/redes_posts.py` (correr `python3 tools/redes_posts.py`): hace las imágenes y la galería `index.html` con los captions. Mismo estilo, letras y medidas (1080x1350) que el carrusel de `redes/ejemplo-heladeria/` (necesita Pillow y una Mac).

Se ven y se bajan en https://sitioya.vercel.app/redes/posts/

## Orden sugerido para publicar (feed completo, 13 posts + 1 story)
El número es el orden: se publica del 1 al 13. Los 10, 11 y 12 son extra y van después del 9. El 13 (Síguenos: Tu negocio merece una página web) es el más nuevo y va después del 12, así queda arriba en el perfil. Si los 1-12 ya salieron, toca publicar el 13.

1. `1-tu-negocio-en-internet.png` · Tu negocio en internet, ya
   > Tu negocio en internet, ya. Hacemos páginas web para negocios en Panamá, listas en pocos días. ¿Tu negocio ya tiene página? Sí o no, te leemos en los comentarios

2. `2-como-funciona.png` · ¿Cómo funciona?
   > ¿Cómo funciona? 1. Escríbenos 2. Te armamos un ejemplo de tu página 3. Lista en pocos días y compartes tu link. Escríbenos por WhatsApp al 6919-7559 y empezamos

3. `3-paginas-de-ejemplo.png` · 4 páginas de ejemplo (Panadería, Barbería, Tienda, Repostería)
   > 4 páginas de ejemplo: panadería, barbería, tienda y repostería. ¿Cuál estilo va con tu negocio? Dinos en los comentarios

4. Carrusel `redes/ejemplo-heladeria/` (4 slides: `heladeria-1-portada.png`, `heladeria-2-sabores.png`, `heladeria-3-pedidos.png`, `heladeria-4-cierre.png`) · Ejemplo de la semana: Heladería
   > Ejemplo de la semana: Heladería. Así podría quedar la página de tu negocio. Compártelo con alguien que tenga negocio

5. `5-tres-cosas-que-tu-pagina-debe-tener.png` · 3 cosas que tu página debe tener
   > 3 cosas que tu página debe tener: tus productos con foto, un botón para escribirte y tu horario y cómo llegar. ¿La tuya las tiene? Guárdalo para cuando armes la tuya

6. `6-antes-y-despues.png` · Antes y después
   > Antes: te buscan y no te encuentran. Después: tu página con tus precios, tu horario y tu link para compartir. ¿Quieres pasar al después? Escríbenos por WhatsApp al 6919-7559

7. `7-vendes-por-instagram.png` · ¿Vendes por Instagram? Así se vería tu negocio con página (vender solo por mensajes vs con página; abajo en chico "Hacemos páginas para negocios en Panamá. @sitioya.pty")
   > ¿Vendes solo por Instagram? Con una página tus clientes ven todo en un solo lugar y te piden directo. Compártelo con alguien que venda por mensajes

8. `8-precios.png` · Precios
   > Precios claros: Básica $99, Completa $199 y Diseño único desde $369. Pagas una sola vez y el mantenimiento de $15/mes es opcional. Comenta PÁGINA y te contamos

9. `9-siguenos.png` · Síguenos para más
   > Síguenos para ver páginas de ejemplo, precios claros y tips para tu negocio. Hacemos páginas web para negocios en Panamá

10. `10-tres-cosas-que-pierde-tu-negocio.png` · 3 cosas que pierde tu negocio sin página
   > 3 cosas que pierde tu negocio sin página: clientes que te buscan, tiempo contestando lo mismo y pedidos cuando estás ocupado. Guárdalo para cuando lo necesites

11. `11-pagina-y-no-solo-instagram.png` · Por qué página y no solo Instagram
   > Instagram para que te conozcan y tu página para que te compren: tus productos ordenados, tus precios y tu horario a la vista y todo siempre en el mismo lugar. ¿Tu negocio ya tiene página o solo redes? Cuéntanos en los comentarios

12. `12-ejemplo-gratis-de-tu-pagina.png` · Te armamos un ejemplo gratis de tu página
   > Te armamos un ejemplo gratis de tu página para que veas cómo quedaría tu negocio antes de decidir. Comenta PÁGINA y te contamos

13. `13-siguenos-tu-negocio-merece-pagina.png` · Síguenos: Tu negocio merece una página web (celulares con la Heladería del carrusel y el menú de Mesa Lunar)
   > Hacemos páginas web para negocios en Panamá. Síguenos para ver más ejemplos y tips para tu negocio

Story (1080x1920): `redes/ejemplo-heladeria/story-encuesta.png` · ¿Tu negocio tiene página web? Se puede subir el mismo día que el 10. En el recuadro de arriba va el sticker de encuesta con "¿Tu negocio tiene página web?" y las opciones Sí / No (o, en otra story con el mismo arte, la cajita de preguntas: "Si no tiene, ¿qué te frena? Pregúntanos"); en el de abajo, el sticker de mención @sitioya.pty. Ya trae el texto "Hacemos páginas web para negocios en Panamá. Síguenos en @sitioya.pty y mira ejemplos" (sale de `tools/redes_heladeria.py`).

Los videos los hace Cam (ver `redes/VIDEOS.md`). Los nombres viejos `4-precios.png` y `5-siguenos.png` redirigen a los nuevos (`vercel.json`).

## Qué se cuidó
- Llamados a la acción variados: "Comenta PÁGINA" solo en los de venta (8 Precios y 12 Ejemplo gratis). Los demás usan preguntas para opinar, "Guárdalo", "Compártelo con alguien que tenga negocio" o "Escríbenos por WhatsApp al 6919-7559". Las imágenes 2, 5, 10, 12 y la slide 4 de la Heladería todavía traen el botón "Comenta PÁGINA" dibujado.
- No dicen la palabra de antes en ningún lado: se habla de páginas y de ejemplos.
- Precios: solo los de la web (Básica $99, Completa $199, Diseño único desde $369, mantenimiento opcional $15/mes). El post 7 no muestra precios.
- Sin logos ni marcas de terceros: a las capturas se les cortó el botón flotante de abajo; el perfil del post 7 es genérico (sin logo de ninguna red, sin @ ni cifras de seguidores) y el botón "Pedir por WhatsApp" es solo texto. "WhatsApp" e "Instagram" solo aparecen como texto.
- Los negocios (Luna, Norte Barber, brisa., Dulce Nube, Nieve & Co, Mesa Lunar) son ficticios, igual que sus datos, y cada post con capturas lo dice ("Negocios y datos de ejemplo"). Sin reseñas ni cifras inventadas.
