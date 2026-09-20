# Acervo do dossiê 003 — Nadadores do Saara

Levantado em 20/09/2026 no Wikimedia Commons, via API, com licença, autoria e
resolução conferidas arquivo por arquivo. **Cada candidata foi baixada e
aberta** antes de entrar — duas foram descartadas depois de olhadas.

Nenhuma recriação. O sítio existe, é fotografado, e o degrau 1 resolveu tudo.

---

## A armadilha deste dossiê

São **três** abrigos em Wadi Sura, não um:

| Abrigo | Nome | Onde |
|---|---|---|
| **Wadi Sura I** | caverna dos nadadores | o de Almásy, 1933 — arruinado |
| **Cave of the Archers** | caverna dos arqueiros | no mesmo domo de rocha |
| **Wadi Sura II** | caverna das feras | 10 km a oeste, achada em 2002 |

O dossiê denuncia a confusão entre eles; publicar uma foto trocada seria
vexame. Por isso **a coluna "abrigo" abaixo saiu da descrição escrita pelo
próprio fotógrafo no Commons**, não da categoria — categoria no Commons é
frouxa, e a `WadiSuraCaves.jpg` aparece em três delas ao mesmo tempo.

---

## O que entrou

| Arquivo no site | Origem | Abrigo | Licença / autor |
|---|---|---|---|
| `saara-nadador.jpg` | WadiSuraSingleSwimmer.jpg | Wadi Sura I | CC BY-SA 3.0 · Roland Unger |
| `saara-figuras.jpg` | WadiSuraHumans.jpg | Wadi Sura I | CC BY-SA 3.0 · Roland Unger |
| `saara-maos-figuras.jpg` | WadiSuraHandHumans.jpg | Wadi Sura I | CC BY-SA 3.0 · Roland Unger |
| `saara-animal.jpg` | WadiSuraAnimal.jpg | Wadi Sura I | CC BY-SA 3.0 · Roland Unger |
| `saara-abrigos.jpg` | WadiSuraCaves.jpg | a rocha, com I e arqueiros | CC BY-SA 3.0 · Roland Unger |
| `saara-feras-abrigo.jpg` | FogginiCaveTotal.jpg | **Wadi Sura II** | CC BY-SA 3.0 · Roland Unger |
| `saara-feras-maos.jpg` | FogginiHands.jpg | **Wadi Sura II** | CC BY-SA 3.0 · Roland Unger |
| `saara-gilf-kebir.jpg` | GilfKebir1.jpg | paisagem | CC BY-SA 4.0 · Clemens Schmillen |
| `saara-almasy.jpg` | Salam operation at Wadi Sura.jpg | documento de época | **domínio público** |

Processamento: corte 16:9 centralizado, JPEG progressivo q82. **Sem
ampliação** — os originais de Roland Unger são 800 px, e esticar para os 1200
do padrão do site inventaria resolução que não existe. Fica levemente mole em
tela de alta densidade, como boa parte do acervo já registrado no `BAIXAR.md`.

A `saara-almasy.jpg` é a menor de todas, 551 px. É foto de 1942 — não há
versão melhor, e a alternativa era não ter.

### Share-alike

Sete das nove são CC BY-SA. O recorte é obra derivada e sai nos mesmos
termos, como o `COMMONS.md` já registra para o acervo do Göbekli Tepe. A
legenda de cada figura no dossiê nomeia autor e licença.

---

## O que foi descartado, e por quê

**`AST-16-1247 contrast enhanced.jpg`** — imagem da NASA, Apollo-Soyuz, 1975,
domínio público, 3920 × 3870, com a descrição prometendo Líbia, Egito e o Mar
de Areia Líbio a 223 km de altitude. Parecia o achado do levantamento: uma
vista orbital do platô, livre de qualquer licença.

Aberta, é um quadro roxo uniforme com cruzes fiduciais. Nenhum relevo, nenhum
Gilf Kebir. Provavelmente um quadro perdido do rolo.

Fica registrado porque a ficha continua atraente, e alguém vai topar com ela
de novo. **Não perca tempo: a imagem não mostra nada.**

**`WadiSuraBowmen.jpg`** — arqueiros, ótima foto. Mas a descrição do autor diz
"in the **Cave of the Archers**". É o terceiro abrigo, e entraria no dossiê
como se fosse da caverna dos nadadores. Foi salva pela conferência da
descrição, não pela categoria.

**`WadiSuraLandscape.jpg`** — não baixou. O Wikimedia limitou o IP depois de
muitas requisições e essa foi a única que não passou em nenhuma tentativa. Não
faz falta: a `GilfKebir1.jpg` cobre a paisagem com mais resolução e um
enquadramento melhor, olhando de cima para dentro do wadi.

---

## Nota de processo, para o próximo levantamento

O `upload.wikimedia.org` devolve **429** depois de poucas dezenas de
requisições seguidas, e a mensagem de erro recomenda usar thumbnail em vez do
original. Duas coisas que funcionaram quando o download direto travou:

1. Pedir `iiurlwidth` na API e baixar o `thumburl`.
2. `https://commons.wikimedia.org/wiki/Special:FilePath/NOME?width=800`
   — **com `curl -L`**, porque devolve 302.

E espaçar. Vinte e cinco segundos entre arquivos passou; quatro não passou.
