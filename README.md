# Vestígio Oculto

Portal investigativo de enigmas antigos e contemporâneos, no ar em
**https://vestigiooculto.com.br**. Site estático, sem framework e sem build no
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
├── favicon.svg, sitemap.xml,
│   robots.txt, ads.txt             ← gerados pelo build
├── assets/
│   ├── img/                        ← fotos e recriações; CREDITOS.md registra cada uma
│   └── fontes/                     ← woff2 hospedados (Cinzel, Inter, JetBrains Mono)
├── .htaccess                       ← HTTPS, cache, bloqueio de _src/ e de .md
├── README.md, PROXIMOS.md, AUDITORIA.md, BAIXAR*.md   ← notas de trabalho
└── _src/                           ← fonte; vai no repositório, não é servido
    ├── build.py                    ← gera tudo; ARQUIVO é a ordem dos dossiês
    ├── vestigio.css, fontes.css    ← sistema de design, embutido em cada página
    ├── *.tpl.html                  ← um template por página
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
