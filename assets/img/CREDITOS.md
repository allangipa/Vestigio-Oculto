# Imagens do site — origem e crédito

Uma linha para **cada imagem que alguma página publicada usa** (conferido por
script contra o HTML gerado em 03/10/2026: 114 arquivos de base, mais as 22 prévias de `og/`, fora as
variantes `-640`, `-800`, `-960`, `-1280` e os `.webp`, que herdam a linha do
original). A origem decide a etiqueta que aparece na tela.

Este arquivo não é público: o `.htaccess` bloqueia `.md` em qualquer pasta.

## As etiquetas

| Etiqueta | O que significa |
|---|---|
| **Acervo** | o documento, o lugar ou o objeto é aquele mesmo, fotografado de um original. |
| **Recriação** | a cena foi construída por geração de imagem. Não é registro do lugar. |
| **Modelo** | réplica moderna fotografada (012 e 014). |

Num site que se vende por precisão histórica, o leitor precisa saber, sem
esforço, se está vendo uma reconstituição ou a coisa.

## Regras de crédito

- **CC BY e CC BY-SA**: o crédito vai na própria página, junto da imagem —
  legenda (`acervo-fonte`) nos dossiês e a linha `quadro-credito` em cada
  quadro da home (autor · licença com link · indicação de recorte).
- **CC BY-NC não entra** (canal e site são monetizados). Etiqueta de quem
  subiu o arquivo no Commons não vale mais que a licença de origem: o material
  do Vesuvius Challenge é NC na fonte, mesmo quando o Commons diz BY-SA.
- **Domínio público**: a coluna "licença" diz a base (idade, governo dos EUA,
  documento oficial, dedicação do autor), porque "domínio público" sozinho
  não é base.
- **Nome do arquivo ≠ número do dossiê.** Vários arquivos guardam a numeração
  anterior à renumeração de 20/09/2026 (`006-grande-piramide-real` é o quadro
  005, `008-manuscrito-voynich` é o 009, `009-nan-madol-real` é o 006,
  `010-denisovanos-real` é o 007, `003-serra-da-capivara-real` é o 008,
  `007-fawcett-real` é o 010). A coluna "onde entra" usa a numeração atual.

## Home e compartilhamento

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `001-gobekli-tepe-capa.jpg` | gerada para o episódio 01 (`03-colina-larga`), `flux_2` | arte do canal | — | recorte 16:9 | herói da home, com etiqueta **Recriação** visível |
| `og-vestigio-oculto.jpg` | a mesma recriação da colina, com a marca | arte do canal | — | escurecida, texto sobreposto | imagem de compartilhamento (`og:image`) da home, de `sobre`, `contato` e `privacidade`; reserva do `build.py` para dossiê sem prévia própria |

### Prévias dos dossiês (`assets/img/og/<slug>.jpg`)

Desde 03/10/2026 cada dossiê tem a sua imagem de compartilhamento
(`og:image`, `twitter:image` e `image` do JSON-LD), 1200 × 630, gerada a
partir de uma imagem **real** já usada no próprio dossiê. O `build.py` aponta
por slug (dicionário `OG_ALT`, que também é o `og:image:alt`) e para se o
arquivo faltar. **Modificação em todas:** recortada (ou encaixada à direita
sobre fundo carvão, quando o original é vertical ou quadrado), escurecida, com
degradê de carvão e título do dossiê e a marca sobrepostos. A atribuição de
cada uma é a da imagem-base. Nenhuma usa recriação.

| Arquivo | Deriva de | Autor | Licença | Modificação específica |
|---|---|---|---|---|
| `og/gobekli-tepe.jpg` | `001-gobekli-tepe-real.jpg` (*Archäologiepark Göbekli Tepe.jpg*) | Philrock | CC BY-SA 4.0 | — |
| `og/amazonia-lidar.jpg` | `am-02-lidar-real.png`, painel b (Pärssinen et al., *Nature*, 2026, fig. 2) | Pärssinen et al. | CC BY 4.0 | só o painel b, ampliado, à direita |
| `og/nadadores-do-saara.jpg` | `saara-nadador.jpg` (*WadiSuraSingleSwimmer.jpg*) | Roland Unger | CC BY-SA 3.0 | ampliada 1,5× |
| `og/papiros-herculano.jpg` | `hc-01-rolo-real.jpg`, painel a (Stabile et al., *Sci. Rep.* 11, 2021) | Sara Stabile et al. | CC BY 4.0 | só o rolo do painel a; fundo branco da figura trocado por carvão |
| `og/grande-piramide.jpg` | `006-grande-piramide-real.jpg` | Gary Todd | CC0 | — |
| `og/nan-madol.jpg` | `009-nan-madol-real.jpg` | NOAA | domínio público (PD-USGov-NOAA) | — |
| `og/denisovanos.jpg` | `010-denisovanos-real.jpg` | Александр Байдуков | CC BY-SA 4.0 | — |
| `og/serra-da-capivara.jpg` | `003-serra-da-capivara-real.jpg` | Mateus S. Figueiredo | CC BY-SA 4.0 | — |
| `og/manuscrito-voynich.jpg` | `008-manuscrito-voynich.jpg` (Beinecke MS 408) | Beinecke Rare Book & Manuscript Library | domínio público | substitui o uso direto do `008-…` como `og:image` |
| `og/percy-fawcett.jpg` | `fw-01-retrato-real.jpg` (*PercyFawcett.jpg*, 1911) | autor desconhecido | domínio público (PD-old) | à direita, sobre carvão |
| `og/sentinela-do-norte.jpg` | `011-sentinela-voo.jpg` (*North Sentinel Island from flight.jpg*) | PJeganathan | CC BY-SA 4.0 | — (ilha vista do avião; nenhuma pessoa) |
| `og/anticitera.jpg` | `ac-05-modelo-verso.jpg` (*Antikythera mechanism frontview… (model).jpg* — réplica da Universidade Aristóteles de Tessalônica) | Gts-tg | CC BY-SA 4.0 | à direita, sobre carvão, escurecida um pouco mais; réplica de propósito, para a prévia não usar peça do Museu de Atenas (ver "Riscos registrados") |
| `og/linhas-de-nazca.jpg` | `nz-01-colibri.jpg` | Diego Delso | CC BY-SA 4.0 | — |
| `og/puma-punku.jpg` | `pp-02-blocos-h.jpg` (*LAS H DE PUMA PUNKU.jpg*) | Keyan Alejandro | CC BY 4.0 | — |
| `og/moais-rapa-nui.jpg` | `015-moais-rapa-nui-real.jpg` | TravelingOtter | CC BY 2.0 | — |
| `og/anomalia-do-baltico.jpg` | `016-anomalia-do-baltico-real.jpg` | MODIS Land Rapid Response Team, NASA/GSFC | domínio público (NASA) | — |
| `og/dna-fantasma.jpg` | `017-dna-fantasma-real.jpg` | Scotted400 | CC BY 3.0 | — |
| `og/passagem-dyatlov.jpg` | `dy-01-vale-auspiya.jpg` (*Ауспия 2015.JPG*) | Futball80 | CC BY-SA 4.0 | — |
| `og/colonia-roanoke.jpg` | `019-colonia-roanoke-real.jpg` (de Bry, 1590) | Theodor de Bry segundo John White | domínio público | — |
| `og/kryptos.jpg` | `kr-01-escultura.jpg` (*Kryptos sculptor.jpg*) | Jim Sanborn | CC BY-SA 3.0 | à direita, sobre carvão, ampliada 1,23× |
| `og/mashco-piro.jpg` | `mp-01-rio-las-piedras.jpg` | Julio Araújo Flores e Patrick Champagne (ARCAmazon) | CC BY-SA 4.0 | — (paisagem; nenhuma pessoa) |
| `og/korowai.jpg` | `ko-02-casa-alta.jpg` ("Korowai Treehouse 2") | usuário do Flickr "♪ ~ from Jayapura, Indonesia" | CC BY 2.0 | — (casa em silhueta; nenhuma pessoa) |

Os quadros da home usam as imagens de abertura dos dossiês; cada linha abaixo
diz "quadro NNN" quando o arquivo aparece lá.

## 001 · Göbekli Tepe

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `001-gobekli-tepe-real.jpg` | Commons, *Archäologiepark Göbekli Tepe.jpg* | Philrock | CC BY-SA 4.0 | reduzida, recorte | quadro 001; dossiê, seção 02 |
| `gt-01-levantamento-1963.jpg` | gerada para o episódio 01, `flux_2` | arte do canal | — | — | dossiê, **Recriação** (as fotos do levantamento são do DAI e não estão sob licença livre) |
| `gt-02-caderno.jpg` | gerada para o episódio 01 | arte do canal | — | — | dossiê, **Recriação** |
| `gt-03-gazela-real.jpg` | Commons, *Female goitered gazelle, Shirvan National Park, Azerbaijan.jpg* | Elşad İbrahimov | CC BY-SA 4.0 | reduzida, recorte | dossiê |
| `gt-04-relevo-real.jpg` | Commons, *Urfa museum Animal relief sept 2019 4772.jpg* | Dosseman | CC BY-SA 4.0 | reduzida, recorte | dossiê (peça do Museu de Şanlıurfa — ver "Riscos registrados") |
| `gt-05-javali-real.jpg` | Commons, *Urfa museum Boar statue sept 2019 4766.jpg* | Dosseman | CC BY-SA 4.0 | reduzida, recorte | dossiê (idem) |
| `gt-06-cranios.jpg` | gerada para o episódio 01 | arte do canal | — | — | dossiê, **Recriação** (material craniano do DAI sem licença livre) |
| `gt-07-recinto-real.jpg` | Commons, *Gobekli Tepe Building F in 2014 3208.jpg* | Dosseman | CC BY-SA 4.0 | reduzida, recorte | dossiê |

## 002 · Cidades da Amazônia

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `002-amazonia-lidar.jpg` | gerada para o episódio 02 (`a07-01`) | arte do canal | — | recorte 16:9 | quadro 002 e dossiê, **Recriação** |
| `am-01-orellana.jpg` | gerada para o episódio 02 | arte do canal | — | — | dossiê, **Recriação** |
| `am-02-lidar-real.png` (+ `.webp`) | Commons, *Diverse Aquiry earthwork types with their topographical contexts (Fig. 2 in Pärssinen et al. (2026)…), Nature.png* — Pärssinen, M.; Kalliola, R.; Ranzi, A. et al., *Over 20,000 precolonial earthworks in the Southwest Amazonia*, Nature, 2026 | Pärssinen et al. | CC BY 4.0 | reduzida; WebP gerado pelo build | dossiê, seção 03 |
| `am-03-upano.jpg` | gerada para o episódio 02 | arte do canal | — | — | dossiê, **Recriação** |
| `am-04-estrada-reta.jpg` | gerada para o episódio 02 | arte do canal | — | — | dossiê, **Recriação** |
| `am-05-sangay-real.jpg` | Commons, *Volcan-Sangay-Ecuador.jpg* | Dabit100 | CC BY-SA 4.0 | reduzida, recorte | dossiê |
| `am-06-aquiry-mapa-real.png` (+ `.webp`) | Commons, *Area of the Aquiry (Fig. 3 in Pärssinen et al. (2026)…), Nature.png* | Pärssinen et al. | CC BY 4.0 | reduzida; WebP gerado pelo build | dossiê |
| `am-07-terra-preta-real.jpg` | Commons, *Nutrient-enriched terra preta soil.jpg* | Bruno Glaser | CC BY 4.0 | reduzida | dossiê |
| `am-08-lamina.jpg` | gerada para o episódio 02 | arte do canal | — | — | dossiê, **Recriação** |

## 003 · Os nadadores do Saara

Levantamento completo, com a armadilha dos três abrigos, em
`_src/imagens/SAARA.md`. Corte 16:9, sem ampliação (originais de 800 px).

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `saara-nadador.jpg` | Commons, *WadiSuraSingleSwimmer.jpg* (Wadi Sura I) | Roland Unger | CC BY-SA 3.0 | recorte 16:9 | quadro 003 |
| `saara-figuras.jpg` | Commons, *WadiSuraHumans.jpg* (Wadi Sura I) | Roland Unger | CC BY-SA 3.0 | recorte 16:9 | dossiê |
| `saara-animal.jpg` | Commons, *WadiSuraAnimal.jpg* (Wadi Sura I) | Roland Unger | CC BY-SA 3.0 | recorte 16:9 | dossiê |
| `saara-abrigos.jpg` | Commons, *WadiSuraCaves.jpg* (a rocha, com Wadi Sura I e a caverna dos arqueiros) | Roland Unger | CC BY-SA 3.0 | recorte 16:9 | dossiê |
| `saara-feras-abrigo.jpg` | Commons, *FogginiCaveTotal.jpg* (Wadi Sura II) | Roland Unger | CC BY-SA 3.0 | recorte 16:9 | dossiê |
| `saara-feras-maos.jpg` | Commons, *FogginiHands.jpg* (Wadi Sura II) | Roland Unger | CC BY-SA 3.0 | recorte 16:9 | dossiê |
| `saara-gilf-kebir.jpg` | Commons, *GilfKebir1.jpg* | Clemens Schmillen | CC BY-SA 4.0 | recorte 16:9 | dossiê |
| `saara-almasy.jpg` | Commons, *Salam operation at Wadi Sura.jpg*, 1942 (origem declarada: forosegundaguerra.com) | autor desconhecido | domínio público — marcado no Commons como **PD-Egypt** (fotografia egípcia, prazo de 25 anos) e *Not-PD-US-expired-min-year*; base frágil, ver "Riscos registrados" | recorte 16:9 | dossiê, seção 02 |

## 004 · Os papiros de Herculano

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `004-papiros-herculano-rolo.jpg` | Commons, *Herculaneum papyri.jpg* — figura de Stabile, S. et al., *Scientific Reports* 11, 2021 (s41598-020-80458-z) | Sara Stabile, Francesca Palermo, Inna Bukreeva, Daniela Mele, Vincenzo Formoso, Roberto Bartolino, Alessia Cedola | CC BY 4.0 | reduzida e centralizada sobre fundo carvão, 16:9 (sem corte) | quadro 004 |
| `hc-01-rolo-real.jpg` | o mesmo arquivo, inteiro | idem | CC BY 4.0 | reduzida | dossiê, abertura |
| `hc-02-piaggio-real.jpg` | Commons, *ARA 1809 V01 D032 Apparatus used to unroll the Herculenean papyri.jpg*, em *The Repository of Arts*, Londres, 1809 | autor desconhecido | domínio público (publicada em 1809) | reduzida | dossiê, seção 02 |
| `hc-03-aberto-real.jpg` | Commons, *Heruclaneum Papyrus 1521 f001r, British Library 01.jpg* | fotografia de autor desconhecido, British Library | domínio público (reprodução fiel de obra antiga) | reduzida | dossiê, seção 02 |

**Trocado em 03/10/2026:** o quadro 004 usava `004-papiros-herculano-real.jpg`,
que é o *PHerc. Paris 4.webp* do Commons — leitura do Vesuvius Challenge
(fonte: scrollprize.org), marcada lá como CC BY-SA 4.0 com autoria
"Vesuvius Challenge". A montante o material é **CC BY-NC 4.0**, e NC não
entra. O arquivo saiu de `assets/img/` e está em `_src/imagens/descartadas/`.

## 005 · A Grande Pirâmide

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `006-grande-piramide-real.jpg` | Commons, *Giza Great Pyramid of Khufu (9793885004).jpg* (conferida: fiadas expostas até o ápice, é Quéops) | Gary Todd | CC0 | reduzida, recorte 16:9 | quadro 005; dossiê |

## 006 · Nan Madol

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `009-nan-madol-real.jpg` | Commons, *Nan madol.jpg* (NOAA Photo Library, mvey0173) | NOAA | domínio público (obra do governo dos EUA, PD-USGov-NOAA) | reduzida, recorte 16:9 | quadro 006; dossiê |

## 007 · Denisovanos

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `010-denisovanos-real.jpg` | Commons, *Black Anui of Ust-Kansky district. Denisova cave.jpg* | Александр Байдуков | CC BY-SA 4.0 | reduzida, recorte 16:9 | quadro 007; dossiê |

## 008 · Serra da Capivara

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `003-serra-da-capivara-real.jpg` | Commons, *Geologia do PN Serra da Capivara (9580).jpg* | Mateus S. Figueiredo | CC BY-SA 4.0 | reduzida, recorte 16:9 | quadro 008; dossiê |

## 009 · O manuscrito Voynich

| Arquivo | Origem | Onde entra |
|---|---|---|
| `008-manuscrito-voynich.jpg` | Beinecke MS 408, Yale — recorte da folha dobrada | quadro 009; base de `og/manuscrito-voynich.jpg` |
| `vy-004.jpg` `vy-025.jpg` `vy-080.jpg` | Beinecke MS 408 — seção botânica | visor de fólios do dossiê |
| `vy-125.jpg` | Beinecke MS 408 — seção astronômica | visor |
| `vy-158.jpg` | Beinecke MS 408 — folha dobrada, nove diagramas | visor |
| `vy-163.jpg` | Beinecke MS 408 — seção farmacológica | visor |
| `vy-190.jpg` | Beinecke MS 408 — seção das receitas | visor |
| `vy-escrita.jpg` | Beinecke MS 408 — recorte fechado do fólio 190 | figura do dossiê, seção 04 |

**Crédito na tela:** Beinecke Rare Book & Manuscript Library, Yale University
— MS 408. **Licença:** domínio público — o manuscrito é do início do século XV
(radiocarbono 1404–1438), e a Beinecke disponibiliza a digitalização sem
restrição. Os arquivos vieram dessa digitalização, via Internet Archive.
Fonte completa: https://collections.library.yale.edu/catalog/2002046.
Os fólios do visor preservam a proporção original (até 1400 × 980): cortar um
documento histórico para caber num quadro seria falsificá-lo.

## 010 · Percy Fawcett

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `007-fawcett-real.jpg` | Commons, *Culuene River Upper Xingu Mato Gross.jpg* (rio Culuene perto de Gaúcha do Norte, MT, 2023) | JialiangGao | CC BY-SA 4.0 | reduzida, recorte 16:9 | quadro 010 |
| `fw-01-retrato-real.jpg` | Commons, *PercyFawcett.jpg*, 1911 | autor desconhecido | domínio público (PD-old: mais de 100 anos) | reduzida | dossiê |
| `fw-02-jack-raleigh-real.jpg` | Commons, *Jack Fawcett and Raleigh Rimell（1925）.jpg*, 1925 | autor desconhecido | domínio público (PD-old-70) | sem ampliação | dossiê |
| `fw-03-ossada-real.jpg` | Commons, *1952 Orlando e a ossada de Fawcett.jpg* — "foto C.V.B., arquivo da família Villas Bôas" | C.V.B. | CC BY-SA 3.0 (migrada da GFDL) | reduzida | dossiê |

## 011 · A Sentinela do Norte

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `011-sentinela-do-norte-real.jpg` | Commons, *North Sentinel Island from flight.jpg* | PJeganathan | CC BY-SA 4.0 | recorte 16:9 | quadro 011 |
| `011-sentinela-voo.jpg` | o mesmo arquivo, inteiro | PJeganathan | CC BY-SA 4.0 | reduzida | dossiê, seção 01 |
| `011-sentinela-satelite.jpg` | Commons, *North Sentinel Island.jpg* | NASA Earth Observatory (Jesse Allen, dados EO-1) | domínio público (obra da NASA) | reduzida | dossiê, seção 01 |

## 012 · O mecanismo de Anticítera

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `012-anticitera-modelo.jpg` (e `-640`, `-800`) | Commons, *Reconstructing the Antikythera Mechanism exhibition at WA Museum Boola Bardip, 2023, 03.jpg* — réplica de Nick Andronis, vista de lado, exposta em Perth (Austrália) | Chris Olszewski (réplica: Nick Andronis) | CC BY-SA 4.0 | recorte 16:9 | quadro 012, etiqueta **Modelo** |
| `ac-01-mykali-1901.jpg` | Commons, *Antikes Wrack von Antikythera 03.jpg*, 1900–1901 | autor desconhecido | domínio público (fotografia de mais de 120 anos) | sem recorte | dossiê, abertura |
| `ac-02-modelo-roda-principal.jpg` | Commons, *41598 2021 84310 Fig5 HTML.jpg* — Freeth et al., *Scientific Reports* 11:5821 (2021), fig. 5a: reconstrução em computador da roda principal (b1) | T. Freeth, D. Higgon, A. Dacanalis et al. | CC BY 4.0 | recorte do painel (a), rótulo retirado, fundo branco ampliado para quadrado | dossiê, seção 01, etiqueta **Modelo** |
| `ac-03-modelo-cosmos.jpg` | Commons, *41598 2021 84310 Fig7 HTML.jpg* — Freeth et al., *Scientific Reports* 11:5821 (2021), fig. 7: modelo em computador do mostrador da frente | T. Freeth, D. Higgon, A. Dacanalis et al. | CC BY 4.0 | reduzida | dossiê, seção 04, etiqueta **Modelo** |
| `ac-04-modelo-inscricoes.jpg` | Commons, *Reconstructing the Antikythera Mechanism exhibition at WA Museum Boola Bardip, 2023, 04.jpg* — réplica de Nick Andronis, alto da placa da frente com texto em grego | Chris Olszewski (réplica: Nick Andronis) | CC BY-SA 4.0 | recorte | dossiê, seção 02, etiqueta **Modelo** |
| `ac-05-modelo-verso.jpg` | Commons, *Antikythera mechanism frontview, 1st-2nd century BC, Greece (model).jpg* — réplica da Universidade Aristóteles de Tessalônica; a foto mostra a face de trás | Gts-tg | CC BY-SA 4.0 | recorte quadrado | dossiê, seção 03, etiqueta **Modelo**; base de `og/anticitera.jpg` |

## 013 · As Linhas de Nazca

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `013-linhas-de-nazca-real.jpg` | Commons, *Líneas de Nazca, Nazca, Perú, 2015-07-29, DD 52.JPG* | Diego Delso | CC BY-SA 4.0 | recorte 16:9 do beija-flor | quadro 013 |
| `nz-01-colibri.jpg` | o mesmo arquivo | Diego Delso | CC BY-SA 4.0 | reduzida, sem recorte | dossiê, abertura |
| `nz-02-macaco.jpg` | Commons, *Líneas de Nazca, Nazca, Perú, 2015-07-29, DD 49.JPG* | Diego Delso | CC BY-SA 4.0 | reduzida | dossiê, seção 05 |
| `nz-03-aranha.jpg` | Commons, *Líneas de Nazca, Nazca, Perú, 2015-07-29, DD 54.JPG* | Diego Delso | CC BY-SA 4.0 | reduzida | dossiê, seção 04 |
| `nz-04-mirante.jpg` | Commons, *Mirador Lineas de Nazca Peru - panoramio.jpg* | Va de Carro (Panoramio) | CC BY 3.0 | reduzida | dossiê, seção 03 |
| `nz-05-rodovia.jpg` | Commons, *Nazca-Linien 062016 hands tree lizard.jpg* | Max Berger | CC BY-SA 4.0 | reduzida | dossiê, seção 07 |

## 014 · Puma Punku

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `014-puma-punku-real.jpg` | Commons, *Pumapunku 02.jpg*, 2017 | Benjamin Burga | CC BY-SA 4.0 | recorte 16:9 | quadro 014; dossiê |
| `pp-01-laje-arenito.jpg` | Commons, *Puma Punku foundation rock 2.JPG*, 2011 | Janikorpi | CC BY-SA 3.0 | reduzida | dossiê, seção 01 |
| `pp-02-blocos-h.jpg` | Commons, *LAS H DE PUMA PUNKU.jpg*, 2025 | Keyan Alejandro | CC BY 4.0 | reduzida | dossiê, seção 04 |
| `pp-03-encaixes-grampos.jpg` | Commons, *Puma Punku foundation plate joint.JPG*, 2011 | Janikorpi | CC BY-SA 3.0 | reduzida | dossiê, seção 05 |
| `pp-04-modelo-vranich.jpg` | Commons, *Virtual model pumapunku2.png* — figura de *Heritage Science* 6:65, 2018 | Alexei Vranich | CC BY 4.0 | fundo transparente achatado em branco | dossiê, seção 07, etiqueta **Modelo** |
| `pp-05-blocos-espalhados.jpg` | Commons, *Puma Punku pile of rocks.JPG*, 2011 | Janikorpi | CC BY-SA 3.0 | recorte da borda esquerda | dossiê, abertura |

## 015 · Os moais da Ilha de Páscoa

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `015-moais-rapa-nui-real.jpg` | Commons, *Moai at Rano Raraku - Easter Island* (Flickr), 2010 | TravelingOtter | CC BY 2.0 | recorte 16:9 | quadro 015; dossiê |
| `mo-01-rano-raraku.jpg` | Commons, *Easter Island, Rano Raraku, moais* (Flickr), 2011 | Arian Zwegers | CC BY 2.0 | reduzida | dossiê, abertura |
| `mo-02-escavada-1919.jpg` | Katherine Routledge, *The Mystery of Easter Island* (Londres, 1919), fig. 72, "Excavated statue. South-east side, Rano Raraku" — via Project Gutenberg (ebook 69807) | fotografia da expedição Mana, 1914–1915 | domínio público — publicada em 1919 no Reino Unido; a autora morreu em 1935 e Scoresby Routledge em 1939 (mais de 70 anos); publicação anterior a 1931 nos EUA. Substitui em 03/10/2026 a lantern slide do British Museum (Oc,G.T.1465), cuja origem é de licença não comercial | sem recorte | dossiê, seção dos corpos enterrados |
| `mo-03-inacabado.jpg` | Commons, *Fabrica de Moais-10* (Flickr), 2024 | Otávio Nogueira | CC BY 2.0 | reduzida | dossiê, seção 02 |
| `mo-04-ahu-tongariki.jpg` | Commons, *Ahu Tongariki - Easter Island* (Flickr), 2010 | TravelingOtter | CC BY 2.0 | reduzida | dossiê, seção 05 |
| `mo-05-hoa-hakananaia.jpg` | Commons, *Hoa Hakananai'a BM Oc1869 1005 1*, 2011 | Andreas Praefcke | domínio público (dedicação do autor, PD-self) | reduzida | dossiê, seção 07 |

## 016 · A anomalia do mar Báltico

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `016-anomalia-do-baltico-real.jpg` | Commons, *Gulf of Bothnia (MODIS).jpg*, 3 abr. 2023 | MODIS Land Rapid Response Team, NASA/GSFC | domínio público (obra da NASA) | recorte 16:9 | quadro 016 |
| `ba-01-golfo-de-botnia.jpg` | Commons, *Gulf of Bothnia satellite.jpg*, 15 mar. 2002 | Jacques Descloitres, MODIS Land Rapid Response Team, NASA/GSFC | domínio público (obra da NASA) | reduzida | dossiê, abertura |
| `ba-02-sonar-de-arrasto.jpg` | Commons, *US Navy 040827-N-7676W-145 … retrieves the Towfish side scan sonar unit*, 27 ago. 2004 | John F. Williams, Marinha dos EUA | domínio público (obra do governo dos EUA) | reduzida | dossiê, seção 02 |
| `ba-03-sonar-lateral.jpg` | Commons, *USRC Bear wreck sidescan sonar image North Atlantic 16 September 2019.png* | NOAA / Guarda Costeira dos EUA | domínio público (obra do governo dos EUA) | reduzida | dossiê, seção 02 |
| `ba-04-bloco-erratico.jpg` | Commons, *Viikki rapakivi erratic boulder.jpg*, 15 ago. 2020 | Mjeltsch | CC BY-SA 4.0 | reduzida | dossiê, seção 05 |
| `ba-05-limonita.jpg` | Commons, *Limonite, bog iron ore, Nova Scotia - Redpath Museum - McGill University … DSC08020.jpg*, 2016 | Daderot | CC0 | reduzida | dossiê, seção 04 |

## 017 · O DNA fantasma da África Ocidental

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `017-dna-fantasma-real.jpg` | Commons, *Illumina Hiseq 2000 sequencers, BGI Hong Kong sequencing room.JPG* | Scotted400 | CC BY 3.0 | recorte 16:9 | quadro 017; dossiê, seção 07 |
| `df-01-iwo-eleru.jpg` | Commons, *Iwo Eleru.Journal.pone.0024024.g001-crop.jpg* — Harvati, K. et al., PLoS ONE 6(9): e24024, 2011, fig. 1 | Harvati, Stringer, Grün, Aubert, Allsworth-Jones, Folorunso | CC BY 4.0 | recorte | dossiê, seção 05 |
| `df-02-mapa-iwo-eleru.jpg` | Commons, *Journal.pone.0024024.g001-(L).jpg* — mesma figura, metade esquerda | idem | CC BY 4.0 | recorte | dossiê, seção 05 |
| `df-03-kabwe.jpg` | Commons, *Broken Hill skull 02.jpg* (Natural History Museum, Londres) | Jonathan Cardy | CC BY-SA 3.0 | recorte | dossiê, seção 05 |
| `df-04-sequenciador.jpg` | Commons, *Illumina HiSeq 2500.jpg* | Konrad Förstner | CC0 | reduzida | dossiê, abertura |

## 018 · O incidente da passagem Dyatlov

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `018-passagem-dyatlov-real.jpg` | Commons, *Dyatlov.Volume 1.Page 387.jpg* — despacho de encerramento, p. 4, 28/05/1959 | Lev Ivanov, Procuradoria da região de Sverdlovsk | domínio público (documento oficial, PD-RU-exempt) | recorte 16:9 | quadro 018 |
| `dy-01-vale-auspiya.jpg` | Commons, *Ауспия 2015.JPG* | Futball80 | CC BY-SA 4.0 | reduzida | dossiê, abertura |
| `dy-02-mapa-encosta.jpg` | Commons, *Dyatlov pass incident satellite height map 1.svg*, 2021, sobre dados ASTER (NASA/METI) e Sentinel-2 (ESA) | Merikanto | CC BY-SA 4.0 | rasterizado e recortado | dossiê, seção 02 |
| `dy-03-abertura-do-caso.jpg` | Commons, *Dyatlov.Volume 1.Page 1.jpg* — despacho de abertura, 26/02/1959 | V. I. Tempalov, Procuradoria de Ivdel | domínio público (PD-RU-exempt) | recortado | dossiê, seção 04 |
| `dy-04-pericia-radiologica.jpg` | Commons, *Dyatlov.Volume 1.Page 370.jpg* — perícia radiológica, 18/05/1959 | Lev Ivanov | domínio público (PD-RU-exempt) | recortado | dossiê, seção 03 |
| `dy-05-encerramento.jpg` | Commons, *Dyatlov.Volume 1.Page 387.jpg* | Lev Ivanov | domínio público (PD-RU-exempt) | recortado | dossiê, seção 04 |

## 019 · A colônia perdida de Roanoke

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `019-colonia-roanoke-real.jpg` | Commons, *Map of Virginia, Theodorus de Bry, 1591.jpg* — "Americae pars, nunc Virginia dicta", 1590 (exemplar colorido fotografado por GoShow) | Theodor de Bry segundo John White | domínio público (gravura de 1590; reprodução fiel) | recorte 16:9 | quadro 019 |
| `rk-01-chegada.jpg` | "The Englishmen's arrival in Virginia", 1590, Library of Congress (LCCN 2001696963) | Theodor de Bry segundo John White | domínio público | recorte sem o texto alemão | dossiê, abertura |
| `rk-02-mapa-de-bry.jpg` | o mesmo mapa de 1590 (exemplar fotografado por GoShow) | Theodor de Bry segundo John White | domínio público | reduzida | dossiê, seção 01 |
| `rk-03-croatoan.jpg` | "The Lost Colony", em *A Popular History of the United States*, 1876 (Internet Archive Book Images) | desenho de William Ludwell Sheppard, gravura de William James Linton | domínio público (publicada em 1876) | reduzida | dossiê, seção 04 (legendada como ilustração) |
| `rk-04-ilha-satelite.jpg` | "Kitty Hawk and Kill Devil Hills", NASA Earth Observatory, dados Landsat (USGS), 21/12/2017 | Joshua Stevens | domínio público (obra da NASA) | recorte | dossiê, seção 08 |
| `rk-05-fort-raleigh.jpg` | "Fort Raleigh National Historic Site earthworks", 2011 | Sarah Stierch | CC BY 4.0 | recorte | dossiê, seção 09 |

## 020 · Kryptos

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `020-kryptos-real.jpg` | Commons, *Kryptos sculptor.jpg*, 1991 — permissão do autor registrada na Wikimedia (VRT/OTRS, tíquete 2009102410027534) | Jim Sanborn | CC BY-SA 3.0 | recorte 16:9 (640 × 360); a versão de 960 é ampliada 1,5× | quadro 020 |
| `kr-01-escultura.jpg` | o mesmo arquivo, inteiro (640 × 512) | Jim Sanborn | CC BY-SA 3.0 | sem recorte | dossiê, abertura |
| `kr-02-sede.jpg` | Commons, *Aerial view of the Central Intelligence Agency headquarters, Langley, Virginia - Corrected and Cropped.jpg* (Biblioteca do Congresso) | Carol M. Highsmith | domínio público (doação da autora, PD-Highsmith) | reduzida | dossiê, seção 06 |
| `kr-03-carter.jpg` | Commons, *The Moment Carter Opens the Shrine.jpg*, 1924 | Harry Burton | domínio público (publicada em 1924) | reduzida, recorte vertical | dossiê, seção 04 |
| `kr-04-relogio.jpg` | Commons, *Reloj Mundial, Berlín, Alemania, 2016-04-22, DD 46-48 HDR.jpg* (obra em espaço público, liberdade de panorama na Alemanha) | Diego Delso | CC BY-SA 4.0 | reduzida | dossiê, seção 05 |

## 021 · O povo mashco piro

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `021-mashco-piro-real.jpg` | Commons, *Las Piedras River Outlook.jpg*, 2018 | Julio Araújo Flores e Patrick Champagne (ARCAmazon) | CC BY-SA 4.0 | recorte 16:9 | quadro 021 |
| `mp-01-rio-las-piedras.jpg` | o mesmo arquivo, inteiro | idem | CC BY-SA 4.0 | reduzida | dossiê, seção 01 |
| `mp-02-istmo-fitzcarrald.jpg` | Commons, *Map depicting the Isthmus of Fitzcarrald, circa 1904.jpg* — *Plano del Istmo Fiscarrald*, Lima, 1903 | Georg M. von Hassel, reduzido por Rafael E. Baluarte | domínio público (publicado em 1903) | reduzida | dossiê, seção 02 |
| `mp-03-las-piedras-1907.jpg` | rio Las Piedras a 103 km da foz, em Carlos Larrabure i Correa, *Noticia histórico-geográfica de algunos ríos de nuestro Oriente*, Lima, 1907 | autor da fotografia não identificado | domínio público (publicada em 1907) | reduzida | dossiê, seção 02 |
| `mp-04-mapa-las-piedras.jpg` | Commons, *Map of Las Piedras River and Pariamanu* | © colaboradores do OpenStreetMap, editado por UliHeiral | CC BY-SA 4.0 | reduzida | dossiê, seção 03 |
| `mp-05-garimpo-madre-de-dios.jpg` | Commons, *Garimpo de ouro ilegal na Amazônia em Madre de Dios, Perú* (Flickr observacao-da-terra), set. 2019 | Coordenação-Geral de Observação da Terra (INPE) | CC BY-SA 2.0 | reduzida | dossiê, seção 07 |

## 022 · Os korowai

| Arquivo | Origem | Autor | Licença | Modificação | Onde entra |
|---|---|---|---|---|---|
| `022-korowai-real.jpg` | Commons, diapositivo "Een boomhuis van Kuruwai Papua's in Basman", 14/07/1992, Nationaal Museum van Wereldculturen / Wereldmuseum TM-20041236 | Willem Theodoor (Wim) van Oijen | CC BY 4.0 | recorte 16:9 | quadro 022 |
| `ko-01-casa-mbasman.jpg` | o mesmo diapositivo, quadro inteiro | idem | CC BY 4.0 | reduzida | dossiê, seção 03 |
| `ko-02-casa-alta.jpg` | Commons, "Korowai Treehouse 2" (Flickr), 23/07/2006 | usuário do Flickr "♪ ~ from Jayapura, Indonesia" | CC BY 2.0 | ampliada de 640 para 960 px | dossiê, seção 04 |
| `ko-03-lorentz-1910.jpg` | Commons, "Verlaten Papua boomhuis langs de Lorentz-rivier", 1909–1910, Wereldmuseum TM-FV-0783-104 | autor desconhecido | domínio público (fotografia de mais de 110 anos) | recorte da cópia montada (não é casa korowai; a legenda diz isso) | dossiê, seção 04 |
| `ko-04-mapa-1959.jpg` | U.S. Army Map Service, folha SB 54-1 "Eilanden River", série T401, 1:500.000, 1959 | U.S. Army Map Service | domínio público (obra do governo dos EUA) | recorte, com marcação âmbar de Yaniruma acrescentada por nós | dossiê, seção 01 |

## Riscos registrados (decisão do dono)

- **012 · peças do Museu Arqueológico Nacional de Atenas**: a lei grega (art. 46
  da Lei 3028/2002; DM 436630/2023) exige autorização para uso comercial de
  imagem de bem cultural. **Resolvido por decisão do dono em 03/10/2026:**
  as fotos das peças originais (`012-anticitera-real`, `ac-02-fragmento-a`,
  `ac-03-fragmento-c`, `ac-04-fragmento-19`) saíram do site e foram para
  `_src/imagens/descartadas/`; no lugar entraram réplicas fotografadas fora
  da Grécia (Nick Andronis, Perth) e figuras de reconstrução em computador
  de Freeth et al. 2021 (CC BY 4.0), todas com etiqueta **Modelo**. Ficam
  `ac-01` (fotografia de 1900–1901 da operação no naufrágio, domínio
  público; risco baixo) e `ac-05` (réplica de Tessalônica).
- **001 · `gt-04` e `gt-05`**: peças do Museu de Şanlıurfa; a Turquia também
  pede autorização para uso comercial. Risco baixo; registrado.
- **003 · `saara-almasy`**: a base PD-Egypt depende de a foto ser egípcia, e
  a origem declarada no Commons é um fórum. Fica, por ser a única imagem da
  missão de 1942; se aparecer dúvida concreta, sai sem prejuízo do texto.

## Tratamento padrão

Corte 16:9, até 1200 px de largura, JPEG progressivo em qualidade 82. As
variantes `-640` e `-800` (e `-960`/`-1280` do herói) são geradas pelo
`build.py` para o `srcset` da home; os PNG referenciados em `<picture>`
ganham `.webp` no mesmo passo.

## Arquivos em `assets/img/` que nenhuma página usa

`001-gobekli-tepe.jpg`, `006-grande-piramide.jpg`, `010-denisovanos.jpg`,
`am-02-lidar.jpg`, `am-05-cinza-sangay.jpg`, `am-06-geoglifo.jpg`,
`am-07-terra-preta.jpg`, `gt-03-gazelas.jpg`, `gt-04-relevo-animal.jpg`,
`gt-05-javali-pintado.jpg`, `gt-07-entulho.jpg` (recriações substituídas por
foto), `dn-01-osso-real.jpg`, `dn-02-caverna-real.jpg`, `gt-08-pilar-real.jpg`,
`saara-maos-figuras.jpg`. Não estão no ar como imagem de página; podem sair
da pasta pública numa limpeza futura.
