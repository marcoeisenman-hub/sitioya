# Genera biblioteca.html con las plantillas de index.html (correr después de agregar plantillas)
import re, json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "index.html").read_text()
arr = re.search(r"const T = (\[.*?\n\]);", src, re.S).group(1)
js = re.sub(r'(\{|,)\s*([a-z]+):', r'\1"\2":', arr)
T = json.loads(js)
tpl = (root / "tools" / "biblioteca.tpl.html").read_text()
(root / "biblioteca.html").write_text(tpl.replace("/*DATA*/[]", json.dumps(T, ensure_ascii=False)))
print(len(T), "plantillas")
