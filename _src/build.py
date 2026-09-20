#!/usr/bin/env python3
"""
Vestígio Oculto — build estático.

Injeta nos templates .tpl.html:
  {{CSS}}   → _src/vestigio.css
  {{LOGO}}  → _src/marca/logo-horizontal-escuro-solido.svg (em curvas)

e grava as páginas finais, autocontidas, na raiz do site. Também copia o
símbolo da marca como favicon.svg.

Uso:  python3 _src/build.py       (a partir da raiz do projeto)

Cada página gerada é um único arquivo HTML sem dependências locais — basta
enviar a raiz do projeto para o servidor. O CSS vive num lugar só: edite
_src/vestigio.css e rode o build de novo.
"""

import re
import shutil
from pathlib import Path

# ---------------------------------------------------------------
# TROQUE AQUI quando o domínio estiver definido. É o único lugar:
# canonical, og:url, og:image e JSON-LD saem todos daqui.
DOMINIO = "https://vestigiooculto.com.br"
# ---------------------------------------------------------------

RAIZ = Path(__file__).resolve().parent.parent
SRC = RAIZ / "_src"

CSS = (SRC / "vestigio.css").read_text(encoding="utf-8")

# A marca vai inline: nenhuma requisição extra e nada quebra se o caminho
# mudar. Abaixo de 200 px a identidade pede a versão SÓLIDA, sem tweed.
LOGO = (SRC / "marca" / "logo-horizontal-escuro-solido.svg").read_text(encoding="utf-8")
LOGO = re.sub(r'\s(width|height)="[^"]*"', "", LOGO, count=2)  # o tamanho é do CSS
LOGO = LOGO.replace("<svg ", '<svg role="img" aria-hidden="true" focusable="false" ', 1)

FAVICON = SRC / "marca" / "simbolo-escuro-solido.svg"

# Visor de fólios do dossiê 008. Fica num arquivo à parte porque é um bloco
# grande e independente do texto.
VISOR = (SRC / "visor-voynich.html").read_text(encoding="utf-8")

# template  ->  caminho final, relativo à raiz do site
PAGINAS = {
    "index.tpl.html": "index.html",
    "gobekli-tepe.tpl.html": "dossies/gobekli-tepe.html",
    "amazonia-lidar.tpl.html": "dossies/amazonia-lidar.html",
    "manuscrito-voynich.tpl.html": "dossies/manuscrito-voynich.html",
    "denisovanos.tpl.html": "dossies/denisovanos.html",
    "sentinela-do-norte.tpl.html": "dossies/sentinela-do-norte.html",
    "grande-piramide.tpl.html": "dossies/grande-piramide.html",
}


def main() -> None:
    for template, destino in PAGINAS.items():
        origem = SRC / template
        if not origem.exists():
            print(f"  ! template ausente: {template}")
            continue

        html = origem.read_text(encoding="utf-8")
        faltando = [m for m in ("{{CSS}}", "{{LOGO}}") if m not in html]
        if faltando:
            print(f"  ! {template}: marcador ausente {', '.join(faltando)}")
            continue

        saida = RAIZ / destino
        saida.parent.mkdir(parents=True, exist_ok=True)
        saida.write_text(
            html.replace("{{CSS}}", CSS)
                .replace("{{LOGO}}", LOGO)
                .replace("{{DOMINIO}}", DOMINIO.rstrip("/"))
                .replace("{{VISOR}}", VISOR),
            encoding="utf-8",
        )
        print(f"  ✓ {destino}  ({saida.stat().st_size / 1024:.1f} KB)")

    if FAVICON.exists():
        shutil.copyfile(FAVICON, RAIZ / "favicon.svg")
        print("  ✓ favicon.svg")


if __name__ == "__main__":
    print("Vestígio Oculto — gerando páginas")
    main()
    print("pronto.")
