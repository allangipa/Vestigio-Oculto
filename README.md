# Vestígio Oculto

Portal investigativo de enigmas antigos e contemporâneos. Site estático, sem
framework e sem build no servidor — o mesmo fluxo do viagemnalupa.com.br:
commit no GitHub, deploy na Hostinger.

---

## O que falta para entrar no ar

1. **Dizer qual é o domínio.** É a única coisa que trava a publicação. Abra
   `_src/build.py`, troque a linha `DOMINIO = "https://vestigiooculto.com.br"`
   pelo domínio real e rode o build. Ela alimenta `canonical`, `og:url`,
   `og:image` e o JSON-LD das duas páginas — é um lugar só.
2. **Criar o repositório e apontar a Hostinger para ele** (passo a passo
   abaixo).
3. **Gerar as seis imagens que faltam.** Prompts prontos em
   `_src/imagens/PROMPTS.md`, ≈ 9 créditos no total. Os quadros funcionam sem
   elas: aparecem com a tarja "imagem em produção".

Nada mais é bloqueio. O site já tem favicon, imagem de compartilhamento,
dados estruturados e passa em telas de 390 px a 1440 px sem estouro.

---

## Publicar na Hostinger

O painel tem deploy direto do GitHub (**Sites → seu site → Avançado → Git**).
O fluxo é o mesmo do outro site:

1. Crie o repositório e mande o projeto:

   ```bash
   git init
   git add .
   git commit -m "Vestígio Oculto — site inicial"
   git branch -M main
   git remote add origin git@github.com:SEU-USUARIO/vestigio-oculto.git
   git push -u origin main
   ```

2. No painel, conecte o repositório e defina a branch `main`.
3. O diretório publicado é a **raiz** do repositório: `index.html`,
   `dossies/`, `assets/` e `favicon.svg` ficam lá. `_src/` vai junto mas não é
   servido — são os arquivos de trabalho.
4. Depois do primeiro deploy, confira se o SSL está ativo e force HTTPS.

A cada alteração: edite em `_src/`, rode `python3 _src/build.py`, commite e
faça push.

---

## Estrutura

```
vestigio-oculto/
├── index.html                  ← home (gerado)
├── dossies/
│   └── gobekli-tepe.html       ← dossiê 001 (gerado)
├── favicon.svg                 ← símbolo da marca (gerado)
├── assets/img/                 ← fotos dos quadros e das figuras
├── README.md
└── _src/                       ← fonte; vai no repositório, não é servido
    ├── vestigio.css            ← sistema de design, arquivo único
    ├── index.tpl.html          ← template da home
    ├── gobekli-tepe.tpl.html   ← template do dossiê
    ├── marca/                  ← SVGs oficiais, sem os metadados C2PA
    ├── imagens/PROMPTS.md      ← prompts das imagens que faltam
    └── build.py                ← injeta CSS, marca e domínio nos templates
```

As páginas publicadas são **autocontidas**: todo o CSS e a marca vão embutidos
em cada arquivo. Só as fotos são requisições à parte.

### Como editar

Nunca edite `index.html` nem `dossies/*.html`: eles são gerados e qualquer
alteração se perde no próximo build.

```bash
python3 _src/build.py     # a partir da raiz do projeto
```

### Como criar um dossiê novo

1. Duplique `_src/gobekli-tepe.tpl.html` com o novo nome.
2. Mantenha `{{CSS}}`, `{{LOGO}}` e `{{DOMINIO}}` onde estão; troque título,
   meta tags, JSON-LD e conteúdo.
3. Registre o par no dicionário `PAGINAS`, em `_src/build.py`.
4. **Ponha o slug na lista `ARQUIVO`, na posição que ele ocupa na escada.**
5. Na home, troque o `href="#dossies"` do quadro pelo caminho real, mude
   `<span class="estado apuracao">Apuração</span>` para
   `<span class="estado publicado">Publicado</span>` e acrescente os chips de
   navegação, como no quadro 001.

### A numeração sai de um lugar só

O número do dossiê não se escreve à mão. O template pede `{{NUM}}` para o
próprio número e `{{NUM:slug}}` para citar outro, e os dois saem da lista
`ARQUIVO` em `_src/build.py` — que é também a ordem do arquivo.

A ordem segue a escada de "onde estava escondido", o mesmo fio do canal no
YouTube: terra, floresta, areia, cinzas, pedra, água, DNA, consenso, à vista
de todos, arquivo, zona de exclusão. Reordenar é editar essa lista; não há
nada para caçar nos templates.

Isso existe porque o número estava escrito à mão em 56 pontos, e os links
entre dossiês são por slug. Um número errado não quebrava link nenhum — só
mandava o leitor para o dossiê errado, em silêncio. Agora o build quebra se um
template citar slug fora da lista.

O `AUDITORIA.md` usa a numeração antiga de propósito, e tem a tabela de-para
no topo: ele é registro do que foi corrigido, não índice.

---

## Sistema de design

Alinhado à **Identidade Visual v1** do canal (`Identidade Visual/LEIA-ME.txt`).

| Token | Valor | Uso |
|---|---|---|
| `--carvao` | `#0B0B0C` | fundo de tudo |
| `--osso` | `#D9CBB3` | texto corrente, molduras |
| `--ambar` | `#C8862A` | acento único: destaques, marcadores, links |
| `--gelo` | `#F2F0EA` | títulos e números |
| `--carvao-2` / `--carvao-3` | `#121213` / `#191919` | cartões e hover |
| `--ambar-fundo` | `#8a5c1c` | âmbar rebaixado, para peso menor |

**Vermelho não entra**, e **âmbar é o único acento**: os quatro pilares se
distinguem por nome e posição, não por cor. Por isso o medidor de "peso de
evidência" não é semáforo — o comprimento da barra carrega o dado e o rótulo
o nomeia.

Tipografia: **Cinzel** nos títulos (a fonte da marca), **Inter** no corpo e na
interface, **JetBrains Mono** em coordenadas, datas e metadados.

### A marca

Vai **inline** nas páginas, em curvas, na versão **sólida** — no cabeçalho
aparece a 34 px, e a identidade manda usar sólido abaixo de 200 px. Os
arquivos em `_src/marca/` foram limpos de um bloco de metadados C2PA que valia
mais da metade do peso: o horizontal caiu de 16,5 KB para 6,4 KB.

Regras herdadas: não recolorir as lentes, não separar o chapéu dos óculos, não
aplicar contorno ou sombra, não esticar.

---

## Imagens

| Quadro | Arquivo | Origem |
|---|---|---|
| Hero | `001-gobekli-tepe-capa.jpg` | episódio 01, `03-colina-larga` |
| 001 Göbekli Tepe | `001-gobekli-tepe.jpg` | episódio 01, `07-escala-humana` |
| 002 Amazônia | `002-amazonia-lidar.jpg` | episódio 02, `a07-01` |
| 006 Grande Pirâmide | `006-grande-piramide.jpg` | episódio 01, `10-piramide` |
| 010 Denisovanos | `010-denisovanos.jpg` | episódio 01, `11-cacadores-v2` |
| 003, 004, 005, 007, 008, 009 | — | a gerar (`_src/imagens/PROMPTS.md`) |

Dentro do dossiê 001 há mais sete figuras, todas do episódio 01, intercaladas
no trecho que cada uma ilustra.

Todas passam por corte 16:9, 1200 px de largura e JPEG progressivo em
qualidade 82 — entre 100 e 230 KB cada.

**Toda imagem gerada leva a etiqueta "Recriação".** Um canal que se vende por
precisão histórica não pode deixar uma reconstituição passar por fotografia do
sítio; a etiqueta aparece no canto da foto e na legenda de cada figura.

---

## Microinterações

- **Tarja de confidencialidade**: metadados cobertos por uma barra sólida que
  some ao passar o cursor. Funciona por foco de teclado.
- **Figuras que abrem**: cada imagem do dossiê chega desfocada e revela ao
  entrar na tela — a mesma quebra de sigilo, aplicada ao material visual.
- **Lupa**: clique (ou Enter) em qualquer figura amplia sem sair da página.
  Fecha no Esc, no botão ou clicando fora.
- **Filtro por pilar** na home, sem recarregar.
- **Barra de progresso de leitura** no topo do dossiê.
- Tudo respeita `prefers-reduced-motion`.

---

## SEO

`<title>`, meta description, canonical, Open Graph com imagem 1200×630,
Twitter card e JSON-LD válido: `WebSite` na home, `Article` + `Place` com
`geo` no dossiê. Todos os endereços absolutos saem da constante `DOMINIO`.

---

## Licença de conteúdo

Textos integralmente autorais. As fontes consultadas ficam listadas ao fim de
cada dossiê, sem reprodução de trecho algum. Imagens de recriação sinalizadas.
