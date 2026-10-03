# Imagens do site — origem e crédito

Mesma lógica do `Material real/CREDITOS.md` dos episódios: cada arquivo tem
origem declarada, e a origem decide a etiqueta que aparece na tela.

## As duas etiquetas, e por que elas são diferentes

| Etiqueta | Cor | O que significa |
|---|---|---|
| **Recriação** | osso | a cena foi construída por geração de imagem. Não é registro do lugar. |
| **Acervo** | âmbar | o documento é aquele mesmo, fotografado de um original. |

Se as duas levassem o mesmo rótulo, a etiqueta perderia a função. Num canal
que se vende por precisão histórica, o leitor precisa saber, sem esforço, se
está vendo uma reconstituição ou a coisa.

## Acervo

| Arquivo | Origem | Onde entra |
|---|---|---|
| `011-sentinela-do-norte-real*.jpg` | Wikimedia Commons, *North Sentinel Island from flight.jpg*, PJeganathan, CC BY-SA 4.0 — recorte 16:9 | quadro 011 na home |
| `011-sentinela-voo.jpg` | o mesmo arquivo, inteiro | dossiê 011, seção 01 |
| `011-sentinela-satelite.jpg` | Wikimedia Commons, *North Sentinel Island.jpg*, NASA Earth Observatory (Jesse Allen, dados EO-1), domínio público | dossiê 011, seção 01 |
| `012-anticitera-real*.jpg` | Wikimedia Commons, *The Antikythera Mechanism (3209887483).jpg*, Tilemahos Efthimiadis (Flickr), CC BY 2.0 — recorte 16:9 da vitrine com os três maiores fragmentos, Museu Arqueológico Nacional de Atenas | quadro 012 na home |
| `ac-01-mykali-1901.jpg` | Wikimedia Commons, *Antikes Wrack von Antikythera 03.jpg*, fotografia de autor desconhecido, 1900–1901, domínio público — tamanho original (783 × 800), sem recorte | dossiê 012, abertura |
| `ac-02-fragmento-a.jpg` | Wikimedia Commons, *Antikythera Fragment A (Front).webp*, Logg Tandy, CC BY 4.0 — reduzido a 960 × 960, sem recorte | dossiê 012, seção 01 |
| `ac-04-fragmento-19.jpg` | Wikimedia Commons, *Antikythera Fragment 19 (Front).webp*, Logg Tandy, CC BY 4.0 — recortada a plaqueta numerada do museu, no pé | dossiê 012, seção 02 |
| `ac-05-modelo-verso.jpg` | Wikimedia Commons, *Antikythera mechanism frontview, 1st-2nd century BC, Greece (model).jpg*, Gts-tg, CC BY-SA 4.0 — recorte quadrado. **É réplica moderna** (Universidade Aristóteles de Tessalônica), por isso a legenda leva o rótulo **Modelo**, e não Acervo. O nome do arquivo no Commons diz "frontview", mas a foto mostra a face de trás, com as espirais do metônico e do saros | dossiê 012, seção 03 |
| `ac-03-fragmento-c.jpg` | Wikimedia Commons, *Antikythera Fragment C (Front).webp*, Logg Tandy, CC BY 4.0 — reduzido a 960 × 960, sem recorte | dossiê 012, seção 04 |
| `008-manuscrito-voynich.jpg` | Beinecke MS 408, Yale — recorte da folha dobrada | quadro 008 na home |
| `vy-004` `vy-025` `vy-080` | Beinecke MS 408 — seção botânica | visor de fólios |
| `vy-125` | Beinecke MS 408 — seção astronômica | visor de fólios |
| `vy-158` | Beinecke MS 408 — folha dobrada, nove diagramas | visor de fólios |
| `vy-163` | Beinecke MS 408 — seção farmacológica | visor de fólios |
| `vy-190` | Beinecke MS 408 — seção das receitas | visor de fólios |
| `vy-escrita.jpg` | Beinecke MS 408 — recorte fechado do fólio 190 | figura no dossiê 008 |

**Crédito na tela:** Beinecke Rare Book & Manuscript Library, Yale University
— MS 408. O manuscrito é do início do século XV, datado por carbono entre
1404 e 1438, e está em domínio público. Os arquivos vieram da digitalização
que a Beinecke disponibiliza abertamente, via Internet Archive.

**Fonte completa:** https://collections.library.yale.edu/catalog/2002046

## Recriação

Todas geradas para os episódios do canal, com `flux_2`. A pasta de origem
está em `Roteiros/<episódio>/Teste de video/imagens`.

| Arquivo | Episódio | Original |
|---|---|---|
| `001-gobekli-tepe-capa.jpg` | 01 | `03-colina-larga` |
| `001-gobekli-tepe.jpg` | 01 | `07-escala-humana` |
| `gt-01` a `gt-07` | 01 | levantamento, caderno, gazelas, relevo, javali pintado, crânios, entulho |
| `002-amazonia-lidar.jpg` | 02 | `a07-01` |
| `006-grande-piramide.jpg` | 01 | `10-piramide` |
| `010-denisovanos.jpg` | 01 | `11-cacadores-v2` |
| `am-01` a `am-08` | 02 | Orellana, lidar, Upano, estrada reta, cinza, geoglifo, terra preta, lâmina |

**Descartada:** `05-circulos-de-cima-v2`. Vista de cima, os pilares em T leem
como cruzes e o recinto vira cemitério cristão.

## Ainda sem imagem

Dossiês 003, 004, 005, 007 e 009. Prompts em `_src/imagens/PROMPTS.md`.

Busca no Storyblocks feita em 19/09/2026, e o resultado foi desigual:

| Termo | Resultados |
|---|---|
| serra da capivara | 0 |
| caatinga | 0 |
| nan madol | 0 |
| herculaneum | 290 |
| amazon rainforest aerial | 276 |

Ou seja, o banco cobre bem Herculano e serve de ambiente para o Fawcett; para
Serra da Capivara e Nan Madol não há nada, e essas duas continuam dependendo
de geração. O material do Storyblocks vem em verde saturado e céu azul, então
precisa da correção de cor da receita do canal antes de entrar ao lado das
imagens geradas.

## Tratamento padrão

Corte 16:9, 1200 px de largura, JPEG progressivo em qualidade 82 — entre 100 e
230 KB por arquivo. Os fólios do visor fogem à regra: preservam a proporção
original, limitados a 1400 × 980, porque cortar um documento histórico para
caber num quadro seria falsificá-lo.

## ⚠ Correção de atribuição — material do episódio 01

O clipe `gize-piramide-aereo-SBV-354940900.mp4`, catalogado em
`Material real/01 Gobekli Tepe/CREDITOS.md` como *"drone subindo pela face da
Grande Pirâmide"*, **não é a Grande Pirâmide**. O topo do monumento no clipe
conserva o revestimento liso de calcário — assinatura da pirâmide de Quéfren,
a segunda de Gizé. A de Quéops perdeu praticamente todo o revestimento, e o
que se vê nela são as fiadas do núcleo.

Consequência para o vídeo: no episódio 01 o clipe entra na comparação de
idade, onde a narração diz "Gizé" de forma genérica — ali não há erro. Mas ele
**não pode** entrar num trecho que nomeie a Grande Pirâmide, e a linha do
`CREDITOS.md` do episódio precisa ser corrigida.

Consequência para o site: por isso o quadro e a figura do dossiê 006 usam a
recriação, e não esse frame. Um substituto real está indicado em
`_src/imagens/COMMONS.md`.
