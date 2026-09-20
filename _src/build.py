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

# AdSense. ADSENSE_LIGADO = False tira o script de TODAS as páginas e
# apaga o ads.txt — é o interruptor geral, uma linha só.
ADSENSE_LIGADO = True
ADSENSE_PUB = "pub-4401770243539507"

# Consentimento. False = a faixa avisa e o anúncio carrega de imediato; quem
# recusar deixa de receber. True = nada de anúncio até a pessoa clicar em
# "Entendi" — mais conservador com a LGPD, e menos receita.
CONSENTIMENTO_BLOQUEIA = False
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

# O bloco do AdSense é montado a partir do ID acima, para o número não
# aparecer escrito à mão em sete arquivos diferentes. O preconnect adianta
# o handshake com o servidor de anúncios; o script é async e não bloqueia
# a renderização.
# O <head> leva só a meta de verificação e o preconnect. O SCRIPT em si é
# injetado pelo bloco de consentimento, depois que ele decide se pode.
if ADSENSE_LIGADO:
    ADSENSE = (
        f'<meta name="google-adsense-account" content="ca-{ADSENSE_PUB}">\n'
        '<link rel="preconnect" href="https://pagead2.googlesyndication.com" crossorigin>'
    )
else:
    ADSENSE = "<!-- AdSense desligado em _src/build.py -->"

CONSENTIMENTO = (SRC / "consentimento.html").read_text(encoding="utf-8")
CONSENTIMENTO = (CONSENTIMENTO
    .replace("{{ADSENSE_PUB}}", ADSENSE_PUB if ADSENSE_LIGADO else "")
    .replace("{{CONSENTIMENTO_BLOQUEIA}}", "true" if CONSENTIMENTO_BLOQUEIA else "false"))

# template  ->  caminho final, relativo à raiz do site
PAGINAS = {
    "index.tpl.html": "index.html",
    "privacidade.tpl.html": "privacidade.html",
    "gobekli-tepe.tpl.html": "dossies/gobekli-tepe.html",
    "amazonia-lidar.tpl.html": "dossies/amazonia-lidar.html",
    "serra-da-capivara.tpl.html": "dossies/serra-da-capivara.html",
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
        raiz_rel = "../" if "/" in destino else ""
        faltando = [m for m in ("{{CSS}}", "{{LOGO}}") if m not in html]
        if faltando:
            print(f"  ! {template}: marcador ausente {', '.join(faltando)}")
            continue

        # Os blocos "TROCA PRONTA" são anotação de trabalho: ficam no template,
        # nunca na página publicada. Sem isto, markup comentado iria para o ar.
        html = re.sub(r"[ \t]*<!--\s*TROCA PRONTA:.*?-->\n?", "", html, flags=re.S)

        saida = RAIZ / destino
        saida.parent.mkdir(parents=True, exist_ok=True)
        saida.write_text(
            html.replace("{{CSS}}", CSS)
                .replace("{{LOGO}}", LOGO)
                .replace("{{DOMINIO}}", DOMINIO.rstrip("/"))
                .replace("{{VISOR}}", VISOR)
                .replace("{{ADSENSE}}", ADSENSE)
                .replace("{{CONSENTIMENTO}}", CONSENTIMENTO.replace("{{RAIZ}}", raiz_rel))
                .replace("{{RAIZ}}", raiz_rel),
            encoding="utf-8",
        )
        print(f"  ✓ {destino}  ({saida.stat().st_size / 1024:.1f} KB)")

    if FAVICON.exists():
        shutil.copyfile(FAVICON, RAIZ / "favicon.svg")
        print("  ✓ favicon.svg")

    # ads.txt precisa ficar na RAIZ do domínio, nunca numa subpasta.
    ads = RAIZ / "ads.txt"
    if ADSENSE_LIGADO:
        ads.write_text(
            "# Vestígio Oculto — declaração de vendedor autorizado (IAB ads.txt)\n"
            "# Gerado por _src/build.py a partir de ADSENSE_PUB. Não editar à mão.\n"
            f"google.com, {ADSENSE_PUB}, DIRECT, f08c47fec0942fa0\n",
            encoding="utf-8")
        print("  ✓ ads.txt")
    elif ads.exists():
        ads.unlink()
        print("  ✓ ads.txt removido")


if __name__ == "__main__":
    print("Vestígio Oculto — gerando páginas")
    main()
    print("pronto.")
