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

import re
import shutil
from pathlib import Path

# ---------------------------------------------------------------
# TROQUE AQUI quando o domínio estiver definido. É o único lugar:
# canonical, og:url, og:image e JSON-LD saem todos daqui.
DOMINIO = "https://vestigiooculto.com.br"

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

CONSENTIMENTO = (SRC / "consentimento.html").read_text(encoding="utf-8")
CONSENTIMENTO = (CONSENTIMENTO
    .replace("{{ADSENSE_PUB}}", ADSENSE_PUB if ADSENSE_LIGADO else "")
    .replace("{{CONSENTIMENTO_BLOQUEIA}}", "true" if CONSENTIMENTO_BLOQUEIA else "false"))

if f"var CHAVE = '{CHAVE_CONSENTIMENTO}';" not in CONSENTIMENTO:
    raise SystemExit(f"  ! consentimento.html não usa a chave {CHAVE_CONSENTIMENTO}")

# "Rever escolha de cookies", no rodapé de toda página: apaga a escolha salva
# e recarrega, e a faixa volta a aparecer. O script vai junto do link, e não
# no bloco de consentimento, porque o 404 não leva a faixa.
REVER_LINK = ' · <a href="#" role="button" data-rever-cookies>Rever escolha de cookies</a>'
REVER_JS = ("\n<script>\ndocument.querySelectorAll('[data-rever-cookies]').forEach(function (a) {\n"
            "  a.addEventListener('click', function (ev) {\n    ev.preventDefault();\n"
            f"    try {{ localStorage.removeItem('{CHAVE_CONSENTIMENTO}'); }} catch (e) {{}}\n"
            "    location.reload();\n  });\n});\n</script>")


def rodape_rever(html: str, template: str) -> str:
    """Põe o link "Rever escolha de cookies" ao lado da política de privacidade
    do rodapé. Para se o rodapé não tiver esse link: página sem a revogação
    não sai."""
    if not ADSENSE_LIGADO:
        return html
    m = re.search(r"<footer\b.*?</footer>", html, flags=re.S)
    alvo = 'privacidade.html">Política de privacidade</a>'
    if not m or m.group(0).count(alvo) != 1:
        raise SystemExit(f"  ! {template}: rodapé sem o link da política de privacidade")
    rod = m.group(0).replace(alvo, alvo + REVER_LINK)
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


def imagem_de_compartilhamento(html: str, slug: str, template: str) -> str:
    """Aponta og:image, twitter:image e o "image" do JSON-LD para a prévia do
    dossiê, com 1200 x 630 e alt. Para se o arquivo apontado não existir."""
    if slug in OG_ALT:
        nome = f"og/{slug}.jpg"
        if not (RAIZ / "assets" / "img" / nome).is_file():
            raise SystemExit(f"  ! {slug}: prévia de compartilhamento ausente: assets/img/{nome}")
        url = f"{{{{DOMINIO}}}}/assets/img/{nome}"
        alt = OG_ALT[slug].replace('"', "&quot;")
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

def titulo_do_dossie(slug: str) -> str:
    """O <h1> do template, sem marcação. É o título que todo link usa."""
    html = (SRC / f"{slug}.tpl.html").read_text(encoding="utf-8")
    achou = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if not achou:
        raise SystemExit(f"  ! {slug}: template sem <h1>")
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", achou.group(1))).strip()


def proximo_de(slug: str) -> str:
    """O dossiê seguinte em ARQUIVO; o último volta ao primeiro."""
    i = ARQUIVO.index(slug)
    return ARQUIVO[(i + 1) % len(ARQUIVO)]


def bloco_proximo(slug: str) -> str:
    """O link "próximo" de cada dossiê, gerado — nunca escrito à mão.

    Até 03/10/2026 cada template trazia o próprio "próximo", e eles tinham
    virado um grafo arbitrário: dez dossiês não recebiam link de nenhum outro,
    e o mesmo dossiê aparecia com três títulos diferentes. Agora o próximo é
    sempre o número seguinte de ARQUIVO (o 022 volta ao 001), e o título é o
    <h1> da página de destino.
    """
    alvo = proximo_de(slug)
    return (
        f'<a class="proximo" href="{alvo}.html">\n'
        f'      <span>\n'
        f'        <span class="mono">Próximo no arquivo · Dossiê {NUMERO[alvo]}</span>\n'
        f'        <strong>{titulo_do_dossie(alvo)}</strong>\n'
        f'      </span>\n'
        f'      <span class="seta">→</span>\n'
        f'    </a>')


def conferir_relacionados() -> None:
    """O "Leia também" é escrito à mão; isto confere o que derrapa nele.

    Quebra o build quando um item cita o dossiê com título diferente do <h1>
    dele, ou quando repete o "próximo" — que já aparece logo abaixo.
    """
    erros = []
    for slug in ARQUIVO:
        html = (SRC / f"{slug}.tpl.html").read_text(encoding="utf-8")
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
            if re.sub(r"\s+", " ", titulo).strip() != titulo_do_dossie(alvo):
                erros.append(f"{slug}: Leia também chama {alvo} de \"{titulo}\"; "
                             f"o título é \"{titulo_do_dossie(alvo)}\"")
    if erros:
        raise SystemExit("  ! " + "\n  ! ".join(erros))


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


def meta_do_template(template: str) -> tuple:
    html = (SRC / template).read_text(encoding="utf-8")
    t = re.search(r"<title>(.*?)</title>", html, re.S)
    d = re.search(r'<meta name="description" content="([^"]*)"', html)
    return (t.group(1).strip() if t else ""), (d.group(1) if d else "")


def conferir_seo() -> None:
    """Porteiro de <title> e meta description, antes de gravar qualquer página.

    Em 03/10/2026 metade dos dossiês tinha título acima de 60 caracteres (o
    Google corta) e descrição de mais de 200 (idem). Regra: título até 60,
    único, assunto primeiro e a marca no fim; descrição de 120 a 155, única.
    A 404 não entra na conta da descrição (é noindex).
    """
    erros, vistos_t, vistos_d = [], {}, {}
    metas = [(tpl, *meta_do_template(tpl)) for tpl in PAGINAS]
    metas += [(f"temas/{v['slug']}", v["titulo"], v["descricao"]) for v in TEMAS.values()]
    for template, t, d in metas:
        if not t or len(t) > TITULO_MAX:
            erros.append(f"{template}: título com {len(t)} caracteres (máx. {TITULO_MAX})")
        if template != "404.tpl.html" and not DESCRICAO_MIN <= len(d) <= DESCRICAO_MAX:
            erros.append(f"{template}: descrição com {len(d)} caracteres "
                         f"({DESCRICAO_MIN}–{DESCRICAO_MAX})")
        if t in vistos_t:
            erros.append(f"{template}: título igual ao de {vistos_t[t]}")
        if d in vistos_d:
            erros.append(f"{template}: descrição igual à de {vistos_d[d]}")
        vistos_t[t], vistos_d[d] = template, template
    if erros:
        raise SystemExit("  ! SEO: " + "\n  ! SEO: ".join(erros))


def breadcrumb(slug: str) -> str:
    """BreadcrumbList do dossiê: Vestígio Oculto › título (o <h1>). Gerado."""
    import json
    dados = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Vestígio Oculto",
             "item": f"{DOMINIO.rstrip('/')}/"},
            {"@type": "ListItem", "position": 2, "name": titulo_do_dossie(slug),
             "item": f"{DOMINIO.rstrip('/')}/dossies/{slug}.html"},
        ],
    }
    return ('<script type="application/ld+json">\n'
            + json.dumps(dados, ensure_ascii=False, indent=2) + "\n</script>\n</head>")


def data_modificacao(template: str) -> str:
    """lastmod do sitemap. Dossiê: o dateModified do próprio JSON-LD, que é a
    data editorial. Outras páginas: o último commit do template, ou hoje se
    ele tem mudança ainda não publicada. A home leva a mais recente de todas.
    """
    import subprocess
    from datetime import date
    html = (SRC / template).read_text(encoding="utf-8")
    achou = re.search(r'"dateModified":\s*"(\d{4}-\d{2}-\d{2})"', html)
    if achou:
        return achou.group(1)
    try:
        sujo = subprocess.run(["git", "status", "--porcelain", "--", f"_src/{template}"],
                              cwd=RAIZ, capture_output=True, text=True).stdout.strip()
        if not sujo:
            data = subprocess.run(["git", "log", "-1", "--format=%cs", "--", f"_src/{template}"],
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


def cartoes_da_home() -> list:
    """(pilar, slug, html do cartão) na ordem da home."""
    html = (SRC / "index.tpl.html").read_text(encoding="utf-8")
    saida = []
    for bloco in re.findall(r'<article class="quadro".*?</article>', html, re.S):
        pilar = re.search(r'data-pilar="([a-z]+)"', bloco).group(1)
        slug = re.search(r'dossies/([a-z0-9-]+)\.html', bloco).group(1)
        saida.append((pilar, slug, bloco))
    return saida


def pilar_do_dossie() -> dict:
    """slug do dossiê -> chave do pilar. Para se o articleSection divergir."""
    mapa, erros = {}, []
    for pilar, slug, _ in cartoes_da_home():
        mapa[slug] = pilar
        tpl = (SRC / f"{slug}.tpl.html").read_text(encoding="utf-8")
        sec = re.search(r'"articleSection":\s*"([^"]+)"', tpl)
        if not sec or sec.group(1) != TEMAS[pilar]["nome"]:
            erros.append(f"{slug}: articleSection {sec.group(1) if sec else None!r} "
                         f"≠ pilar da home {TEMAS[pilar]['nome']!r}")
    faltam = [s for s in ARQUIVO if s not in mapa]
    if faltam:
        erros.append(f"dossiês sem pilar na home: {faltam}")
    if erros:
        raise SystemExit("  ! pilares: " + "\n  ! pilares: ".join(erros))
    return mapa


def tema_template(chave: str) -> str:
    """Monta, em memória, o template da página do pilar. Ela passa depois pelo
    mesmo caminho das outras páginas (CSS, logo, consentimento, rodapé)."""
    import json
    t = TEMAS[chave]
    dom = DOMINIO.rstrip("/")
    url = f"{dom}/temas/{t['slug']}.html"
    cartoes = [(s, b) for p, s, b in cartoes_da_home() if p == chave]
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
    outros = [TEMAS[k] for k in TEMAS if k != chave]
    og = f"{dom}/assets/img/og/{cartoes[0][0]}.jpg"
    ld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": t["titulo"].split(" · ")[0],
        "description": t["descricao"],
        "url": url,
        "inLanguage": "pt-BR",
        "image": og,
        "isPartOf": {"@type": "WebSite", "name": "Vestígio Oculto", "url": f"{dom}/"},
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Vestígio Oculto", "item": f"{dom}/"},
                {"@type": "ListItem", "position": 2, "name": t["nome"], "item": url},
            ],
        },
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(cartoes),
            "itemListElement": [
                {"@type": "ListItem", "position": i, "name": titulo_do_dossie(s),
                 "url": f"{dom}/dossies/{s}.html"}
                for i, (s, _) in enumerate(cartoes, start=1)],
        },
    }
    intro = "\n\n".join(f"    <p>{p}</p>" for p in t["intro"])
    nav_outros = "\n".join(
        f'        <li><a href="{o["slug"]}.html">\n'
        f'          <span class="num">Pilar</span>\n'
        f'          <strong>{o["nome"]}</strong>\n'
        f'        </a></li>' for o in outros)
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
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
<meta property="og:locale" content="pt_BR">
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
    <a class="marca" href="../index.html" aria-label="Vestígio Oculto — início">
      {{{{LOGO}}}}
      <span class="selo">Pilar</span>
    </a>
    <nav aria-label="Pilares editoriais">
      <ul class="nav-pilares">
        <li><a href="pedra-e-poeira.html">Pedra e Poeira</a></li>
        <li><a href="descoberto-ontem.html">Descoberto Ontem</a></li>
        <li><a href="arquivo-selado.html">Arquivo Selado</a></li>
        <li><a href="ultimos-isolados.html">Últimos Isolados</a></li>
        <li><a href="../sobre.html">Sobre</a></li>
        <li class="nav-canal"><a href="https://www.youtube.com/@VestigoOcultoBrasil" target="_blank" rel="noopener">YouTube</a></li>
      </ul>
    </nav>
  </div>
</header>

<main>
  <header class="dossie-capa">
    <div class="wrap">
      <span class="kicker"><a href="../index.html">Arquivo</a> · Pilar · {len(cartoes):02d} dossiês</span>
      <h1>{t['nome']}</h1>
    </div>
  </header>

  <div class="corpo tema-intro">
{intro}
  </div>

  <section class="wrap" id="dossies" aria-labelledby="dossies-titulo">
    <h2 class="tema-lista" id="dossies-titulo">Os {len(cartoes)} dossiês do pilar</h2>
    <div class="quadros">
{chr(10).join(blocos)}
    </div>

    <nav class="relacionados" aria-label="Outros pilares">
      <span class="mono">Outros pilares</span>
      <ul>
{nav_outros}
      </ul>
    </nav>
  </section>
</main>

<footer class="rodape">
  <div class="wrap">
    <div>
      <a class="marca" href="../index.html" aria-label="Vestígio Oculto — início">{{{{LOGO}}}}</a>
      <p>Um arquivo aberto sobre o que a história começou e não terminou de contar.</p>
    </div>
    <div>
      <span class="mono">Pilares</span>
      <p>Pedra e Poeira · Descoberto Ontem · Arquivo Selado · Últimos Isolados</p>
    </div>
    <div>
      <span class="mono">Canal</span>
      <p><a class="canal-handle" href="https://www.youtube.com/@VestigoOcultoBrasil" target="_blank" rel="noopener">@VestigoOcultoBrasil</a></p>
    </div>
    <div class="creditos">
      <span class="mono">© 2026 Vestígio Oculto</span>
      <span class="mono"><a href="{{{{RAIZ}}}}sobre.html">Sobre</a> · <a href="{{{{RAIZ}}}}contato.html">Contato</a> · <a href="{{{{RAIZ}}}}privacidade.html">Política de privacidade</a></span>
      <span class="mono">Textos autorais · imagens de recriação sinalizadas</span>
    </div>
  </div>
</footer>

{{{{CONSENTIMENTO}}}}

</body>
</html>
"""


PILARES_TEXTO = "Pedra e Poeira · Descoberto Ontem · Arquivo Selado · Últimos Isolados"


def ligar_pilares(html: str, destino: str, pilar_de: dict) -> str:
    """Liga toda menção de pilar à página do pilar.

    - rodapé: a linha "Pedra e Poeira · ..." (texto puro) vira links;
    - menu dos dossiês: index.html#<pilar> passa a apontar para temas/<pilar>.html;
    - home: o título de cada pilar na seção "Pilares" vira link;
    - dossiê: o "Leia também" ganha a linha do pilar dele.
    """
    raiz = "../" if "/" in destino else ""
    em_temas = destino.startswith("temas/")
    base = "" if em_temas else f"{raiz}temas/"
    links = " · ".join(f'<a href="{base}{t["slug"]}.html">{t["nome"]}</a>' for t in TEMAS.values())
    html = html.replace(f"<p>{PILARES_TEXTO}</p>", f"<p>{links}</p>")
    for t in TEMAS.values():
        html = html.replace(f'href="{raiz}index.html#{t["slug"]}"', f'href="{base}{t["slug"]}.html"')
        if destino == "index.html":
            html, n = re.subn(
                rf'(<article class="pilar" id="{t["slug"]}">\s*<h3>){re.escape(t["nome"])}(</h3>)',
                rf'\1<a href="temas/{t["slug"]}.html">{t["nome"]}</a>\2', html)
            if n != 1:
                raise SystemExit(f"  ! index.tpl.html: pilar {t['slug']} sem título para ligar")
    slug = destino.removeprefix("dossies/").removesuffix(".html")
    if destino.startswith("dossies/") and slug in pilar_de:
        t = TEMAS[pilar_de[slug]]
        n_pilar = sum(1 for v in pilar_de.values() if v == pilar_de[slug])
        linha = (f'\n      <p class="tema-link">Este dossiê é do pilar '
                 f'<a href="../temas/{t["slug"]}.html">{t["nome"]}</a> — '
                 f'veja os {n_pilar} dossiês dele.</p>')
        html, n = re.subn(r'(<nav class="relacionados"[^>]*>.*?</ul>)', lambda m: m.group(1) + linha,
                          html, count=1, flags=re.S)
        if n != 1:
            raise SystemExit(f"  ! {destino}: sem Leia também para a linha do pilar")
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


def main() -> None:
    conferir_ordem_da_home()
    conferir_contagens_da_home()
    conferir_relacionados()
    conferir_seo()
    pilar_de = pilar_do_dossie()
    variantes_de_imagem()

    paginas = [(t, d, None) for t, d in PAGINAS.items()]
    paginas += [(f"tema:{k}", f"temas/{t['slug']}.html", tema_template(k)) for k, t in TEMAS.items()]

    for template, destino, pronto in paginas:
        origem = SRC / template
        if pronto is None and not origem.exists():
            print(f"  ! template ausente: {template}")
            continue

        html = pronto if pronto is not None else origem.read_text(encoding="utf-8")
        raiz_rel = "../" if "/" in destino else ""
        faltando = [m for m in ("{{CSS}}", "{{LOGO}}", "{{FONTES}}") if m not in html]
        if faltando:
            print(f"  ! {template}: marcador ausente {', '.join(faltando)}")
            continue

        # Os blocos "TROCA PRONTA" são anotação de trabalho: ficam no template,
        # nunca na página publicada. Sem isto, markup comentado iria para o ar.
        html = re.sub(r"[ \t]*<!--\s*TROCA PRONTA:.*?-->\n?", "", html, flags=re.S)

        slug = template.replace(".tpl.html", "")
        if slug in NUMERO:
            html = html.replace("{{PROXIMO}}", bloco_proximo(slug))
            if '"BreadcrumbList"' not in html:
                html = html.replace("</head>", breadcrumb(slug), 1)
        html = imagem_de_compartilhamento(html, slug, template)
        html = resolver_numeros(html, slug)
        html = meta_robots(html, destino)
        html = preload_do_lcp(html, destino)
        html = imagens_responsivas(html, destino)
        html = ligar_pilares(html, destino, pilar_de)
        html = rodape_rever(html, template)

        saida = RAIZ / destino
        saida.parent.mkdir(parents=True, exist_ok=True)
        saida.write_text(
            sem_comentarios(html
                .replace("{{CSS}}", CSS)
                .replace("{{FONTES}}", FONTES)
                .replace("{{LOGO}}", LOGO)
                .replace("{{DOMINIO}}", DOMINIO.rstrip("/"))
                .replace("{{VISOR}}", VISOR)
                .replace("{{ADSENSE}}", ADSENSE)
                .replace("{{CONSENTIMENTO}}", CONSENTIMENTO.replace("{{RAIZ}}", raiz_rel))
                .replace("{{RAIZ}}", raiz_rel)),
            encoding="utf-8",
        )
        print(f"  ✓ {destino}  ({saida.stat().st_size / 1024:.1f} KB)")

    if FAVICON.exists():
        shutil.copyfile(FAVICON, RAIZ / "favicon.svg")
        print("  ✓ favicon.svg")

    # sitemap.xml e robots.txt: o Google precisa dos dois para rastrear bem.
    # São gerados a partir de PAGINAS, então nunca ficam desatualizados.
    datas = {d: data_modificacao(t) for t, d in PAGINAS.items()}
    # página de pilar: a data mais recente entre os dossiês dela
    for k, t in TEMAS.items():
        datas[f"temas/{t['slug']}.html"] = max(
            datas[f"dossies/{s}.html"] for s, p in pilar_de.items() if p == k)
    datas["index.html"] = max(datas.values())
    urls = []
    for destino in list(PAGINAS.values()) + [f"temas/{t['slug']}.html" for t in TEMAS.values()]:
        if destino == "404.html":
            continue  # página de erro não se indexa
        loc = f"{DOMINIO.rstrip('/')}/{destino}"
        # a home responde na raiz; o Google prefere a forma canônica
        if destino == "index.html":
            loc = DOMINIO.rstrip("/") + "/"
        prioridade = "1.0" if destino == "index.html" else ("0.3" if destino == "privacidade.html" else "0.8")
        urls.append(
            f"  <url>\n    <loc>{loc}</loc>\n"
            f"    <lastmod>{datas[destino]}</lastmod>\n"
            f"    <changefreq>monthly</changefreq>\n"
            f"    <priority>{prioridade}</priority>\n  </url>")
    (RAIZ / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
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
