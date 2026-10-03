#!/usr/bin/env python3
"""
Vestígio Oculto — build estático.

Injeta nos templates .tpl.html:
  {{CSS}}    → _src/fontes.css + _src/vestigio.css
  {{FONTES}} → preload das fontes hospedadas em assets/fontes/
  {{LOGO}}  → _src/marca/logo-horizontal-escuro-solido.svg (em curvas)

e grava as páginas finais, autocontidas, na raiz do site. Também copia o
símbolo da marca como favicon.svg.

Uso:  python3 _src/build.py       (a partir da raiz do projeto)

Cada página gerada é um único arquivo HTML sem dependências locais — basta
enviar a raiz do projeto para o servidor. O CSS vive num lugar só: edite
_src/vestigio.css e rode o build de novo.
"""

import posixpath
import re
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------
# O domínio é um lugar só: canonical, og:url, og:image, JSON-LD, hreflang,
# sitemap e robots saem todos daqui. Desde 03/10/2026 o principal é o .com;
# o .com.br e o concealedpast.com só redirecionam (ver .htaccess e README).
DOMINIO = "https://vestigiooculto.com"

# Preload só das três faces que toda página usa em português. As de grego,
# cirílico e latin-ext ficam de fora de propósito: o unicode-range já garante
# que só baixam na página que mostra um caractere delas, e dar preload nelas
# forçaria o download em todas.
#
# Desde 03/10/2026, preload SÓ da Inter normal: é a face do texto que vira LCP
# nos dossiês (o subtítulo da capa). O PSI no celular media 2,5 s de atraso de
# renderização do LCP com três fontes (114 KB) disputando a banda com o HTML
# em 4G lento. Cinzel e JetBrains Mono continuam com font-display: swap e
# chegam logo depois, sem segurar a primeira pintura.
FONTES = "\n".join(
    f'<link rel="preload" href="{{{{RAIZ}}}}assets/fontes/{a}" as="font" type="font/woff2" crossorigin>'
    for a in ("inter-latin-wght-normal.woff2",))

# AdSense. ADSENSE_LIGADO = False tira o script de TODAS as páginas e
# apaga o ads.txt — é o interruptor geral, uma linha só.
ADSENSE_LIGADO = True
ADSENSE_PUB = "pub-4401770243539507"

# Consentimento. False = a faixa avisa e o anúncio carrega de imediato; quem
# recusar deixa de receber. True = nada de anúncio até a pessoa clicar em
# "Entendi" — mais conservador com a LGPD, e menos receita.
CONSENTIMENTO_BLOQUEIA = False
# Chave do localStorage onde a faixa guarda a escolha. A mesma que está
# escrita em _src/consentimento.html; o build confere que as duas batem.
CHAVE_CONSENTIMENTO = "vo-consentimento"
# ---------------------------------------------------------------

RAIZ = Path(__file__).resolve().parent.parent
SRC = RAIZ / "_src"

sys.path.insert(0, str(SRC))
from idiomas import (IDIOMAS, HREFLANG, OG_LOCALE, MARCA_SUB, T,  # noqa: E402
                     PALAVRAS_DE_CREDITO_PT, EQUIVALENTES_DE_CREDITO, CHAVES_OBRIGATORIAS)

# As fontes vêm primeiro: o @font-face precisa estar declarado antes de
# qualquer regra que use a família. Arquivo gerado por _src/gerar-fontes.py.
CSS = ((SRC / "fontes.css").read_text(encoding="utf-8") + "\n"
       + (SRC / "vestigio.css").read_text(encoding="utf-8"))

# A marca vai inline: nenhuma requisição extra e nada quebra se o caminho
# mudar. Abaixo de 200 px a identidade pede a versão SÓLIDA, sem tweed.
LOGO = (SRC / "marca" / "logo-horizontal-escuro-solido.svg").read_text(encoding="utf-8")
LOGO = re.sub(r'\s(width|height)="[^"]*"', "", LOGO, count=2)  # o tamanho é do CSS
LOGO = LOGO.replace("<svg ", '<svg role="img" aria-hidden="true" focusable="false" ', 1)
# O SVG traz um <clipPath id="crownclip"> que nada referencia. Como a marca vai
# duas vezes por página (cabeçalho e rodapé), o id saía duplicado — HTML
# inválido. Sai o bloco inteiro.
LOGO = re.sub(r'<defs><clipPath id="crownclip">.*?</clipPath></defs>', "", LOGO, flags=re.S)

FAVICON = SRC / "marca" / "simbolo-escuro-solido.svg"

# Visor de fólios do manuscrito Voynich. Fica num arquivo à parte porque é um
# bloco grande e independente do texto.
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

_CONSENTIMENTO = (SRC / "consentimento.html").read_text(encoding="utf-8")
_CONSENTIMENTO = (_CONSENTIMENTO
    .replace("{{ADSENSE_PUB}}", ADSENSE_PUB if ADSENSE_LIGADO else "")
    .replace("{{CONSENTIMENTO_BLOQUEIA}}", "true" if CONSENTIMENTO_BLOQUEIA else "false"))

if f"var CHAVE = '{CHAVE_CONSENTIMENTO}';" not in _CONSENTIMENTO:
    raise SystemExit(f"  ! consentimento.html não usa a chave {CHAVE_CONSENTIMENTO}")


def consentimento(idioma: str) -> str:
    """A faixa de cookies no idioma da página. A lógica é uma só; o texto
    vem de idiomas.py."""
    c = T[idioma]["consentimento"]
    return (_CONSENTIMENTO.replace("{{C_ARIA}}", c["aria"]).replace("{{C_TEXTO}}", c["texto"])
            .replace("{{C_RECUSAR}}", c["recusar"]).replace("{{C_ACEITAR}}", c["aceitar"]))


# "Rever escolha de cookies", no rodapé de toda página: apaga a escolha salva
# e recarrega, e a faixa volta a aparecer. O script vai junto do link, e não
# no bloco de consentimento, porque o 404 não leva a faixa.
REVER_JS = ("\n<script>\ndocument.querySelectorAll('[data-rever-cookies]').forEach(function (a) {\n"
            "  a.addEventListener('click', function (ev) {\n    ev.preventDefault();\n"
            f"    try {{ localStorage.removeItem('{CHAVE_CONSENTIMENTO}'); }} catch (e) {{}}\n"
            "    location.reload();\n  });\n});\n</script>")


def rodape_rever(html: str, template: str, idioma: str = "pt") -> str:
    """Põe o link "Rever escolha de cookies" ao lado da política de privacidade
    do rodapé. Para se o rodapé não tiver esse link: página sem a revogação
    não sai."""
    if not ADSENSE_LIGADO:
        return html
    m = re.search(r"<footer\b.*?</footer>", html, flags=re.S)
    alvo = f'privacidade.html">{T[idioma]["privacidade"]}</a>'
    if not m or m.group(0).count(alvo) != 1:
        raise SystemExit(f"  ! {template}: rodapé sem o link da política de privacidade")
    rever = f' · <a href="#" role="button" data-rever-cookies>{T[idioma]["rever_cookies"]}</a>'
    rod = m.group(0).replace(alvo, alvo + rever)
    return html[:m.start()] + rod + REVER_JS + html[m.end():]


# template  ->  caminho final, relativo à raiz do site
# ---------------------------------------------------------------- numeração

# A ordem do arquivo, e a única fonte dela.
#
# O número do dossiê aparecia escrito à mão em cerca de 55 pontos, entre o
# selo, o kicker, os cartões de "Leia também", o bloco do próximo e o rodapé.
# Reordenar significava reescrever um grafo, e errar uma entrada mandava o
# leitor para o número de outro dossiê — sem quebrar link nenhum, porque os
# links são por slug, o que torna o erro silencioso.
#
# Agora a ordem mora aqui. O template pede {{NUM}} para o próprio número e
# {{NUM:slug}} para citar outro; a próxima reordenação é uma edição nesta
# lista.
#
# A sequência é a escada de "onde estava escondido", que o canal usa como fio:
# terra, floresta, areia, cinzas, pedra, água, DNA, consenso, à vista de
# todos, arquivo, zona de exclusão — e, do 012 em diante, os degraus anotados
# ao lado de cada slug.
ARQUIVO = [
    "gobekli-tepe",        # 001 · terra
    "amazonia-lidar",      # 002 · floresta
    "nadadores-do-saara",  # 003 · areia
    "papiros-herculano",   # 004 · cinzas
    "grande-piramide",     # 005 · pedra
    "nan-madol",           # 006 · água
    "denisovanos",         # 007 · nosso DNA
    "serra-da-capivara",   # 008 · consenso
    "manuscrito-voynich",  # 009 · à vista de todos
    "percy-fawcett",       # 010 · arquivo
    "sentinela-do-norte",  # 011 · zona de exclusão
    "anticitera",          # 012 · naufrágio
    "linhas-de-nazca",      # 013 · perspectiva
    "puma-punku",           # 014 · em pedaços
    "moais-rapa-nui",       # 015 · debaixo da encosta
    "anomalia-do-baltico",  # 016 · no sonar
    "dna-fantasma",         # 017 · dentro do genoma
    "passagem-dyatlov",     # 018 · debaixo da neve
    "colonia-roanoke",      # 019 · numa palavra entalhada
    "kryptos",              # 020 · num pátio fechado
    "mashco-piro",          # 021 · por escolha
    "korowai",              # 022 · no alto das árvores
]

NUMERO = {slug: f"{i:03d}" for i, slug in enumerate(ARQUIVO, start=1)}


def resolver_numeros(html: str, slug: str) -> str:
    """Troca {{NUM}} e {{NUM:slug}} pelos números da lista acima.

    Quebra o build quando um template cita um slug que não está em ARQUIVO.
    Sem isso o erro seria invisível: o marcador ficaria cru na página, e
    "Dossiê {{NUM:nan-madol}}" só aparece para quem abrir a página pronta.
    """
    if slug in NUMERO:
        html = html.replace("{{NUM}}", NUMERO[slug])

    faltando = []

    def troca(m):
        alvo = m.group(1)
        if alvo not in NUMERO:
            faltando.append(alvo)
            return m.group(0)
        return NUMERO[alvo]

    html = re.sub(r"\{\{NUM:([a-z0-9-]+)\}\}", troca, html)

    if faltando:
        raise SystemExit(
            f"  ! {slug}: cita dossiê fora de ARQUIVO: {', '.join(sorted(set(faltando)))}"
        )
    if "{{NUM" in html:
        raise SystemExit(f"  ! {slug}: sobrou marcador de número sem resolver")
    return html


# ---------------------------------------------------------------- compartilhamento

# Imagem de prévia (og:image / twitter:image / "image" do JSON-LD) de cada
# dossiê: assets/img/og/<slug>.jpg, 1200 x 630, feita sobre a imagem real do
# próprio dossiê (origem e licença em assets/img/CREDITOS.md). O texto é o
# og:image:alt. Dossiê fora deste dicionário usa a genérica; dossiê que está
# aqui e não tem o arquivo PARA o build — prévia quebrada não sai.
OG_GENERICA = "og-vestigio-oculto.jpg"
OG_ALT = {
    "gobekli-tepe": "Recinto escavado de Göbekli Tepe com pilares em T, sob o título Göbekli Tepe",
    "amazonia-lidar": "Relevo por LiDAR com recintos geométricos de terra na Amazônia, sob o título Cidades da Amazônia",
    "nadadores-do-saara": "Pintura rupestre de uma figura humana em pose de nado em Wadi Sura, sob o título Os nadadores do Saara",
    "papiros-herculano": "Rolo de papiro carbonizado de Herculano, sob o título Os papiros de Herculano",
    "grande-piramide": "As fiadas de pedra da Grande Pirâmide de Gizé até o ápice, sob o título A Grande Pirâmide",
    "nan-madol": "Muralhas de basalto colunar de Nan Madol entre a vegetação, sob o título Nan Madol",
    "denisovanos": "Vista de dentro da caverna de Denisova, no Altai, sob o título Denisovanos",
    "serra-da-capivara": "Sedimento com seixos e cascalho na Serra da Capivara, sob o título Serra da Capivara",
    "manuscrito-voynich": "Folha dobrada do manuscrito Voynich com diagramas circulares, sob o título O manuscrito Voynich",
    "percy-fawcett": "Retrato de Percy Fawcett em 1911, sob o título Percy Fawcett",
    "sentinela-do-norte": "A ilha Sentinela do Norte vista da janela de um avião, sob o título A Sentinela do Norte",
    "anticitera": "Réplica moderna do mecanismo de Anticítera, com os mostradores de bronze à mostra, sob o título O mecanismo de Anticítera",
    "linhas-de-nazca": "O beija-flor das Linhas de Nazca visto do alto, sob o título As Linhas de Nazca",
    "puma-punku": "Blocos de pedra em forma de H em Puma Punku, sob o título Puma Punku",
    "moais-rapa-nui": "Moais na encosta de Rano Raraku, na Ilha de Páscoa, sob o título Os moais da Ilha de Páscoa",
    "anomalia-do-baltico": "Golfo de Bótnia visto por satélite, com gelo no mar Báltico, sob o título A anomalia do Báltico",
    "dna-fantasma": "Sala de sequenciadores de DNA, sob o título O DNA fantasma",
    "passagem-dyatlov": "Vale do rio Auspiya, nos Urais, com neve nas árvores, sob o título A passagem Dyatlov",
    "colonia-roanoke": "Mapa da Virgínia de Theodor de Bry, 1590, com a ilha de Roanoke, sob o título A colônia de Roanoke",
    "kryptos": "A escultura Kryptos, de Jim Sanborn, sob o título Kryptos",
    "mashco-piro": "O rio Las Piedras serpenteando pela floresta amazônica do Peru, sob o título Os mashco piro",
    "korowai": "Silhueta de uma casa na árvore entre palmeiras, na Papua, sob o título Os korowai",
}


def og_do_idioma(slug: str, idioma: str = "pt") -> str:
    """Caminho da prévia do dossiê, relativo a assets/img/."""
    return f"og/{slug}.jpg" if idioma == "pt" else f"og/{idioma}/{slug}.jpg"


def imagem_de_compartilhamento(html: str, slug: str, template: str, idioma: str = "pt") -> str:
    """Aponta og:image, twitter:image e o "image" do JSON-LD para a prévia do
    dossiê, com 1200 x 630 e alt. Para se o arquivo apontado não existir.

    Fora do português a prévia é a do idioma, assets/img/og/<idioma>/<slug>.jpg,
    com o título traduzido gravado nela (gerada pelo mesmo script das
    portuguesas); o alt é traduzido, em idiomas.py. Falta a imagem do idioma,
    o build para: prévia com título em outra língua não sai."""
    if slug in OG_ALT:
        nome = og_do_idioma(slug, idioma)
        if not (RAIZ / "assets" / "img" / nome).is_file():
            raise SystemExit(f"  ! {slug}: prévia de compartilhamento ausente: assets/img/{nome}")
        url = f"{{{{DOMINIO}}}}/assets/img/{nome}"
        alt = (OG_ALT[slug] if idioma == "pt" else T[idioma]["og_alt"][slug]).replace('"', "&quot;")
        html, n = re.subn(r'<meta property="og:image" content="[^"]*">',
                          f'<meta property="og:image" content="{url}">', html, count=1)
        if n != 1:
            raise SystemExit(f"  ! {template}: sem meta og:image")
        html = re.sub(r'<meta property="og:image:(width|height|alt)" content="[^"]*">\n?', "", html)
        html = html.replace(f'<meta property="og:image" content="{url}">',
                            f'<meta property="og:image" content="{url}">\n'
                            '<meta property="og:image:width" content="1200">\n'
                            '<meta property="og:image:height" content="630">\n'
                            f'<meta property="og:image:alt" content="{alt}">', 1)
        html, n = re.subn(r'("image":\s*)"[^"]*"', rf'\1"{url}"', html, count=1)
        if n != 1:
            raise SystemExit(f"  ! {template}: JSON-LD sem \"image\"")
        tw = (f'<meta name="twitter:image" content="{url}">\n'
              f'<meta name="twitter:image:alt" content="{alt}">\n')
    else:
        achou = re.search(r'<meta property="og:image" content="([^"]*)">', html)
        tw = f'<meta name="twitter:image" content="{achou.group(1)}">\n' if achou else ""
    if "twitter:image" not in html and tw:
        html = html.replace('<meta name="twitter:card" content="summary_large_image">\n',
                            '<meta name="twitter:card" content="summary_large_image">\n' + tw, 1)
    # toda imagem de compartilhamento apontada tem de existir no disco
    for caminho in set(re.findall(r'\{\{DOMINIO\}\}/(assets/img/[^"]+\.(?:jpg|png))"', html)):
        if re.search(rf'(og:image"|twitter:image"|"image":)[^\n]*{re.escape(caminho)}', html) \
                and not (RAIZ / caminho).is_file():
            raise SystemExit(f"  ! {template}: imagem de compartilhamento inexistente: {caminho}")
    return html


# ---------------------------------------------------------------- navegação

# ---------------------------------------------------------------- idiomas
#
# Português na raiz, com os caminhos de sempre; cada outro idioma numa pasta
# (/en/, /es/) com os MESMOS nomes de arquivo. Uma página só existe num idioma
# se o template traduzido existir em _src/<idioma>/. A "chave" de uma página é
# o caminho dela sem o prefixo do idioma (dossies/gobekli-tepe.html): é por
# ela que as versões se reconhecem como a mesma página.

INTERFACE = ["index.html", "sobre.html", "contato.html", "privacidade.html", "404.html"]


def pasta(idioma: str) -> Path:
    return SRC if idioma == "pt" else SRC / idioma


def prefixo(idioma: str) -> str:
    return "" if idioma == "pt" else f"{idioma}/"


def base_url(idioma: str) -> str:
    return DOMINIO.rstrip("/") + ("" if idioma == "pt" else f"/{idioma}")


def url_de(idioma: str, chave: str) -> str:
    b = base_url(idioma)
    return b + "/" if chave == "index.html" else f"{b}/{chave}"


def templates_do_idioma(idioma: str) -> dict:
    """chave -> template, só das páginas que existem no idioma."""
    saida = {}
    for tpl, chave in PAGINAS.items():
        caminho = pasta(idioma) / tpl
        if caminho.is_file():
            saida[chave] = caminho
    return saida


def dossies_do_idioma(idioma: str) -> list:
    return [s for s in ARQUIVO if (pasta(idioma) / f"{s}.tpl.html").is_file()]


def idiomas_ativos() -> list:
    """Português sempre; os outros quando têm home traduzida e um dossiê.

    Idioma ativo precisa da interface inteira (home, sobre, contato,
    privacidade, 404) e do dicionário completo; faltando, o build para em vez
    de publicar um idioma com link quebrado no rodapé."""
    ativos = ["pt"]
    for idioma in IDIOMAS[1:]:
        if not (pasta(idioma) / "index.tpl.html").is_file() or not dossies_do_idioma(idioma):
            continue
        tem = templates_do_idioma(idioma)
        faltam = [c for c in INTERFACE if c not in tem]
        faltam += [f"idiomas.py: {k}" for k in CHAVES_OBRIGATORIAS if k not in T.get(idioma, {})]
        faltam += [f"cartoes/{s}.html" for s in dossies_do_idioma(idioma)
                   if not (pasta(idioma) / "cartoes" / f"{s}.html").is_file()]
        faltam += [f"idiomas.py: og_alt de {s}" for s in dossies_do_idioma(idioma)
                   if s not in T[idioma].get("og_alt", {})]
        if faltam:
            raise SystemExit(f"  ! idioma {idioma}: falta {', '.join(faltam)}")
        ativos.append(idioma)
    return ativos


def temas_do_idioma(idioma: str) -> list:
    """Pilares com página no idioma. Fora do português, só quando o texto do
    pilar está traduzido E todos os dossiês dele também: a introdução nomeia
    cada caso, e prometer na página o que não está nela seria pior que não
    ter a página."""
    if idioma == "pt":
        return list(TEMAS)
    tem = set(dossies_do_idioma(idioma))
    pilar_de = {s: p for p, s, _ in cartoes_da_home()}
    return [k for k in TEMAS
            if T[idioma].get("temas", {}).get(k, {}).get("intro")
            and all(s in tem for s, p in pilar_de.items() if p == k)]


def paginas_existentes(idioma: str) -> set:
    """Todas as chaves que existem no idioma, inclusive páginas de pilar."""
    return (set(templates_do_idioma(idioma))
            | {f"temas/{TEMAS[k]['slug']}.html" for k in temas_do_idioma(idioma)})


def relativo(de: str, para: str) -> str:
    """Caminho relativo entre duas páginas dadas a partir da raiz do site."""
    return posixpath.relpath(para, posixpath.dirname(de) or ".")


def titulo_do_dossie(slug: str, idioma: str = "pt") -> str:
    """O <h1> do template, sem marcação. É o título que todo link usa."""
    html = (pasta(idioma) / f"{slug}.tpl.html").read_text(encoding="utf-8")
    achou = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if not achou:
        raise SystemExit(f"  ! {slug}: template sem <h1>")
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", achou.group(1))).strip()


def proximo_de(slug: str) -> str:
    """O dossiê seguinte em ARQUIVO; o último volta ao primeiro."""
    i = ARQUIVO.index(slug)
    return ARQUIVO[(i + 1) % len(ARQUIVO)]


def bloco_proximo(slug: str, idioma: str = "pt") -> str:
    """O link "próximo" de cada dossiê, gerado — nunca escrito à mão.

    Até 03/10/2026 cada template trazia o próprio "próximo", e eles tinham
    virado um grafo arbitrário: dez dossiês não recebiam link de nenhum outro,
    e o mesmo dossiê aparecia com três títulos diferentes. Agora o próximo é
    sempre o número seguinte de ARQUIVO (o 022 volta ao 001), e o título é o
    <h1> da página de destino.

    Fora do português, se o seguinte ainda não foi traduzido, o link vai para
    o original, com o título original e o aviso "em português".
    """
    alvo = proximo_de(slug)
    traduzido = alvo in dossies_do_idioma(idioma)
    titulo = titulo_do_dossie(alvo, idioma if traduzido else "pt")
    aviso = "" if traduzido else f' · {T[idioma]["em_portugues"]}'
    return (
        f'<a class="proximo" href="{alvo}.html">\n'
        f'      <span>\n'
        f'        <span class="mono">{T[idioma]["proximo"]} {NUMERO[alvo]}{aviso}</span>\n'
        f'        <strong>{titulo}</strong>\n'
        f'      </span>\n'
        f'      <span class="seta">→</span>\n'
        f'    </a>')


def conferir_relacionados(idioma: str = "pt") -> None:
    """O "Leia também" é escrito à mão; isto confere o que derrapa nele.

    Quebra o build quando um item cita o dossiê com título diferente do <h1>
    dele, ou quando repete o "próximo" — que já aparece logo abaixo. Numa
    tradução, o título citado é o do dossiê traduzido; se o destino ainda não
    foi traduzido, é o do original (o link vai para ele).
    """
    erros = []
    traduzidos = dossies_do_idioma(idioma)
    for slug in traduzidos:
        html = (pasta(idioma) / f"{slug}.tpl.html").read_text(encoding="utf-8")
        if html.count("{{PROXIMO}}") != 1:
            erros.append(f"{slug}: precisa de exatamente um {{{{PROXIMO}}}}")
        nav = re.search(r'<nav class="relacionados".*?</nav>', html, re.S)
        if not nav:
            continue
        for alvo, titulo in re.findall(
                r'<a href="([a-z0-9-]+)\.html">\s*<span class="num">[^<]*</span>\s*<strong>(.*?)</strong>',
                nav.group(0), re.S):
            if alvo not in NUMERO:
                erros.append(f"{slug}: Leia também cita {alvo}, fora de ARQUIVO")
                continue
            if alvo == proximo_de(slug):
                erros.append(f"{slug}: Leia também repete o próximo ({alvo})")
            certo = titulo_do_dossie(alvo, idioma if alvo in traduzidos else "pt")
            if re.sub(r"\s+", " ", titulo).strip() != certo:
                erros.append(f"{slug}: Leia também chama {alvo} de \"{titulo}\"; "
                             f"o título é \"{certo}\"")
    if erros:
        raise SystemExit(f"  ! [{idioma}] " + f"\n  ! [{idioma}] ".join(erros))


def conferir_contagens_da_home() -> None:
    """Os números da home são escritos à mão; aqui eles são contados.

    Em 03/10/2026 a home dizia 21 dossiês e "Publicados: 10" com 22 cartões
    publicados, e o pilar Pedra e Poeira dizia 6 tendo 7.
    """
    html = (SRC / "index.tpl.html").read_text(encoding="utf-8")
    cartoes = re.findall(r'<article class="quadro" data-pilar="([a-z]+)"', html)
    total = len(cartoes)
    erros = []
    for padrao in (r'Arquivo aberto · (\d+) dossiês',
                   r'<span class="rotulo">Dossiês</span><span class="valor">(\d+)</span>',
                   r'<span class="rotulo">Publicados</span><span class="valor viva">(\d+)</span>',
                   r'id="contador">(\d+) dossiês'):
        achou = re.search(padrao, html)
        if not achou or int(achou.group(1)) != total:
            erros.append(f"esperado {total} em {padrao!r}")
    ids = {"pedra": "pedra-e-poeira", "ontem": "descoberto-ontem",
           "selado": "arquivo-selado", "isolados": "ultimos-isolados"}
    for pilar, ident in ids.items():
        achou = re.search(rf'id="{ident}".*?<span class="contagem">(\d+) dossiês', html, re.S)
        n = cartoes.count(pilar)
        if not achou or int(achou.group(1)) != n:
            erros.append(f"pilar {pilar}: esperado {n:02d}")
    if erros:
        raise SystemExit("  ! index.tpl.html: " + "; ".join(erros))


def sem_comentarios(html: str) -> str:
    """Tira os comentários HTML da página publicada (fora de <script>).

    Comentário de template é anotação de trabalho — numeração, decisões,
    pendências. No ar ele só expõe bastidor no código-fonte.
    """
    partes = re.split(r"(<script\b.*?</script>)", html, flags=re.S | re.I)
    for i in range(0, len(partes), 2):
        partes[i] = re.sub(r"[ \t]*<!--.*?-->[ \t]*\r?\n?", "", partes[i], flags=re.S)
    return "".join(partes)


# ---------------------------------------------------------------- SEO

TITULO_MAX = 60
DESCRICAO_MIN, DESCRICAO_MAX = 120, 155


def marcadores_de_idioma(html: str, idioma: str) -> str:
    """Marcadores que dependem só do idioma (valem também no <title>)."""
    return html.replace("{{MARCA_SUB}}", MARCA_SUB[idioma]).replace("{{BASE}}", base_url(idioma))


def meta_do_template(caminho: Path, idioma: str = "pt") -> tuple:
    html = marcadores_de_idioma(caminho.read_text(encoding="utf-8"), idioma)
    t = re.search(r"<title>(.*?)</title>", html, re.S)
    d = re.search(r'<meta name="description" content="([^"]*)"', html)
    return (t.group(1).strip() if t else ""), (d.group(1) if d else "")


def texto_do_tema(chave: str, idioma: str) -> dict:
    """Nome, título, descrição e introdução do pilar no idioma."""
    t = TEMAS[chave]
    if idioma == "pt":
        return t
    return {**t, "nome": T[idioma]["pilares"][chave], **T[idioma]["temas"][chave]}


def conferir_seo(idioma: str = "pt") -> None:
    """Porteiro de <title> e meta description, antes de gravar qualquer página.

    Em 03/10/2026 metade dos dossiês tinha título acima de 60 caracteres (o
    Google corta) e descrição de mais de 200 (idem). Regra: título até 60,
    único, assunto primeiro e a marca no fim; descrição de 120 a 155, única.
    A 404 não entra na conta da descrição (é noindex). Vale por idioma.
    """
    erros, vistos_t, vistos_d = [], {}, {}
    metas = [(f"{prefixo(idioma)}{c}", *meta_do_template(p, idioma))
             for c, p in templates_do_idioma(idioma).items()]
    metas += [(f"{prefixo(idioma)}temas/{TEMAS[k]['slug']}", texto_do_tema(k, idioma)["titulo"],
               texto_do_tema(k, idioma)["descricao"]) for k in temas_do_idioma(idioma)]
    for template, t, d in metas:
        if not t or len(t) > TITULO_MAX:
            erros.append(f"{template}: título com {len(t)} caracteres (máx. {TITULO_MAX})")
        if not template.endswith("404.html") and not DESCRICAO_MIN <= len(d) <= DESCRICAO_MAX:
            erros.append(f"{template}: descrição com {len(d)} caracteres "
                         f"({DESCRICAO_MIN}–{DESCRICAO_MAX})")
        if t in vistos_t:
            erros.append(f"{template}: título igual ao de {vistos_t[t]}")
        if d in vistos_d:
            erros.append(f"{template}: descrição igual à de {vistos_d[d]}")
        vistos_t[t], vistos_d[d] = template, template
    if erros:
        raise SystemExit("  ! SEO: " + "\n  ! SEO: ".join(erros))


def breadcrumb(slug: str, idioma: str = "pt") -> str:
    """BreadcrumbList do dossiê: Vestígio Oculto › título (o <h1>). Gerado."""
    import json
    dados = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Vestígio Oculto",
             "item": url_de(idioma, "index.html")},
            {"@type": "ListItem", "position": 2, "name": titulo_do_dossie(slug, idioma),
             "item": url_de(idioma, f"dossies/{slug}.html")},
        ],
    }
    return ('<script type="application/ld+json">\n'
            + json.dumps(dados, ensure_ascii=False, indent=2) + "\n</script>\n</head>")


def data_modificacao(caminho: Path) -> str:
    """lastmod do sitemap. Dossiê: o dateModified do próprio JSON-LD, que é a
    data editorial. Outras páginas: o último commit do template, ou hoje se
    ele tem mudança ainda não publicada. A home leva a mais recente de todas.
    """
    import subprocess
    from datetime import date
    html = caminho.read_text(encoding="utf-8")
    achou = re.search(r'"dateModified":\s*"(\d{4}-\d{2}-\d{2})"', html)
    if achou:
        return achou.group(1)
    rel = caminho.relative_to(RAIZ).as_posix()
    try:
        sujo = subprocess.run(["git", "status", "--porcelain", "--", rel],
                              cwd=RAIZ, capture_output=True, text=True).stdout.strip()
        if not sujo:
            data = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel],
                                  cwd=RAIZ, capture_output=True, text=True).stdout.strip()
            if data:
                return data
    except OSError:
        pass
    return date.today().isoformat()


PAGINAS = {
    "index.tpl.html": "index.html",
    "privacidade.tpl.html": "privacidade.html",
    "sobre.tpl.html": "sobre.html",
    "contato.tpl.html": "contato.html",
    "404.tpl.html": "404.html",
    "gobekli-tepe.tpl.html": "dossies/gobekli-tepe.html",
    "amazonia-lidar.tpl.html": "dossies/amazonia-lidar.html",
    "nadadores-do-saara.tpl.html": "dossies/nadadores-do-saara.html",
    "serra-da-capivara.tpl.html": "dossies/serra-da-capivara.html",
    "papiros-herculano.tpl.html": "dossies/papiros-herculano.html",
    "percy-fawcett.tpl.html": "dossies/percy-fawcett.html",
    "manuscrito-voynich.tpl.html": "dossies/manuscrito-voynich.html",
    "denisovanos.tpl.html": "dossies/denisovanos.html",
    "sentinela-do-norte.tpl.html": "dossies/sentinela-do-norte.html",
    "grande-piramide.tpl.html": "dossies/grande-piramide.html",
    "nan-madol.tpl.html": "dossies/nan-madol.html",
    "anticitera.tpl.html": "dossies/anticitera.html",
    "linhas-de-nazca.tpl.html": "dossies/linhas-de-nazca.html",
    "puma-punku.tpl.html": "dossies/puma-punku.html",
    "moais-rapa-nui.tpl.html": "dossies/moais-rapa-nui.html",
    "anomalia-do-baltico.tpl.html": "dossies/anomalia-do-baltico.html",
    "dna-fantasma.tpl.html": "dossies/dna-fantasma.html",
    "passagem-dyatlov.tpl.html": "dossies/passagem-dyatlov.html",
    "colonia-roanoke.tpl.html": "dossies/colonia-roanoke.html",
    "kryptos.tpl.html": "dossies/kryptos.html",
    "mashco-piro.tpl.html": "dossies/mashco-piro.html",
    "korowai.tpl.html": "dossies/korowai.html",
}


def variantes_de_imagem() -> None:
    """Gera as versões reduzidas usadas pelo srcset da home.

    Os quadros são exibidos entre ~358 px (celular) e 628 px (duas colunas a
    partir de 1280). Servir sempre o arquivo grande fazia a home baixar 2,2 MB
    mesmo em tela comum. Com 640 e 800 no srcset, o navegador escolhe o menor
    que serve — e a home cai para cerca de 700 KB em 1x.

    É idempotente: só regera o que está faltando ou desatualizado.
    """
    try:
        from PIL import Image
    except ImportError:
        print("  ! Pillow ausente: variantes de imagem não geradas")
        return

    img = RAIZ / "assets" / "img"
    if not img.is_dir():
        return

    # quais arquivos a home usa, e em que larguras
    alvo = {}
    home = SRC / "index.tpl.html"
    if home.exists():
        for nome in re.findall(r'<img src="assets/img/([^"]+)"', home.read_text(encoding="utf-8")):
            if re.search(r"-(640|800|960|1280)\.", nome):
                continue
            alvo[nome] = (640, 800, 960, 1280) if nome.startswith("001-gobekli-tepe-capa") else (640, 800)

    feitas = 0
    for nome, larguras in alvo.items():
        origem = img / nome
        if not origem.exists():
            continue
        im = None
        for L in larguras:
            destino = img / f"{origem.stem}-{L}{origem.suffix}"
            if destino.exists() and destino.stat().st_mtime >= origem.stat().st_mtime:
                continue
            if im is None:
                im = Image.open(origem).convert("RGB")
            if L >= im.width:
                continue
            alt = int(round(im.height * L / im.width))
            im.resize((L, alt), Image.LANCZOS).save(
                destino, "JPEG", quality=80, progressive=True, optimize=True)
            feitas += 1

    feitas += webp_dos_png(img, Image)
    if feitas:
        print(f"  ✓ {feitas} variante(s) de imagem")


def webp_dos_png(img, Image) -> int:
    """Converte para WebP todo PNG que algum <picture> referencia.

    Só os PNG valem a conversão. Os JPEG do acervo já estão em q82 e o WebP não
    tira nada deles — alguns até crescem. Nos dois PNG de figura científica o
    ganho é de 87%: o formato guarda cor chapada e linha fina sem o desperdício
    do PNG, e o canal alfa dos dois é 100% opaco, peso morto puro.

    O PNG continua no repositório como fallback do <picture>. Ele não é baixado
    por nenhum navegador lançado depois de 2020.
    """
    alvos = set()
    for tpl in SRC.glob("*.tpl.html"):
        texto = tpl.read_text(encoding="utf-8")
        for nome in re.findall(r'srcset="[^"]*assets/img/([^"]+)\.webp"', texto):
            alvos.add(nome + ".png")

    feitas = 0
    for nome in sorted(alvos):
        origem = img / nome
        destino = origem.with_suffix(".webp")
        if not origem.exists():
            print(f"  ! PNG ausente para o WebP referenciado: {nome}")
            continue
        if destino.exists() and destino.stat().st_mtime >= origem.stat().st_mtime:
            continue
        Image.open(origem).convert("RGB").save(destino, "WEBP", quality=82, method=6)
        feitas += 1
    return feitas


def conferir_ordem_da_home() -> None:
    """A home tem de listar os dossiês na ordem dos episódios.

    Os cartões da home são escritos à mão no index.tpl.html, e por isso
    derrapam. Em 28/09/2026 a ordem publicada era 001, 002, 003, **008**, 004,
    **011**, 005, **010**, **009**, 006, 007 — restos da renumeração de
    20/09/2026, com os dossiês novos anexados no fim. Quem chegava ao site
    vindo de um vídeo não achava o dossiê seguinte onde ele deveria estar.

    A causa raiz foi um cartão inserido **sem o comentário de numeração** (o da
    Serra da Capivara). Ele escondeu o desalinhamento de quem lesse só os
    comentários, que continuavam em sequência.

    ARQUIVO manda. Esta função só compara, e quebra o build quando divergir.
    """
    html = (SRC / "index.tpl.html").read_text(encoding="utf-8")
    blocos = re.findall(r'<article class="quadro".*?</article>', html, re.S)

    publicados = []
    for bloco in blocos:
        achou = re.search(r"dossies/([a-z-]+)[.]html", bloco)
        if achou:
            publicados.append(achou.group(1))

    fora = [s for s in publicados if s not in NUMERO]
    if fora:
        raise SystemExit(f"  ! index.tpl.html: cartão fora de ARQUIVO: {fora}")

    esperado = [s for s in ARQUIVO if s in publicados]
    if publicados != esperado:
        linhas = ["  ! index.tpl.html: os cartões não seguem a ordem de ARQUIVO"]
        for i, (tem, devia) in enumerate(zip(publicados, esperado), start=1):
            if tem != devia:
                linhas.append(f"      posição {i}: está {tem}, deveria ser {devia}")
        raise SystemExit("\n".join(linhas))

    numerados = re.findall(r'<!-- ([0-9]{3}) -->\s*<article class="quadro"', html)
    if len(numerados) != len(blocos):
        raise SystemExit(
            f"  ! index.tpl.html: {len(blocos)} cartões e {len(numerados)} "
            "comentários de numeração. Cartão sem comentário foi exatamente "
            "como a ordem se perdeu da última vez.")
    if numerados != [f"{i:03d}" for i in range(1, len(blocos) + 1)]:
        raise SystemExit(
            "  ! index.tpl.html: os comentários de numeração não estão em "
            "sequência")


# ---------------------------------------------------------------- pilares (páginas de tema)

# Os quatro pilares da home viram páginas próprias em temas/<slug>.html, em vez
# de uma taxonomia paralela. Quem decide o pilar de cada dossiê é o
# data-pilar do cartão na home (e o articleSection do dossiê tem de bater).
# Os cartões são copiados da home — imagem, crédito de licença, resumo — para
# não existir um segundo texto escrito à mão para o mesmo dossiê.
# A introdução só repete o que os dossiês dizem.
TEMAS = {
    "pedra": {
        "slug": "pedra-e-poeira", "nome": "Pedra e Poeira",
        "titulo": "Pedra e Poeira: monumentos antigos · Vestígio Oculto",
        "descricao": "Göbekli Tepe, Grande Pirâmide, Nan Madol, Linhas de Nazca, Puma Punku, "
                     "moais e os nadadores do Saara: monumentos antigos lidos pela evidência.",
        "intro": [
            "Pedra e Poeira reúne os dossiês sobre monumentos e sítios antigos que não cabem "
            "na cronologia aceita: o que foi erguido, pintado ou raspado no chão antes de "
            "existir quem, em tese, soubesse fazer.",
            "São sete casos. Os pilares de Göbekli Tepe, erguidos por caçadores-coletores antes "
            "da agricultura; os nadadores pintados no Gilf Kebir, um dos lugares mais secos do "
            "planeta; os vazios que detectores de partículas mapearam dentro da Grande Pirâmide; "
            "a cidade de basalto de Nan Madol, construída sobre um recife na Micronésia; as "
            "Linhas de Nazca, raspadas no deserto do Peru; os blocos em H de Puma Punku, no "
            "altiplano da Bolívia; e os moais de Rapa Nui, com corpo inteiro debaixo da encosta.",
            "Em todos, a cronologia vem antes da teoria: primeiro o que está no chão e como foi "
            "datado, depois as hipóteses, da mais sóbria à mais improvável, com o peso de "
            "evidência de cada uma declarado.",
        ],
    },
    "ontem": {
        "slug": "descoberto-ontem", "nome": "Descoberto Ontem",
        "titulo": "Descoberto Ontem: descobertas recentes · Vestígio Oculto",
        "descricao": "Lidar na Amazônia, papiros de Herculano, denisovanos, Serra da Capivara, "
                     "Anticítera, anomalia do Báltico e DNA fantasma: o que a tecnologia revelou.",
        "intro": [
            "Descoberto Ontem reúne os achados que só apareceram porque a tecnologia mudou: "
            "lidar, tomografia, sequenciamento de DNA, sonar — instrumentos novos relendo "
            "evidências antigas.",
            "O laser que atravessou o dossel da Amazônia e desenhou ruas e pirâmides de terra; "
            "a tomografia somada a aprendizado de máquina que começou a ler os papiros "
            "carbonizados de Herculano; o DNA de um fragmento de falange que revelou os "
            "denisovanos; o carvão da Serra da Capivara, no Piauí, que não cabe na cronologia "
            "das Américas; os raios X e a tomografia que leram as engrenagens do mecanismo de "
            "Anticítera; a imagem de sonar da anomalia do Báltico; e o modelo estatístico que "
            "estimou um DNA fantasma em populações da África Ocidental.",
            "Descoberta recente não é caso encerrado. Em vários desses dossiês o dado é firme e "
            "a interpretação segue em disputa, e o texto separa uma coisa da outra.",
        ],
    },
    "selado": {
        "slug": "arquivo-selado", "nome": "Arquivo Selado",
        "titulo": "Arquivo Selado: mistérios não resolvidos · Vestígio Oculto",
        "descricao": "Manuscrito Voynich, Percy Fawcett, passo Dyatlov, colônia de Roanoke e "
                     "Kryptos: mistérios não resolvidos, o que já se sabe e o que segue em aberto.",
        "intro": [
            "Arquivo Selado reúne documentos sem decifração e expedições sem desfecho: casos em "
            "que o registro existe, está preservado — e continua ilegível ou incompleto.",
            "O manuscrito Voynich, em pergaminho autêntico e num idioma que ninguém identificou; "
            "Percy Fawcett, que entrou no Alto Xingu em 1925 atrás de uma cidade que chamava de "
            "“Z” e não voltou; os nove esquiadores da passagem Dyatlov, nos Urais, em 1959; a "
            "colônia de Roanoke, que deixou CROATOAN entalhado num poste; e Kryptos, a escultura "
            "no pátio da CIA cuja quarta mensagem segue com o método desconhecido.",
            "Aqui o mistério raramente é a falta de documento. É o documento que existe e não "
            "fecha — e cada dossiê mostra o que já foi descartado, o que é hipótese e o que "
            "continua em aberto.",
        ],
    },
    "isolados": {
        "slug": "ultimos-isolados", "nome": "Últimos Isolados",
        "titulo": "Últimos Isolados: povos isolados · Vestígio Oculto",
        "descricao": "Ilha Sentinela do Norte, mashco piro e korowai: povos e territórios fora "
                     "do alcance, o que se sabe deles e o que a nossa curiosidade custa a eles.",
        "intro": [
            "Últimos Isolados reúne territórios e povos fora do alcance do mundo contemporâneo "
            "— e o que a nossa curiosidade custa a eles.",
            "A ilha Sentinela do Norte, no arquipélago de Andamão, cuja população recusa contato "
            "há gerações; os mashco piro, descendentes de quem fugiu dos massacres da borracha, "
            "em isolamento voluntário entre o Peru e o Acre; e os korowai, da Papua, cujas casas "
            "no alto das árvores viraram, em trinta anos de fotografias, o retrato de um povo "
            "inteiro.",
            "Nesses dossiês o mistério não está enterrado. Quase tudo o que se sabe foi visto de "
            "longe, e a pergunta muda: não é só o que existe ali, é o que decidimos não "
            "perguntar.",
        ],
    },
}
TEMA_DE_SLUG = {t["slug"]: k for k, t in TEMAS.items()}


def cartoes_da_home(idioma: str = "pt") -> list:
    """(pilar, slug, html do cartão) na ordem da home.

    Em português os cartões estão escritos na própria home. Nos outros
    idiomas, cada dossiê traduzido tem o seu em _src/<idioma>/cartoes/, e a
    home do idioma é montada com eles, na ordem de ARQUIVO."""
    if idioma == "pt":
        html = (SRC / "index.tpl.html").read_text(encoding="utf-8")
        blocos = re.findall(r'<article class="quadro".*?</article>', html, re.S)
    else:
        blocos = []
        for s in dossies_do_idioma(idioma):
            texto = (pasta(idioma) / "cartoes" / f"{s}.html").read_text(encoding="utf-8")
            achou = re.findall(r'<article class="quadro".*?</article>', texto, re.S)
            if len(achou) != 1:
                raise SystemExit(f"  ! {idioma}/cartoes/{s}.html: precisa de exatamente um cartão")
            blocos.append(achou[0])
    saida = []
    for bloco in blocos:
        pilar = re.search(r'data-pilar="([a-z]+)"', bloco).group(1)
        slug = re.search(r'dossies/([a-z0-9-]+)\.html', bloco).group(1)
        saida.append((pilar, slug, bloco))
    return saida


def pilar_do_dossie(idioma: str = "pt") -> dict:
    """slug do dossiê -> chave do pilar. Para se o articleSection divergir.

    Quem decide o pilar é o cartão da home em português; a tradução tem de
    declarar o mesmo pilar, com o nome traduzido."""
    mapa, erros = {}, []
    for pilar, slug, _ in cartoes_da_home():
        mapa[slug] = pilar
    if idioma != "pt":
        for pilar, slug, _ in cartoes_da_home(idioma):
            if mapa.get(slug) != pilar:
                erros.append(f"{idioma}/cartoes/{slug}.html: data-pilar {pilar!r} ≠ {mapa.get(slug)!r}")
    nomes = {k: texto_do_tema(k, idioma)["nome"] if idioma == "pt" else T[idioma]["pilares"][k]
             for k in TEMAS}
    for slug in dossies_do_idioma(idioma):
        if slug not in mapa:
            continue
        tpl = (pasta(idioma) / f"{slug}.tpl.html").read_text(encoding="utf-8")
        sec = re.search(r'"articleSection":\s*"([^"]+)"', tpl)
        if not sec or sec.group(1) != nomes[mapa[slug]]:
            erros.append(f"{prefixo(idioma)}{slug}: articleSection {sec.group(1) if sec else None!r} "
                         f"≠ pilar da home {nomes[mapa[slug]]!r}")
    faltam = [s for s in ARQUIVO if s not in mapa]
    if faltam:
        erros.append(f"dossiês sem pilar na home: {faltam}")
    if erros:
        raise SystemExit("  ! pilares: " + "\n  ! pilares: ".join(erros))
    return mapa


def tema_template(chave: str, idioma: str = "pt") -> str:
    """Monta, em memória, o template da página do pilar. Ela passa depois pelo
    mesmo caminho das outras páginas (CSS, logo, consentimento, rodapé)."""
    import json
    t = texto_do_tema(chave, idioma)
    L = T[idioma]
    dom = DOMINIO.rstrip("/")
    url = url_de(idioma, f"temas/{t['slug']}.html")
    cartoes = [(s, b) for p, s, b in cartoes_da_home(idioma) if p == chave]
    blocos = []
    for i, (slug, b) in enumerate(cartoes):
        b = (b.replace('src="assets/', 'src="../assets/')
              .replace('href="dossies/', 'href="../dossies/'))
        b = re.sub(r'srcset="([^"]*)"',
                   lambda m: 'srcset="' + m.group(1).replace("assets/", "../assets/") + '"', b)
        b = b.replace('href="../dossies/', 'href="../dossies/')
        if i == 0:  # o primeiro cartão é o LCP da página: sem lazy, com prioridade
            b = b.replace(' loading="lazy"', ' fetchpriority="high"', 1)
        blocos.append("      " + b)
    com_pagina = temas_do_idioma(idioma)
    outros = [(k, texto_do_tema(k, idioma)) for k in TEMAS if k != chave]
    og = f"{dom}/assets/img/{og_do_idioma(cartoes[0][0], idioma)}"
    ld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": t["titulo"].split(" · ")[0],
        "description": t["descricao"],
        "url": url,
        "inLanguage": HREFLANG[idioma],
        "image": og,
        "isPartOf": {"@type": "WebSite", "name": "Vestígio Oculto", "url": url_de(idioma, "index.html")},
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Vestígio Oculto",
                 "item": url_de(idioma, "index.html")},
                {"@type": "ListItem", "position": 2, "name": t["nome"], "item": url},
            ],
        },
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(cartoes),
            "itemListElement": [
                {"@type": "ListItem", "position": i, "name": titulo_do_dossie(s, idioma),
                 "url": url_de(idioma, f"dossies/{s}.html")}
                for i, (s, _) in enumerate(cartoes, start=1)],
        },
    }
    intro = "\n\n".join(f"    <p>{p}</p>" for p in t["intro"])
    nav_outros = "\n".join(
        f'        <li><a href="{o["slug"] + ".html" if k in com_pagina else "../index.html#" + o["slug"]}">\n'
        f'          <span class="num">{L["pilar"]}</span>\n'
        f'          <strong>{o["nome"]}</strong>\n'
        f'        </a></li>' for k, o in outros)
    nav_pilares = "\n".join(
        f'        <li><a href="{o["slug"] + ".html" if k in com_pagina else "../index.html#" + o["slug"]}">'
        f'{o["nome"]}</a></li>'
        for k, o in [(k, texto_do_tema(k, idioma)) for k in TEMAS])
    return f"""<!DOCTYPE html>
<html lang="{HREFLANG[idioma]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['titulo']}</title>
<meta name="description" content="{t['descricao']}">
<meta name="theme-color" content="#0B0B0C">
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:title" content="{t['nome']} — Vestígio Oculto">
<meta property="og:description" content="{t['descricao']}">
<meta property="og:locale" content="{OG_LOCALE[idioma]}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{{{{ADSENSE}}}}
{{{{FONTES}}}}
<style>{{{{CSS}}}}</style>
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
</script>
</head>
<body>

<header class="topbar">
  <div class="wrap">
    <a class="marca" href="../index.html" aria-label="{L['inicio_aria']}">
      {{{{LOGO}}}}
      <span class="selo">{L['pilar']}</span>
    </a>
    <nav aria-label="{L['pilares_aria']}">
      <ul class="nav-pilares">
{nav_pilares}
        <li><a href="../sobre.html">{L['sobre']}</a></li>
        <li class="nav-canal"><a href="https://www.youtube.com/@VestigoOcultoBrasil" target="_blank" rel="noopener">YouTube</a></li>
      </ul>
    </nav>
  </div>
</header>

<main>
  <header class="dossie-capa">
    <div class="wrap">
      <span class="kicker"><a href="../index.html">{L['arquivo']}</a> · {L['pilar']} · {n_dossies(idioma, len(cartoes))}</span>
      <h1>{t['nome']}</h1>
    </div>
  </header>

  <div class="corpo tema-intro">
{intro}
  </div>

  <section class="wrap" id="dossies" aria-labelledby="dossies-titulo">
    <h2 class="tema-lista" id="dossies-titulo">{L['dossies_do_pilar'].format(n=len(cartoes))}</h2>
    <div class="quadros">
{chr(10).join(blocos)}
    </div>

    <nav class="relacionados" aria-label="{L['outros_pilares']}">
      <span class="mono">{L['outros_pilares']}</span>
      <ul>
{nav_outros}
      </ul>
    </nav>
  </section>
</main>

<footer class="rodape">
  <div class="wrap">
    <div>
      <a class="marca" href="../index.html" aria-label="{L['inicio_aria']}">{{{{LOGO}}}}</a>
      <p>{L['slogan']}</p>
    </div>
    <div>
      <span class="mono">{L['pilares_rotulo']}</span>
      <p>{pilares_texto(idioma)}</p>
    </div>
    <div>
      <span class="mono">{L['canal']}</span>
      <p><a class="canal-handle" href="https://www.youtube.com/@VestigoOcultoBrasil" target="_blank" rel="noopener">@VestigoOcultoBrasil</a></p>
    </div>
    <div class="creditos">
      <span class="mono">© 2026 Vestígio Oculto</span>
      <span class="mono"><a href="{{{{RAIZ}}}}sobre.html">{L['sobre']}</a> · <a href="{{{{RAIZ}}}}contato.html">{L['contato']}</a> · <a href="{{{{RAIZ}}}}privacidade.html">{L['privacidade']}</a></span>
      <span class="mono">{L['rodape_selo']}</span>
    </div>
  </div>
</footer>

{{{{CONSENTIMENTO}}}}

</body>
</html>
"""


def pilares_texto(idioma: str) -> str:
    """A linha "Pedra e Poeira · Descoberto Ontem · ..." do rodapé, em texto
    puro, como os templates a escrevem; ligar_pilares a transforma em links."""
    return " · ".join(T[idioma]["pilares"][k] for k in TEMAS)


def href_do_pilar(k: str, chave: str, idioma: str) -> str:
    """Para onde aponta uma menção ao pilar k na página `chave` do idioma:
    a página do pilar, se ela existe no idioma; senão, a seção do pilar na
    home do idioma."""
    slug = TEMAS[k]["slug"]
    if k in temas_do_idioma(idioma):
        return relativo(chave, f"temas/{slug}.html")
    return relativo(chave, "index.html") + f"#{slug}"


def ligar_pilares(html: str, destino: str, pilar_de: dict, idioma: str = "pt") -> str:
    """Liga toda menção de pilar à página do pilar.

    - rodapé: a linha "Pedra e Poeira · ..." (texto puro) vira links;
    - menu dos dossiês: index.html#<pilar> passa a apontar para temas/<pilar>.html;
    - home: o título de cada pilar na seção "Pilares" vira link;
    - dossiê: o "Leia também" ganha a linha do pilar dele.

    `destino` é a chave da página (sem o prefixo do idioma). Num idioma em que
    o pilar ainda não tem página, os links ficam na seção do pilar na home.
    """
    raiz = "../" if "/" in destino else ""
    nomes = T[idioma]["pilares"]
    com_pagina = temas_do_idioma(idioma)
    links = " · ".join(f'<a href="{href_do_pilar(k, destino, idioma)}">{nomes[k]}</a>' for k in TEMAS)
    html = html.replace(f"<p>{pilares_texto(idioma)}</p>", f"<p>{links}</p>")
    for k, t in TEMAS.items():
        if k in com_pagina:
            html = html.replace(f'href="{raiz}index.html#{t["slug"]}"',
                                f'href="{href_do_pilar(k, destino, idioma)}"')
        if destino == "index.html" and k in com_pagina:
            html, n = re.subn(
                rf'(<article class="pilar" id="{t["slug"]}">\s*<h3>){re.escape(nomes[k])}(</h3>)',
                rf'\1<a href="temas/{t["slug"]}.html">{nomes[k]}</a>\2', html)
            if n != 1:
                raise SystemExit(f"  ! {prefixo(idioma)}index: pilar {t['slug']} sem título para ligar")
    slug = destino.removeprefix("dossies/").removesuffix(".html")
    if destino.startswith("dossies/") and slug in pilar_de:
        k = pilar_de[slug]
        link = f'<a href="{href_do_pilar(k, destino, idioma)}">{nomes[k]}</a>'
        if k in com_pagina:
            n_pilar = sum(1 for v in pilar_de.values() if v == k)
            frase = T[idioma]["tema_link"].format(link=link, n=n_pilar)
        else:
            frase = T[idioma]["tema_link_sem_pagina"].format(link=link)
        linha = f'\n      <p class="tema-link">{frase}</p>'
        html, n = re.subn(r'(<nav class="relacionados"[^>]*>.*?</ul>)', lambda m: m.group(1) + linha,
                          html, count=1, flags=re.S)
        if n != 1:
            raise SystemExit(f"  ! {prefixo(idioma)}{destino}: sem Leia também para a linha do pilar")
    return html


SIZES_FIGURA = {
    # .figura.larga: min(94vw, 1000px); abaixo de 860 px, a coluna inteira
    "larga": "(max-width: 860px) calc(100vw - 2.5rem), (min-width: 1064px) 1000px, 94vw",
    # .figura.lado: 46% da coluna de 66ch em tela grande
    "lado": "(max-width: 860px) calc(100vw - 2.5rem), 340px",
}


def imagens_responsivas(html: str, destino: str) -> str:
    """Figuras dos dossiês ganham uma versão de 640 px no srcset.

    O PSI de 03/10/2026 (Göbekli Tepe, celular) apontava imagens de 1200 px
    exibidas a 369 px. A versão de 640 cobre o celular com folga para tela
    densa; em tela grande o navegador continua pegando o original. A lupa
    abre sempre o original (data-full), não a versão reduzida.

    Só JPEG fora de <picture> (os PNG de figura já têm WebP). A variante é
    gerada uma vez e regerada se o original mudar.
    """
    if not destino.startswith("dossies/"):
        return html
    from PIL import Image
    pasta = RAIZ / "assets" / "img"

    def troca(m):
        figura, classe = m.group(0), m.group(1)
        if "<picture" in figura or "srcset=" in figura:
            return figura
        img = re.search(r'<img src="\.\./assets/img/([^"]+\.jpg)"', figura)
        if not img:
            return figura
        nome = img.group(1)
        origem = pasta / nome
        if not origem.is_file():
            return figura
        variante = origem.with_name(f"{origem.stem}-640.jpg")
        if not variante.exists() or variante.stat().st_mtime < origem.stat().st_mtime:
            im = Image.open(origem)
            if im.width <= 760:
                return figura
            im = im.convert("RGB")
            im.resize((640, round(im.height * 640 / im.width)), Image.LANCZOS).save(
                variante, "JPEG", quality=80, progressive=True, optimize=True)
        largura = Image.open(origem).width
        tipo = "lado" if "lado" in classe.split() else "larga"
        attrs = (f' srcset="../assets/img/{variante.name} 640w, ../assets/img/{nome} {largura}w"'
                 f' sizes="{SIZES_FIGURA[tipo]}" data-full="../assets/img/{nome}"')
        return figura.replace(img.group(0), img.group(0) + attrs, 1)

    html = re.sub(r'<figure class="figura ([^"]*)">.*?</figure>', troca, html, flags=re.S)
    html = html.replace("img.src = origem.currentSrc || origem.src;",
                        "img.src = origem.dataset.full || origem.currentSrc || origem.src;")
    return html


ROBOTS_INDEXA = "index, follow, max-image-preview:large"


def meta_robots(html: str, destino: str) -> str:
    """Toda página indexável leva max-image-preview:large (Google Discover).
    A 404 continua noindex."""
    if destino == "404.html":
        return html
    if 'name="robots"' in html:
        html, n = re.subn(r'<meta name="robots" content="index, follow">',
                          f'<meta name="robots" content="{ROBOTS_INDEXA}">', html)
        if n != 1:
            raise SystemExit(f"  ! {destino}: meta robots inesperada")
        return html
    html, n = re.subn(r'(<link rel="canonical" href="[^"]*">\n)',
                      rf'\1<meta name="robots" content="{ROBOTS_INDEXA}">\n', html, count=1)
    if n != 1:
        raise SystemExit(f"  ! {destino}: sem canonical para pôr a meta robots ao lado")
    return html


def preload_do_lcp(html: str, destino: str) -> str:
    """A imagem do topo da home é o LCP. O preload com imagesrcset faz o
    navegador pedi-la junto com o HTML, antes de achar o <img> no corpo
    (o PSI de 03/10/2026 media 360 ms de atraso de carregamento)."""
    if destino != "index.html":
        return html
    img = re.search(r'<section class="hero-foto">\s*<img src="([^"]+)"\s*srcset="([^"]+)"\s*sizes="([^"]+)"', html)
    if not img:
        raise SystemExit("  ! index: imagem do topo não encontrada para o preload")
    tag = (f'<link rel="preload" as="image" href="{img.group(1)}" imagesrcset="{img.group(2)}" '
           f'imagesizes="{img.group(3)}" fetchpriority="high">\n')
    return html.replace("{{FONTES}}", tag + "{{FONTES}}", 1)


# ---------------------------------------------------------------- idiomas: montagem

def n_dossies(idioma: str, n: int) -> str:
    """"07 dossiês", "01 dossier"."""
    return T[idioma]["dossie_n1" if n == 1 else "dossies_n"].format(n=n)


def montar_home(html: str, idioma: str) -> str:
    """Home de um idioma que não o português: os cartões, os filtros e as
    contagens saem dos dossiês traduzidos, nunca escritos à mão."""
    L = T[idioma]
    cartoes = cartoes_da_home(idioma)
    n, n_pt = len(cartoes), len(cartoes_da_home())
    pilares = [k for k in TEMAS if any(p == k for p, _, _ in cartoes)]
    filtros = [f'        <button type="button" data-pilar="todos" aria-pressed="true">{L["todos"]}</button>']
    filtros += [f'        <button type="button" data-pilar="{k}">{L["pilares"][k]}</button>' for k in pilares]
    html = (html.replace("{{CARTOES}}", "\n\n".join("      " + b for _, _, b in cartoes))
                .replace("{{FILTROS}}", "\n".join(filtros))
                .replace("{{QTD}}", L["qtd"](n)).replace("{{N}}", f"{n:02d}")
                .replace("{{QTD_PT}}", L["qtd"](n_pt)).replace("{{N_PT}}", f"{n_pt:02d}"))
    for k in TEMAS:
        c = sum(1 for p, _, _ in cartoes if p == k)
        html = html.replace(f"{{{{CONTAGEM:{k}}}}}", n_dossies(idioma, c) if c else L["contagem_zero"])
    sobra = re.sub(r"\{\{(CSS|FONTES|LOGO|ADSENSE|CONSENTIMENTO|RAIZ|DOMINIO|NUM[^}]*)\}\}", "", html)
    if "{{" in sobra:
        raise SystemExit(f"  ! {idioma}/index.tpl.html: marcador sem resolver: "
                         + ", ".join(sorted(set(re.findall(r"\{\{[^}]+\}\}", sobra)))))
    return html


def cabecalho_de_idioma(html: str, chave: str, idioma: str, ativos: list, existe: dict) -> str:
    """hreflang de todas as versões da página (com x-default: inglês quando
    existe, senão português) e og:locale:alternate. A 404 não leva: é noindex."""
    if chave == "404.html":
        return html
    linhas = [f'<link rel="alternate" hreflang="{HREFLANG[x]}" href="{url_de(x, chave)}">'
              for x in ativos if chave in existe[x]]
    padrao = "en" if "en" in ativos and chave in existe["en"] else "pt"
    linhas.append(f'<link rel="alternate" hreflang="x-default" href="{url_de(padrao, chave)}">')
    html, n = re.subn(r'(<link rel="canonical" href="[^"]*">\n)',
                      lambda m: m.group(1) + "\n".join(linhas) + "\n", html, count=1)
    if n != 1:
        raise SystemExit(f"  ! {prefixo(idioma)}{chave}: sem canonical para pôr o hreflang ao lado")
    outros = [x for x in ativos if x != idioma and chave in existe[x]]
    if outros:
        alt = "".join(f'<meta property="og:locale:alternate" content="{OG_LOCALE[x]}">\n' for x in outros)
        html = re.sub(r'(<meta property="og:locale" content="[^"]*">\n)', lambda m: m.group(1) + alt,
                      html, count=1)
    return html


def seletor_de_idioma(html: str, chave: str, idioma: str, ativos: list, existe: dict) -> str:
    """PT · EN no cabeçalho, só com os idiomas ativos. Cada um leva à mesma
    página no outro idioma; se ela ainda não foi traduzida, à home dele (e o
    title avisa). Fica fora do menu porque o menu some no celular."""
    if len(ativos) < 2:
        return html
    de = prefixo(idioma) + chave
    itens = []
    for x in ativos:
        equivalente = chave in existe[x] and chave != "404.html"
        para = prefixo(x) + (chave if equivalente else "index.html")
        href = "/" + para if chave == "404.html" else relativo(de, para)
        extra = ' aria-current="true"' if x == idioma else ""
        if not equivalente and x != idioma and chave != "404.html":
            extra += f' title="{T[idioma]["sem_traducao"].format(idioma=T[x]["nome"])}"'
        itens.append(f'<a href="{href}" hreflang="{HREFLANG[x]}" lang="{HREFLANG[x]}" '
                     f'aria-label="{T[x]["nome"]}"{extra}>{T[x]["sigla"]}</a>')
    nav = (f'\n    <nav class="idiomas" aria-label="{T[idioma]["idioma_aria"]}">\n      '
           + "\n      ".join(itens) + "\n    </nav>")
    html, n = re.subn(r'(<header class="topbar">.*?)(\n  </div>\n</header>)',
                      lambda m: m.group(1) + nav + m.group(2), html, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"  ! {de}: cabeçalho fora do padrão para o seletor de idioma")
    return html


def ligar_ao_original(html: str, chave: str, idioma: str, existe: dict) -> str:
    """Numa tradução, link para página que ainda não existe no idioma vai para
    o original em português, com hreflang="pt-BR" e, nos cartões do "Leia
    também", o aviso "em português". Link para página que não existe em
    idioma nenhum para o build."""
    pasta_pg = posixpath.dirname(chave)
    sobe = "../" * (chave.count("/") + 1)
    quebrados = []

    def troca(m):
        abre, href, corpo = m.group(1), m.group(2), m.group(3)
        if re.match(r"^(?:[a-z]+:|#|/)", href):
            return m.group(0)
        caminho, _, frag = href.partition("#")
        if not caminho.endswith(".html"):
            return m.group(0)
        alvo = posixpath.normpath(posixpath.join(pasta_pg, caminho))
        if alvo.startswith("..") or alvo in existe[idioma]:
            return m.group(0)
        if alvo not in existe["pt"]:
            quebrados.append(href)
            return m.group(0)
        novo = sobe + alvo + (f"#{frag}" if frag else "")
        abre = abre.replace(f'href="{href}"', f'href="{novo}" hreflang="pt-BR"', 1)
        corpo = re.sub(r'(<span class="num">[^<]*)(</span>)',
                       lambda s: f'{s.group(1)} · {T[idioma]["em_portugues"]}{s.group(2)}', corpo, count=1)
        return abre + corpo + "</a>"

    html = re.sub(r'(<a\b[^>]*?\bhref="([^"]*)"[^>]*>)(.*?)</a>', troca, html, flags=re.S)
    if quebrados:
        raise SystemExit(f"  ! {prefixo(idioma)}{chave}: link para página inexistente: {sorted(set(quebrados))}")
    return html


def subir_recursos(html: str, idioma: str) -> str:
    """O template traduzido escreve os caminhos como o original (../assets/...).
    As imagens, as fontes e o favicon moram uma vez só, na raiz do site; aqui
    eles ganham o ../ a mais que a pasta do idioma pede."""
    if idioma == "pt":
        return html
    html = re.sub(r'(\b(?:href|src|data-full)=")((?:\.\./)*)(assets/|favicon\.svg)', r'\1../\2\3', html)
    return re.sub(r'(\b(?:srcset|imagesrcset)=")([^"]*)"',
                  lambda m: m.group(1) + re.sub(r'(^|,\s*)((?:\.\./)*)(assets/)', r'\1../\2\3',
                                                m.group(2)) + '"', html)


def desvio_do_404(html: str, ativos: list) -> str:
    """O servidor tem uma 404 só, a da raiz (português). Quem cai nela vindo de
    /en/... é levado à 404 do próprio idioma. O status 404 já foi servido."""
    outros = [x for x in ativos if x != "pt"]
    if not outros:
        return html
    js = ("<script>\nvar m = location.pathname.match(/^\\/(" + "|".join(outros) + ")\\//);\n"
          "if (m) location.replace('/' + m[1] + '/404.html');\n</script>\n")
    return html.replace("</body>", js + "</body>", 1)


def conferir_pagina(html: str, chave: str, idioma: str) -> None:
    """A página pronta declara o idioma e o endereço certos, e nada aponta
    mais para o domínio antigo."""
    destino = prefixo(idioma) + chave
    erros = []
    if f'<html lang="{HREFLANG[idioma]}">' not in html:
        erros.append(f"lang ≠ {HREFLANG[idioma]}")
    if chave != "404.html":
        url = url_de(idioma, chave)
        for padrao, nome in ((r'<link rel="canonical" href="([^"]*)">', "canonical"),
                             (r'<meta property="og:url" content="([^"]*)">', "og:url")):
            achou = re.search(padrao, html)
            if not achou or achou.group(1) != url:
                erros.append(f"{nome} {achou.group(1) if achou else None} ≠ {url}")
        loc = re.search(r'<meta property="og:locale" content="([^"]*)">', html)
        if not loc or loc.group(1) != OG_LOCALE[idioma]:
            erros.append(f"og:locale ≠ {OG_LOCALE[idioma]}")
    antigo = re.search(r"(vestigiooculto|arquiteturadoimpossivel|xadrezbelico)\.com\.br", html)
    if antigo:
        erros.append(f"ainda aponta para o domínio antigo {antigo.group(0)}")
    if erros:
        raise SystemExit(f"  ! {destino}: " + "; ".join(erros))


# ---------------------------------------------------------------- idiomas: conferência da tradução

def _visivel(html: str) -> str:
    """Texto que o leitor vê (e o que vai em alt, title, meta e JSON-LD)."""
    import html as _h
    html = re.sub(r"<style\b.*?</style>", " ", html, flags=re.S)
    ld = " ".join(re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
    html = re.sub(r"<script\b.*?</script>", " ", html, flags=re.S)
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    attrs = " ".join(re.findall(r'\b(?:alt|content|title|aria-label)="([^"]*)"', html))
    texto = re.sub(r"<[^>]+>", " ", html) + " " + attrs + " " + ld
    return _h.unescape(re.sub(r"\{\{[^}]*\}\}", " ", texto))


def _numeros(texto: str) -> set:
    """Números, com separador neutro: 7.000 (pt) e 7,000 (en) são o mesmo;
    5,5 e 5.5 também."""
    return {re.sub(r"[.,]", "|", n) for n in re.findall(r"\d+(?:[.,]\d+)*", texto)}


def _imagens(html: str) -> list:
    return [re.sub(r"^(\.\./)+", "", u) for u in
            re.findall(r'<(?:img|source)\b[^>]*?\b(?:src|srcset)="([^"\s]+)', html)]


def _licencas(html: str) -> list:
    achadas = re.findall(r"CC0|CC BY(?:-SA|-NC|-ND)*(?: \d\.\d)?|dom[ií]nio p[uú]blico|public[- ]domain",
                         _visivel(html), re.I)
    return [("PD" if "blic" in a.lower() else a.upper()) for a in achadas]


def _links_de_licenca(html: str) -> list:
    return re.findall(r'creativecommons\.org/(?:licenses|publicdomain)/[a-z-]+/[\d.]+', html)


def _creditos(html: str) -> list:
    return [re.sub(r"<[^>]+>", " ", c) for c in
            re.findall(r'<(?:span class="acervo-fonte"|p class="quadro-credito")>(.*?)</(?:span|p)>',
                       html, re.S)]


def _rotulos(html: str, idioma: str) -> tuple:
    rec, acv = map(re.escape, (T[idioma]["rotulo_recriacao"], T[idioma]["rotulo_acervo"]))
    return (len(re.findall(rf'<b>{rec}</b>|class="recriacao">{rec}<', html)),
            len(re.findall(rf'class="acervo(?:-linha)?">{acv}<', html)))


# TODO, FIXME e XXX só em caixa-alta: "todo" é palavra comum em espanhol.
BASTIDOR = re.compile(r"\b(TODO|FIXME|XXX)\b|(?i:\b(?:TRADUZIR|TROCA PRONTA|rascunho|bastidor)\b)|\[\?\]")
RESTO_DE_PORTUGUES = re.compile(r"\b(não|também|são|está|uma|pelo|pela|então|através|\w+ções?)\b", re.I)


def comparar_com_original(original: str, traducao: str, idioma: str, nome: str) -> list:
    """O que a tradução não pode mudar: números, imagens, licenças, créditos e
    a marcação de recriação. E não pode levar bastidor."""
    erros = []
    a, b = _numeros(_visivel(original)), _numeros(_visivel(traducao))
    if a - b:
        erros.append(f"número do original ausente na tradução: {sorted(a - b)}")
    if b - a:
        erros.append(f"número na tradução que não está no original: {sorted(b - a)}")
    if _imagens(original) != _imagens(traducao):
        erros.append("imagens diferentes do original (mesmos arquivos, na mesma ordem)")
    if _licencas(original) != _licencas(traducao):
        erros.append(f"licenças {_licencas(traducao)} ≠ original {_licencas(original)}")
    if _links_de_licenca(original) != _links_de_licenca(traducao):
        erros.append("links de licença diferentes do original")
    co, ct = _creditos(original), _creditos(traducao)
    if len(co) != len(ct):
        erros.append(f"{len(ct)} créditos de imagem; o original tem {len(co)}")
    else:
        for c_o, c_t in zip(co, ct):
            nomes = [w for w in re.findall(r"[^\W\d_][\w'’.\-]*", c_o)
                     if w[0].isupper() and w.rstrip(".") not in PALAVRAS_DE_CREDITO_PT
                     and w not in ("CC", "BY", "BY-SA", "SA")]
            eq = EQUIVALENTES_DE_CREDITO.get(idioma, {})
            faltam = [w for w in nomes if w not in c_t and not (eq.get(w) and eq[w] in c_t)]
            if faltam:
                erros.append(f"crédito sem {faltam}: {' '.join(c_t.split())[:80]}")
    if _rotulos(original, "pt") != _rotulos(traducao, idioma):
        erros.append(f"rótulos Recriação/Acervo {_rotulos(traducao, idioma)} "
                     f"≠ original {_rotulos(original, 'pt')}")
    achou = BASTIDOR.search(_visivel(traducao))
    if achou:
        erros.append(f"bastidor no texto: {achou.group(0)!r}")
    sem_leia = re.sub(r'<nav class="relacionados".*?</nav>', "", traducao, flags=re.S)
    resto = sorted(set(m.group(0) for m in RESTO_DE_PORTUGUES.finditer(_visivel(sem_leia))))
    if idioma == "es":
        # "está" e "pelo" também são espanhol
        resto = [w for w in resto if w.lower() not in ("está", "pelo")]
    if resto:
        print(f"  ? {nome}: palavras que parecem português (conferir): {resto[:8]}")
    return [f"{nome}: {e}" for e in erros]


def conferir_traducao(idioma: str) -> None:
    """Cada página traduzida contra o original; cada cartão contra o cartão
    da home em português. A home do idioma não entra: os números dela são
    as contagens do próprio idioma."""
    erros = []
    for chave, caminho in templates_do_idioma(idioma).items():
        if chave == "index.html":
            continue
        original = (SRC / caminho.name).read_text(encoding="utf-8")
        erros += comparar_com_original(original, caminho.read_text(encoding="utf-8"), idioma,
                                       f"{idioma}/{caminho.name}")
    pt = {s: b for _, s, b in cartoes_da_home()}
    for _, s, b in cartoes_da_home(idioma):
        erros += comparar_com_original(pt[s], b, idioma, f"{idioma}/cartoes/{s}.html")
    if erros:
        raise SystemExit("  ! tradução: " + "\n  ! tradução: ".join(erros))


def main() -> None:
    ativos = idiomas_ativos()
    print("  idiomas ativos:", ", ".join(ativos),
          "| inativos:", ", ".join(x for x in IDIOMAS if x not in ativos) or "nenhum")
    conferir_ordem_da_home()
    conferir_contagens_da_home()
    for idioma in ativos:
        conferir_relacionados(idioma)
        conferir_seo(idioma)
    pilar_de = pilar_do_dossie()
    for idioma in ativos[1:]:
        pilar_do_dossie(idioma)
        conferir_traducao(idioma)
    variantes_de_imagem()

    existe = {x: paginas_existentes(x) for x in ativos}
    paginas = []
    for idioma in ativos:
        paginas += [(idioma, c, p, None) for c, p in templates_do_idioma(idioma).items()]
        paginas += [(idioma, f"temas/{TEMAS[k]['slug']}.html", None, tema_template(k, idioma))
                    for k in temas_do_idioma(idioma)]

    for idioma, chave, caminho, pronto in paginas:
        template = caminho.relative_to(SRC).as_posix() if caminho else f"tema:{chave}"
        destino = prefixo(idioma) + chave
        html = pronto if pronto is not None else caminho.read_text(encoding="utf-8")
        raiz_rel = "../" * chave.count("/")      # raiz do idioma
        raiz_site = "../" * destino.count("/")   # raiz do site (assets, fontes)
        faltando = [m for m in ("{{CSS}}", "{{LOGO}}", "{{FONTES}}") if m not in html]
        if faltando:
            print(f"  ! {template}: marcador ausente {', '.join(faltando)}")
            continue

        # Os blocos "TROCA PRONTA" são anotação de trabalho: ficam no template,
        # nunca na página publicada. Sem isto, markup comentado iria para o ar.
        html = re.sub(r"[ \t]*<!--\s*TROCA PRONTA:.*?-->\n?", "", html, flags=re.S)
        html = marcadores_de_idioma(html, idioma)

        slug = Path(chave).stem
        if chave.startswith("dossies/") and slug in NUMERO:
            html = html.replace("{{PROXIMO}}", bloco_proximo(slug, idioma))
            if '"BreadcrumbList"' not in html:
                html = html.replace("</head>", breadcrumb(slug, idioma), 1)
        if chave == "index.html" and idioma != "pt":
            html = montar_home(html, idioma)
        html = imagem_de_compartilhamento(html, slug, template, idioma)
        html = resolver_numeros(html, slug)
        html = meta_robots(html, chave)
        html = preload_do_lcp(html, chave)
        html = imagens_responsivas(html, chave)
        html = ligar_pilares(html, chave, pilar_de, idioma)
        html = rodape_rever(html, template, idioma)
        html = cabecalho_de_idioma(html, chave, idioma, ativos, existe)
        html = seletor_de_idioma(html, chave, idioma, ativos, existe)
        if idioma != "pt":
            # os links de página escritos com {{RAIZ}} precisam estar resolvidos
            # para serem conferidos; recurso com {{RAIZ}} só entra depois (CSS,
            # fontes), e por isso não pode aparecer aqui
            if "{{RAIZ}}assets/" in html:
                raise SystemExit(f"  ! {template}: use ../assets/ no template, não {{{{RAIZ}}}}assets/")
            html = html.replace("{{RAIZ}}", raiz_rel)
            # o visor do Voynich é texto do dossiê: vai na versão do idioma
            # (_src/<idioma>/visor-voynich.html) e entra ANTES de subir os
            # caminhos, para as imagens dele ganharem o ../ da pasta
            visor = pasta(idioma) / "visor-voynich.html"
            if "{{VISOR}}" in html and not visor.is_file():
                raise SystemExit(f"  ! {template}: falta {visor.relative_to(RAIZ)}")
            if "{{VISOR}}" in html:
                html = html.replace("{{VISOR}}", visor.read_text(encoding="utf-8"))
            html = ligar_ao_original(html, chave, idioma, existe)
            html = subir_recursos(html, idioma)
        elif chave == "404.html":
            html = desvio_do_404(html, ativos)

        final = sem_comentarios(html
            .replace("{{CSS}}", CSS)
            .replace("{{FONTES}}", FONTES)
            .replace("{{LOGO}}", LOGO)
            .replace("{{DOMINIO}}", DOMINIO.rstrip("/"))
            .replace("{{VISOR}}", VISOR)
            .replace("{{ADSENSE}}", ADSENSE)
            .replace("{{CONSENTIMENTO}}", consentimento(idioma))
            .replace("{{RAIZ}}assets/", raiz_site + "assets/")
            .replace("{{RAIZ}}", raiz_rel))
        conferir_pagina(final, chave, idioma)
        saida = RAIZ / destino
        saida.parent.mkdir(parents=True, exist_ok=True)
        saida.write_text(final, encoding="utf-8")
        print(f"  ✓ {destino}  ({saida.stat().st_size / 1024:.1f} KB)")

    # Página que deixou de existir num idioma (tradução retirada, idioma
    # desligado) não pode ficar no ar com conteúdo velho.
    for idioma in IDIOMAS[1:]:
        pasta_saida = RAIZ / idioma
        if not pasta_saida.is_dir():
            continue
        validas = {RAIZ / (prefixo(idioma) + c) for c in existe.get(idioma, set())}
        for velho in pasta_saida.rglob("*.html"):
            if velho not in validas:
                velho.unlink()
                print(f"  ✓ removida (sem tradução): {velho.relative_to(RAIZ).as_posix()}")

    if FAVICON.exists():
        shutil.copyfile(FAVICON, RAIZ / "favicon.svg")
        print("  ✓ favicon.svg")

    # sitemap.xml e robots.txt: o Google precisa dos dois para rastrear bem.
    # São gerados a partir das páginas existentes, então nunca ficam
    # desatualizados. Cada URL com versão em outro idioma leva os alternates.
    datas = {}
    for idioma in ativos:
        for chave, caminho in templates_do_idioma(idioma).items():
            datas[(idioma, chave)] = data_modificacao(caminho)
        # página de pilar: a data mais recente entre os dossiês dela
        for k in temas_do_idioma(idioma):
            datas[(idioma, f"temas/{TEMAS[k]['slug']}.html")] = max(
                datas[(idioma, f"dossies/{s}.html")] for s, p in pilar_de.items() if p == k)
        datas[(idioma, "index.html")] = max(v for (x, _), v in datas.items() if x == idioma)
    urls = []
    ordem = list(PAGINAS.values()) + [f"temas/{t['slug']}.html" for t in TEMAS.values()]
    for idioma in ativos:
        for chave in ordem:
            if chave == "404.html" or chave not in existe[idioma]:
                continue  # página de erro não se indexa
            # a home responde na raiz do idioma; o Google prefere a forma canônica
            loc = url_de(idioma, chave)
            prioridade = "1.0" if chave == "index.html" else ("0.3" if chave == "privacidade.html" else "0.8")
            versoes = [x for x in ativos if chave in existe[x]]
            alternates = ""
            if len(versoes) > 1:
                padrao = "en" if "en" in versoes else "pt"
                alternates = "".join(
                    f'\n    <xhtml:link rel="alternate" hreflang="{h}" href="{url_de(x, chave)}"/>'
                    for h, x in [(HREFLANG[v], v) for v in versoes] + [("x-default", padrao)])
            urls.append(
                f"  <url>\n    <loc>{loc}</loc>\n"
                f"    <lastmod>{datas[(idioma, chave)]}</lastmod>\n"
                f"    <changefreq>monthly</changefreq>\n"
                f"    <priority>{prioridade}</priority>{alternates}\n  </url>")
    (RAIZ / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"'
        + (' xmlns:xhtml="http://www.w3.org/1999/xhtml"' if len(ativos) > 1 else "") + '>\n'
        + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
    print(f"  ✓ sitemap.xml  ({len(urls)} URLs)")

    (RAIZ / "robots.txt").write_text(
        "# Vestígio Oculto\n"
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /_src/\n\n"
        f"Sitemap: {DOMINIO.rstrip('/')}/sitemap.xml\n", encoding="utf-8")
    print("  ✓ robots.txt")

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
