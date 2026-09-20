#!/usr/bin/env python3
"""Baixa as três fontes do npm e gera assets/fontes/ + _src/fontes.css.

Roda de vez em quando, à mão — não faz parte do build. O build só injeta o
fontes.css que este script deixou pronto, e os .woff2 ficam versionados no
repositório. Assim publicar o site não depende de npm nem de rede.

    npm install @fontsource-variable/{inter,cinzel,jetbrains-mono}
    python3 _src/gerar-fontes.py

Por que fonte variável e não os pesos estáticos que o Google servia: o CSS usa
peso 350 no corpo e 700 no <strong> do texto. Com faces estáticas de 300/400/
500/600, o navegador encaixava o 350 no 300 e *sintetizava* o negrito a partir
do 600 — borrão, não negrito de verdade. Um arquivo variável por subconjunto
cobre 100–900 e resolve os dois, pesando menos que os dois estáticos juntos.
"""
import json, re, shutil, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "assets" / "fontes"

# família CSS -> (pacote npm, subconjuntos, estilos)
# Subconjuntos escolhidos pelo que o site de fato escreve:
#   latin-ext  Şanlıurfa, Taş Tepeler, Karacadağ  (dossiê 001)
#   greek      πορφύρας                           (dossiê 004)
#   cyrillic   Александр Байдуков                 (crédito de foto, dossiê 010)
# Cada face tem unicode-range, então um subconjunto só é baixado na página que
# realmente mostra um caractere dele. Incluir os quatro não custa nada a quem
# lê uma página só de português.
FAMILIAS = {
    "Inter":           ("inter",           ["latin", "latin-ext", "greek", "cyrillic"], ["normal", "italic"]),
    "Cinzel":          ("cinzel",          ["latin", "latin-ext"],                      ["normal"]),
    "JetBrains Mono":  ("jetbrains-mono",  ["latin", "latin-ext"],                      ["normal"]),
}

def main(node_modules: Path) -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    for antigo in DESTINO.glob("*.woff2"):
        antigo.unlink()

    blocos, copiados = [], 0
    for familia, (pacote, subconjuntos, estilos) in FAMILIAS.items():
        base = node_modules / "@fontsource-variable" / pacote
        if not base.is_dir():
            sys.exit(f"faltou instalar @fontsource-variable/{pacote}")
        faixas = json.loads((base / "unicode.json").read_text(encoding="utf-8"))
        eixo = json.loads((base / "metadata.json").read_text(encoding="utf-8"))
        peso = eixo["variable"]["wght"]
        for sub in subconjuntos:
            if sub not in faixas:
                sys.exit(f"{pacote} não tem o subconjunto {sub}")
            for estilo in estilos:
                sufixo = "italic" if estilo == "italic" else "normal"
                arq = base / "files" / f"{pacote}-{sub}-wght-{sufixo}.woff2"
                if not arq.exists():
                    sys.exit(f"não achei {arq.name}")
                shutil.copy2(arq, DESTINO / arq.name)
                copiados += 1
                blocos.append(
                    f"/* {familia} · {sub} · {estilo} */\n"
                    "@font-face {\n"
                    f"  font-family: \"{familia}\";\n"
                    f"  font-style: {estilo};\n"
                    f"  font-weight: {peso['min']} {peso['max']};\n"
                    "  font-display: swap;\n"
                    f"  src: url(\"{{{{RAIZ}}}}assets/fontes/{arq.name}\") format(\"woff2-variations\");\n"
                    f"  unicode-range: {faixas[sub]};\n"
                    "}\n"
                )

    cabecalho = (
        "/* ==========================================================================\n"
        "   FONTES — hospedadas aqui, não no Google\n"
        "   Gerado por _src/gerar-fontes.py. Não editar à mão.\n"
        "   O {{RAIZ}} é resolvido pelo build: vira \"\" na raiz e \"../\" nos dossiês,\n"
        "   então o site funciona servido de qualquer pasta, e abrindo o arquivo\n"
        "   direto do disco também.\n"
        "\n"
        "   Antes vinham do Google: duas conexões a terceiros antes de a primeira\n"
        "   letra aparecer, e uma cláusula a mais na política de privacidade.\n"
        "\n"
        "   font-display: swap — o texto aparece na fonte de sistema e troca quando\n"
        "   a fonte chega. Nunca há tela em branco esperando tipografia.\n"
        "   ========================================================================== */\n\n"
    )
    (RAIZ / "_src" / "fontes.css").write_text(cabecalho + "\n".join(blocos), encoding="utf-8")
    print(f"  ✓ {copiados} arquivos em assets/fontes/")
    print(f"  ✓ _src/fontes.css  ({len(blocos)} faces)")

if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "node_modules"))
