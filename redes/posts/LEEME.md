# Posts del feed de @sitioya.pty

Salen de `tools/redes_posts.py` (correr `python3 tools/redes_posts.py`): hace las imágenes y la galería `index.html` con los captions. Mismo estilo, letras y medidas (1080x1350) que el carrusel de `redes/ejemplo-heladeria/` (necesita Pillow y una Mac).

Se ven y se bajan en https://sitioya.vercel.app/redes/posts/

## Orden sugerido para publicar (feed completo, 9 posts)
El número es el orden: se publica del 1 al 9. Así el último (Síguenos para más) queda arriba en el perfil y el de Precios justo debajo.

1. `1-tu-negocio-en-internet.png` · Tu negocio en internet, ya
   > Tu negocio en internet, ya. Hacemos páginas web para negocios en Panamá, listas en pocos días. Comenta PÁGINA y te contamos

2. `2-como-funciona.png` · ¿Cómo funciona?
   > ¿Cómo funciona? 1. Escríbenos 2. Te armamos un ejemplo de tu página 3. Lista en pocos días y compartes tu link. Comenta PÁGINA y te contamos

3. `3-paginas-de-ejemplo.png` · 4 páginas de ejemplo (Panadería, Barbería, Tienda, Repostería)
   > 4 páginas de ejemplo: panadería, barbería, tienda y repostería. ¿Cuál estilo va con tu negocio? Comenta PÁGINA y te contamos

4. Carrusel `redes/ejemplo-heladeria/` (4 slides: `heladeria-1-portada.png`, `heladeria-2-sabores.png`, `heladeria-3-pedidos.png`, `heladeria-4-cierre.png`) · Ejemplo de la semana: Heladería
   > Ejemplo de la semana: Heladería. Así podría quedar la página de tu negocio. Comenta PÁGINA y te contamos

5. `5-tres-cosas-que-tu-pagina-debe-tener.png` · 3 cosas que tu página debe tener
   > 3 cosas que tu página debe tener: tus productos con foto, un botón para escribirte y tu horario y cómo llegar. ¿La tuya las tiene? Comenta PÁGINA y te contamos

6. `6-antes-y-despues.png` · Antes y después
   > Antes: te buscan y no te encuentran. Después: tu página con tus precios, tu horario y tu link para compartir. Comenta PÁGINA y te contamos

7. `7-vendes-por-instagram.png` · ¿Vendes por Instagram? (vender solo por mensajes vs con página)
   > ¿Vendes solo por Instagram? Con una página tus clientes ven todo en un solo lugar y te piden directo. Comenta PÁGINA y te contamos

8. `8-precios.png` · Precios
   > Precios claros: Básica $99, Completa $199 y Diseño único desde $369. Pagas una sola vez y el mantenimiento de $15/mes es opcional. Comenta PÁGINA y te contamos

9. `9-siguenos.png` · Síguenos para más
   > Síguenos para ver páginas de ejemplo, precios claros y tips para tu negocio. Hacemos páginas web para negocios en Panamá

Los videos los hace Cam (ver `redes/VIDEOS.md`). Los nombres viejos `4-precios.png` y `5-siguenos.png` redirigen a los nuevos (`vercel.json`).

## Qué se cuidó
- No dicen la palabra de antes en ningún lado: se habla de páginas y de ejemplos.
- Precios: solo los de la web (Básica $99, Completa $199, Diseño único desde $369, mantenimiento opcional $15/mes). El post 7 no muestra precios.
- Sin logos ni marcas de terceros: a las capturas se les cortó el botón flotante de abajo; el perfil del post 7 es genérico (sin logo de ninguna red, sin @ ni cifras de seguidores) y el botón "Pedir por WhatsApp" es solo texto. "WhatsApp" e "Instagram" solo aparecen como texto.
- Los negocios (Luna, Norte Barber, brisa., Dulce Nube, Nieve & Co) son ficticios, igual que sus datos, y cada post con capturas lo dice ("Negocios y datos de ejemplo"). Sin reseñas ni cifras inventadas.
