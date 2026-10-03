# Vestígio Oculto

Portal investigativo de enigmas antigos e contemporâneos, no ar em
**https://vestigiooculto.com** (português na raiz, inglês em `/en/`). Site estático, sem framework e sem build no
servidor: o build roda na máquina, o resultado vai para o GitHub e a Hostinger
publica a raiz do repositório.

**Estado em 03/10/2026:** 22 dossiês publicados (001 a 022), home, Sobre,
Contato, Política de privacidade e 404. AdSense ligado, com faixa de
consentimento. O que vem depois está em `PROXIMOS.md`.

---

## Publicar

O painel da Hostinger faz deploy direto do GitHub (**Sites → o site →
Avançado → Git**, branch `main`). O diretório publicado é a **raiz** do
repositório. `_src/`, os `.md` (em qualquer pasta) e `.git` não são servidos:
o `.htaccess` devolve 403.

A cada alteração:

```bash
PYTHONIOENCODING=utf-8 python _src/build.py   # a partir da raiz
git add -A && git commit -m "…" && git push
```

---

## Estrutura

```
Vestigio-Oculto/
├── index.html, sobre.html, contato.html,
│   privacidade.html, 404.html      ← páginas fixas (geradas)
├── dossies/*.html                  ← os 22 dossiês (gerados)
├── en/                             ← edição em inglês (gerada; mesmos nomes de arquivo)
├── favicon.svg, sitemap.xml,
│   robots.txt, ads.txt             ← gerados pelo build
├── assets/
│   ├── img/                        ← fotos e recriações; CREDITOS.md registra cada uma
│   └── fontes/                     ← woff2 hospedados (Cinzel, Inter, JetBrains Mono)
├── .htaccess                       ← domínios, HTTPS, cache, bloqueio de _src/ e de .md
├── README.md, PROXIMOS.md, AUDITORIA.md, BAIXAR*.md   ← notas de trabalho
└── _src/                           ← fonte; vai no repositório, não é servido
    ├── build.py                    ← gera tudo; ARQUIVO é a ordem dos dossiês
    ├── vestigio.css, fontes.css    ← sistema de design, embutido em cada página
    ├── *.tpl.html                  ← um template por página (português, o original)
    ├── idiomas.py                  ← idiomas ativos e textos que o build escreve
    ├── en/                         ← templates traduzidos + en/cartoes/<slug>.html
    ├── testa_htaccess.py           ← emulador dos redirecionamentos do .htaccess
    ├── consentimento.html          ← faixa de cookies + carga do AdSense
    ├── visor-voynich.html          ← visor de fólios do dossiê 009
    ├── marca/                      ← SVGs oficiais
    ├── imagens/                    ← levantamentos de acervo (TROCAS, COMMONS, SAARA)
    └── _entrada/                   ← rascunhos de cartão da home dos dossiês 013–022
```

As páginas publicadas são **autocontidas**: CSS e marca vão embutidos em cada
arquivo. Só fotos e fontes são requisições à parte.

**Nunca edite o HTML da raiz nem de `dossies/`**: é gerado, e qualquer
alteração se perde no próximo build. Edite o template e rode o build.

---

## O que o build faz (e o que ele recusa)

`_src/build.py` injeta CSS, fontes, marca, domínio, AdSense e consentimento
nos templates, gera as variantes de imagem do `srcset` da home e os `.webp`
dos PNG, escreve `sitemap.xml`, `robots.txt` e `ads.txt`, e **tira os
comentários HTML** da página publicada (comentário de template é anotação de
trabalho).

Ele **quebra** quando:

- um template cita um dossiê fora de `ARQUIVO` (`{{NUM:slug}}`);
- os cartões da home não seguem a ordem de `ARQUIVO`, ou falta o comentário
  de numeração de um cartão;
- os números da home (total, publicados, contador, contagem por pilar) não
  batem com os cartões;
- um "Leia também" chama um dossiê por título diferente do `<h1>` dele, ou
  repete o "próximo";
- um dossiê não tem exatamente um `{{PROXIMO}}`.

### A numeração e o "próximo" saem de um lugar só

O número do dossiê não se escreve à mão: o template pede `{{NUM}}` para o
próprio número e `{{NUM:slug}}` para citar outro, e os dois saem da lista
`ARQUIVO`. O link "próximo" também: cada dossiê tem `{{PROXIMO}}`, e o build
põe ali o número seguinte de `ARQUIVO` (o 022 volta ao 001) com o `<h1>` da
página de destino.

### Criar um dossiê novo

1. Duplique um template recente (ex.: `_src/korowai.tpl.html`).
2. Mantenha `{{CSS}}`, `{{LOGO}}`, `{{FONTES}}`, `{{ADSENSE}}`,
   `{{CONSENTIMENTO}}`, `{{DOMINIO}}` e `{{PROXIMO}}`; troque título, metas,
   JSON-LD e conteúdo.
3. Registre o par em `PAGINAS` e o slug em `ARQUIVO`, na posição dele.
4. Na home, acrescente o cartão com o comentário `<!-- NNN -->`, a etiqueta
   **Acervo** ou **Recriação**, a linha `quadro-credito` (autor · licença com
   link) se a foto for de terceiro, e atualize os números (o build confere).
5. Registre cada imagem nova em `assets/img/CREDITOS.md`.

---

## Domínios e redirecionamentos

O domínio principal é **https://vestigiooculto.com**, sem www (desde
03/10/2026). Na Hostinger, `vestigiooculto.com.br` e `concealedpast.com` estão
estacionados no mesmo site e servem os mesmos arquivos; quem decide para onde
vai cada pedido é o `.htaccess`, sempre com 301, mesmo caminho e query string:

| pedido | vai para |
|---|---|
| `vestigiooculto.com.br/x` e `www.vestigiooculto.com.br/x` | `https://vestigiooculto.com/x` |
| `www.vestigiooculto.com/x` | `https://vestigiooculto.com/x` |
| `http://vestigiooculto.com/x` | `https://vestigiooculto.com/x` |
| `concealedpast.com/` | `https://vestigiooculto.com/en/` |
| `concealedpast.com/dossies/x.html` | `https://vestigiooculto.com/en/dossies/x.html` |
| `concealedpast.com/en/x` | `https://vestigiooculto.com/en/x` (sem `/en/en/`) |
| `concealedpast.com/assets/…`, `/favicon.svg`, `/robots.txt`, `/sitemap.xml`, `/ads.txt` | mesmo caminho, sem `/en/` (existem uma vez só) |

Outros hosts (o domínio temporário da Hostinger) não são tocados. Para testar
sem servidor: `python _src/testa_htaccess.py .htaccess` (sai com erro se algum
caso não der o esperado). Depois de publicar, confira com
`curl -sI https://concealedpast.com/dossies/gobekli-tepe.html`. Os domínios
estacionados precisam de SSL ativo na Hostinger, senão o `https://` do
domínio antigo dá aviso antes de redirecionar.

Página do concealedpast que ainda não tem tradução cai na 404 da raiz, e a 404
leva quem veio de `/en/` para `/en/404.html`, que aponta a home em inglês.

`DOMINIO`, em `_src/build.py`, é o único lugar do domínio: canonical, og:url,
og:image, JSON-LD, hreflang, sitemap e robots saem dele. O build **para** se
alguma página ainda citar `vestigiooculto.com.br` (ou o `.com.br` dos sites
irmãos, que também passaram para `.com`).

---

## Idiomas

`IDIOMAS = ["pt", "en", "es"]` em `_src/idiomas.py`. **Português é o original
e fica na raiz, com os caminhos de sempre**; inglês sai em `/en/`, espanhol em
`/es/`, com os mesmos nomes de arquivo (`/en/dossies/gobekli-tepe.html`). Um
idioma fica **ativo** quando tem home traduzida e ao menos um dossiê; antes
disso o build o ignora. Hoje: pt e en ativos (en com um dossiê, Göbekli Tepe),
es inativo.

**Uma página só sai num idioma se a tradução existir.** Dois lugares:

- **Página escrita à mão** (dossiê, home, sobre, contato, privacidade, 404):
  template traduzido em `_src/<idioma>/<mesmo nome>.tpl.html`, com a mesma
  marcação do original. Caminhos de imagem iguais aos do original
  (`../assets/...`): o build acrescenta o `../` da pasta do idioma. Canonical
  e og:url com `{{BASE}}` (= domínio + `/en`); imagens com `{{DOMINIO}}`.
- **Texto que o build escreve** (o "próximo", a linha do pilar, a faixa de
  cookies, "Rever escolha de cookies", o seletor de idioma, os nomes e as
  páginas dos pilares, o alt da prévia de compartilhamento, o subtítulo da
  marca): dicionário por idioma em `_src/idiomas.py`.

### Traduzir um dossiê

1. Copie `_src/<slug>.tpl.html` para `_src/en/<slug>.tpl.html` e traduza o
   texto, os `alt`, as legendas, as metas e o JSON-LD (`inLanguage: "en"`,
   `articleSection` com o nome do pilar em inglês, `translationOfWork`
   apontando para o original). **Fiel, sem fato novo**: divergências,
   atribuições e ressalvas ficam como estão. Números ficam em algarismo onde
   o original usa algarismo (7.000 vira 7,000; 5,5 vira 5.5).
2. Rótulos das figuras: `Recriação` → `Re-creation`, `Acervo` → `Archive`.
   Créditos: mesmo autor e mesma licença; só "Foto" e nomes de instituição se
   traduzem.
3. "Leia também": se o destino já está traduzido, use o `<h1>` dele em
   inglês; se não, o `<h1>` original — o build manda o link para a página em
   português, com `hreflang="pt-BR"` e o aviso "in Portuguese".
4. Crie o cartão da home em `_src/en/cartoes/<slug>.html` (mesma imagem,
   mesmo crédito, link de licença em `deed.en`).
5. Acrescente o alt da prévia em `T["en"]["og_alt"]`, em `_src/idiomas.py`.
6. Rode o build.

O build **confere cada tradução contra o original** e para quando: falta na
tradução um número do original, ou aparece um que o original não tem
(separador de milhar e decimal não contam); as imagens não são as mesmas, na
mesma ordem; licenças, links de licença ou nomes dos créditos mudaram; o
número de rótulos Recriação/Acervo mudou; aparece bastidor (TODO, FIXME,
TRADUZIR, "[?]"…). Palavras que parecem português sobrando viram aviso. Vale
também por idioma: título até 60 e único, description de 120 a 155, `lang`,
canonical, og:url e og:locale certos.

A home do idioma (`_src/en/index.tpl.html`) não lista cartões à mão: o build
monta `{{CARTOES}}`, `{{FILTROS}}`, `{{QTD}}`, `{{N}}`, `{{QTD_PT}}`,
`{{N_PT}}` e `{{CONTAGEM:pilar}}` a partir dos dossiês traduzidos.

**Páginas de pilar** (`/en/temas/…`) só saem quando **todos** os dossiês do
pilar estão traduzidos, porque a introdução nomeia cada caso. Até lá, menu e
rodapé em inglês apontam para a seção do pilar na home em inglês. Os textos
dos quatro pilares em inglês já estão em `idiomas.py`.

**hreflang**: toda página indexável lista as versões existentes (pt-BR, en,
es) e `x-default` — inglês quando existe, senão português. O sitemap leva os
mesmos alternates. **Seletor de idioma** (PT · EN) no cabeçalho, visível
também no celular: leva à mesma página no outro idioma ou, se ela não foi
traduzida, à home dele.

**Pendente:** a prévia de compartilhamento (`assets/img/og/<slug>.jpg`) é a
mesma em todos os idiomas, com o título em português gravado na imagem. Em
Göbekli Tepe o título é o próprio nome, então não destoa; nos próximos
dossiês traduzidos vale gerar `og/en/<slug>.jpg` com o título em inglês.

**Espanhol:** para ativar, crie `_src/es/index.tpl.html`, as outras páginas
de interface e um dossiê; os textos curtos já estão em `T["es"]` (marca:
"Vestígio Oculto — Huellas ocultas del pasado"); faltam as introduções dos
pilares e o `og_alt`.

---

## Sistema de design

Alinhado à **Identidade Visual v1** do canal.

| Token | Valor | Uso |
|---|---|---|
| `--carvao` | `#0B0B0C` | fundo de tudo |
| `--osso` | `#D9CBB3` | texto corrente, molduras |
| `--osso-suave` | `#a79c8a` | texto secundário |
| `--osso-fraco` | `#847c6f` | metadados e legendas pequenas (4,8:1 sobre o carvão) |
| `--ambar` | `#C8862A` | acento único: destaques, marcadores, links |
| `--gelo` | `#F2F0EA` | títulos e números |
| `--carvao-2` / `--carvao-3` | `#121213` / `#191919` | cartões e hover |
| `--ambar-fundo` | `#8a5c1c` | âmbar rebaixado, para peso menor (não usar em texto) |

**Vermelho não entra**, e **âmbar é o único acento**. O medidor de "peso de
evidência" usa a escala Alto · Em disputa · Baixo · Nula · Minoritária.

Tipografia: **Cinzel** nos títulos, **Inter** no corpo, **JetBrains Mono** em
datas e metadados.

---

## Imagens

A regra de escolha está em `_src/imagens/TROCAS.md`: foto do objeto ou do
lugar, depois documento de época em domínio público, depois figura de artigo
em licença aberta, e só então recriação — sempre etiquetada.

- **Acervo** (âmbar): registro real. **Recriação** (osso): gerada. **Modelo**:
  réplica moderna. A etiqueta fica visível na própria imagem, inclusive no
  herói da home.
- Foto CC BY / CC BY-SA leva crédito na página: legenda nos dossiês, linha
  `quadro-credito` nos cartões da home. **CC BY-NC não entra.**
- `assets/img/CREDITOS.md` tem uma linha por imagem usada, com origem, autor,
  licença (e a base, quando é domínio público), modificação e onde entra.

---

## SEO e privacidade

`<title>`, meta description, canonical, Open Graph, Twitter card e JSON-LD
(`WebSite` na home, `Article` nos dossiês). Todos os endereços absolutos saem
de `DOMINIO`, em `_src/build.py`.

AdSense: `ADSENSE_LIGADO` liga e desliga tudo. `CONSENTIMENTO_BLOQUEIA = False`
(decisão do dono): o anúncio carrega na primeira visita enquanto a faixa está
na tela, e deixa de carregar depois de uma recusa. A Política de privacidade
descreve exatamente isso — se a constante mudar, mude o texto junto.

---

## Licença de conteúdo

Textos integralmente autorais. As fontes consultadas ficam listadas ao fim de
cada dossiê. Imagens de terceiros creditadas na página; recriações sinalizadas.
