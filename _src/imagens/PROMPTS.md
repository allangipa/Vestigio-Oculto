# Imagens que faltam — prompts prontos

Seis dossiês ainda estão sem imagem no quadro da home. Os outros quatro usam
material que já existe nas pastas dos episódios 01 e 02.

Custo: `flux_2` em 2k custa **1,5 crédito** por imagem. Seis imagens ≈ **9
créditos**. Confirme antes de rodar:

```
higgsfield generate cost flux_2 --resolution 2k --aspect-ratio 16:9
```

## Como rodar

```
higgsfield generate create flux_2 ^
  --prompt "<prompt abaixo + sufixo de estilo>" ^
  --resolution 2k --aspect-ratio 16:9 --wait
```

Sufixo de estilo — vai no fim de **todo** prompt, é o que mantém a paleta:

```
cinematic documentary still, moody low-key lighting, charcoal blacks and
bone-white tones with a single amber accent, fine film grain, no text,
no watermark, no red
```

Depois, salve cada arquivo com o nome indicado em `assets/img/` e troque, no
`_src/index.tpl.html`, o bloco `<a class="quadro-foto sem-imagem">` pelo bloco
com `<img>` — o do quadro 001 serve de modelo. Rode `python3 _src/build.py`.

Antes de aceitar, **confira em folha de contato**: das 147 imagens do episódio
01, oito estavam erradas e nenhuma dava para perceber pelo prompt.

---

## 003 — Serra da Capivara
**Arquivo:** `003-serra-da-capivara.jpg`

```
a deep archaeological trench cut into pale dry sandstone at the foot of a
canyon wall in the Brazilian caatinga, dark charcoal layers clearly banded in
the cut face, a single work lamp throwing amber light into the trench, sparse
thorny scrub on the rim above, last light
```

> Cuidado: não peça "red rock canyon" — sai Arizona e todo mundo vê. A pedra
> da Capivara é clara e a vegetação é espinhosa, não é mata. E não peça as
> pinturas rupestres: elas são vermelhas, e vermelho está fora da paleta.

## 004 — Os papiros de Herculano
**Arquivo:** `004-papiros-herculano.jpg`

```
extreme close-up of a carbonised papyrus scroll, black and brittle like burnt
wood, resting on a pale padded support inside a dark laboratory, a narrow amber
lamp raking across its cracked surface, scientific instruments out of focus
behind
```

## 005 — Sentinela do Norte
**Arquivo:** `005-sentinela-do-norte.jpg`

```
a small dense tropical island seen from far offshore across flat grey water,
unbroken forest reaching all the way down to a narrow beach, no buildings, no
boats, no people, heavy overcast sky with a single break of amber sun low on
the horizon
```

> Sem pessoas e sem embarcação, de propósito. O dossiê é sobre um contato que
> não deve acontecer; a imagem não pode sugerir que alguém desembarcou.

## 007 — Percy Fawcett
**Arquivo:** `007-percy-fawcett.jpg`

```
a 1920s canvas expedition tent and stacked wooden supply crates abandoned at
the edge of dense tropical forest at dusk, a kerosene lamp still burning amber
inside the open tent flap, low mist between the trunks, no people
```

## 008 — O manuscrito Voynich
**Arquivo:** `008-manuscrito-voynich.jpg`

```
close-up of an open medieval manuscript on vellum, covered in a flowing
unreadable handwritten script and ink drawings of plants that match no real
species, lying on a dark table under a narrow amber reading lamp, aged
parchment, no legible words
```

## 009 — Nan Madol
**Arquivo:** `009-nan-madol.jpg`

```
walls built from long hexagonal basalt columns stacked crosswise like stacked
timber, dark volcanic stone, rising straight out of shallow tidal water,
mangrove and low forest behind, overcast tropical light, no cut blocks, no
mortar, no brickwork, no masonry courses
```

> A negação no fim é obrigatória. O modelo insiste em parede de tijolo em
> fiadas regulares — foi o que estragou várias imagens do episódio 01. Aqui a
> pedra é colunar e empilhada, não cortada.

---

## Se quiser trocar as que já existem

Os quadros 001, 002, 006 e 010 usam imagens dos episódios. Se alguma não
agradar, as pastas têm alternativas:

| Quadro | Usando | Alternativas na pasta |
|---|---|---|
| 001 Göbekli Tepe | `07-escala-humana` | `06-pilar-em-t-v3`, `12-entulho-v2` |
| 002 Amazônia | `a07-01` (pirâmide de terra) | `a03-01` (avião sobre o dossel), `a05-01` (estrada reta na mata) |
| 006 Grande Pirâmide | `10-piramide` | — |
| 010 Denisovanos | `11-cacadores-v2` | `11-cacadores` (v1) |

**Não use `05-circulos-de-cima-v2`.** Vista de cima, os pilares em T leem como
cruzes, e o recinto vira cemitério cristão — o pior engano possível num
assunto neolítico. É a mesma armadilha que o `CLAUDE.md` do canal já registra.
