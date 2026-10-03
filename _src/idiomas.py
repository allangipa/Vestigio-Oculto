"""
Vestígio Oculto — idiomas do site.

Dois tipos de texto, dois lugares:

1. Página escrita à mão (dossiê, home, sobre, contato, privacidade, 404):
   TEMPLATE TRADUZIDO, em _src/<idioma>/<mesmo nome>.tpl.html, com a mesma
   marcação do original em português. A página só sai no idioma quando o
   arquivo existe. O cartão do dossiê na home do idioma fica em
   _src/<idioma>/cartoes/<slug>.html.

2. Texto que o BUILD escreve (o "próximo", a linha do pilar, a faixa de
   cookies, o link de rever cookies, o seletor de idioma, as páginas de
   pilar, a prévia de compartilhamento): ESTE ARQUIVO, num dicionário por
   idioma.

Português é a raiz do site e o original de tudo. Inglês sai em /en/,
espanhol em /es/. Um idioma só fica ATIVO quando tem home traduzida e pelo
menos um dossiê; antes disso o build o ignora sem erro.
"""

# Ordem do seletor e do sitemap. O primeiro é o original, na raiz.
IDIOMAS = ["pt", "en", "es"]

# Código do atributo lang, do hreflang e do og:locale.
HREFLANG = {"pt": "pt-BR", "en": "en", "es": "es"}
OG_LOCALE = {"pt": "pt_BR", "en": "en_US", "es": "es_LA"}

# Marca por idioma. O nome não se traduz; o subtítulo é configurável aqui e
# entra onde o template pede {{MARCA_SUB}}.
MARCA_SUB = {
    "pt": "",
    "en": "Hidden Traces of the Past",
    "es": "Huellas ocultas del pasado",
}

# Palavras que podem sumir de um crédito de imagem na tradução sem que se
# perca autoria (são rótulo ou instituição traduzida, não nome de pessoa).
# O build confere que todo nome próprio do crédito original continua no
# traduzido; se ele reclamar de uma palavra destas, acrescente-a aqui.
PALAVRAS_DE_CREDITO_PT = {
    "Foto", "Fotografia", "Documento", "Mapa", "Imagem", "Figura", "Plano",
    "Papiro", "Diapositivo", "Parque", "Nacional", "Marinha", "Estados",
    "Unidos", "Guarda", "Costeira", "Biblioteca", "Museu", "Arquivo",
    "Instituto", "Universidade", "Coleção", "Acervo", "Recriação",
    # rótulos de licença e de autoria: a licença em si é conferida à parte
    # (nome e link), e "autoria desconhecida" não é nome de ninguém
    "Domínio", "Público", "Autoria", "Autor", "Desconhecido", "Desconhecida",
    "Modelo", "Réplica", "Esquema",
}

# Nome de lugar, obra ou instituição que tem forma consagrada no idioma: no
# crédito traduzido vale a forma do idioma, sem repetir a portuguesa entre
# parênteses. Autor e licença NÃO entram aqui — continuam conferidos à letra.
EQUIVALENTES_DE_CREDITO = {
    "en": {
        "Londres": "London",
        "EUA": "U.S.",
        "Papiro": "Papyrus",
        "Herculano": "Herculaneum",
        "Biblioteca": "Library",
        "Congresso": "Congress",
        "Procuradoria": "Procuracy",
    },
    "es": {
        "Procuradoria": "Fiscalía",
        "Congresso": "Congreso",
        "EUA": "EE. UU.",
    },
}

T = {
    # ------------------------------------------------------------ português
    # Os textos em português reproduzem exatamente o que o site já publicava:
    # mudar uma linha aqui muda todas as páginas da raiz.
    "pt": {
        "nome": "Português",
        "sigla": "PT",
        "idioma_aria": "Idioma",
        "sem_traducao": "{idioma}: página inicial (esta página ainda não foi traduzida)",
        "em_portugues": "em português",
        "proximo": "Próximo no arquivo · Dossiê",
        "privacidade": "Política de privacidade",
        "rever_cookies": "Rever escolha de cookies",
        "sobre": "Sobre",
        "contato": "Contato",
        "inicio_aria": "Vestígio Oculto — início",
        "slogan": "Um arquivo aberto sobre o que a história começou e não terminou de contar.",
        "rodape_selo": "Textos autorais · imagens de recriação sinalizadas",
        "canal": "Canal",
        "pilares_rotulo": "Pilares",
        "pilares_aria": "Pilares editoriais",
        "pilar": "Pilar",
        "arquivo": "Arquivo",
        "dossies_n": "{n:02d} dossiês",
        "dossie_n1": "{n:02d} dossiê",
        "dossies_do_pilar": "Os {n} dossiês do pilar",
        "outros_pilares": "Outros pilares",
        "tema_link": "Este dossiê é do pilar {link} — veja os {n} dossiês dele.",
        "tema_link_sem_pagina": "Este dossiê é do pilar {link}.",
        "rotulo_recriacao": "Recriação",
        "rotulo_acervo": "Acervo",
        "consentimento": {
            "aria": "Aviso de cookies",
            "texto": ("Este site usa cookies do Google AdSense para exibir anúncios e medir\n"
                      "      audiência. Não coletamos cadastro, não pedimos e-mail e não temos\n"
                      "      formulário. Detalhes na\n"
                      '      <a href="{{RAIZ}}privacidade.html">política de privacidade</a>.'),
            "recusar": "Recusar anúncios",
            "aceitar": "Entendi",
        },
        "pilares": {
            "pedra": "Pedra e Poeira",
            "ontem": "Descoberto Ontem",
            "selado": "Arquivo Selado",
            "isolados": "Últimos Isolados",
        },
        # Os textos das páginas de pilar em português continuam em TEMAS, no
        # build.py, onde sempre estiveram.
        "temas": {},
        "og_alt": {},  # português usa OG_ALT, no build.py
        # home do idioma (só para idiomas que não o português; a home em
        # português tem os números escritos e conferidos no template)
        "qtd": lambda n: f"{n} dossiê" if n == 1 else f"{n} dossiês",
        "contagem_zero": "Em breve",
        "todos": "Todos",
    },

    # ------------------------------------------------------------ inglês
    "en": {
        "nome": "English",
        "sigla": "EN",
        "idioma_aria": "Language",
        "sem_traducao": "{idioma}: home page (this page has not been translated yet)",
        "em_portugues": "in Portuguese",
        "proximo": "Next in the archive · Dossier",
        "privacidade": "Privacy policy",
        "rever_cookies": "Review cookie choice",
        "sobre": "About",
        "contato": "Contact",
        "inicio_aria": "Vestígio Oculto — home",
        "slogan": "An open archive of what history began to tell and never finished.",
        "rodape_selo": "Original writing · re-created images labeled",
        "canal": "Channel",
        "pilares_rotulo": "Pillars",
        "pilares_aria": "Editorial pillars",
        "pilar": "Pillar",
        "arquivo": "Archive",
        "dossies_n": "{n:02d} dossiers",
        "dossie_n1": "{n:02d} dossier",
        "dossies_do_pilar": "The {n} dossiers in this pillar",
        "outros_pilares": "Other pillars",
        "tema_link": "This dossier belongs to the {link} pillar — see its {n} dossiers.",
        "tema_link_sem_pagina": "This dossier belongs to the {link} pillar.",
        "rotulo_recriacao": "Re-creation",
        "rotulo_acervo": "Archive",
        "consentimento": {
            "aria": "Cookie notice",
            "texto": ("This site uses Google AdSense cookies to show ads and measure\n"
                      "      audience. We do not collect sign-ups, ask for e-mail or have\n"
                      "      forms. Details in the\n"
                      '      <a href="{{RAIZ}}privacidade.html">privacy policy</a>.'),
            "recusar": "Decline ads",
            "aceitar": "Got it",
        },
        "pilares": {
            "pedra": "Stone and Dust",
            "ontem": "Discovered Yesterday",
            "selado": "Sealed Archive",
            "isolados": "The Last Isolated",
        },
        # Página de pilar: só sai no idioma quando TODOS os dossiês do pilar
        # estão traduzidos (a introdução nomeia cada caso). Até lá, o menu e o
        # rodapé apontam para a seção do pilar na home do idioma.
        "temas": {
            "pedra": {
                "titulo": "Stone and Dust: ancient monuments · Vestígio Oculto",
                "descricao": "Göbekli Tepe, the Great Pyramid, Nan Madol, the Nazca Lines, Puma Punku, "
                             "the moai and the swimmers of the Sahara: ancient monuments read by the evidence.",
                "intro": [
                    "Stone and Dust gathers the dossiers on ancient monuments and sites that do not fit "
                    "the accepted chronology: what was raised, painted or scraped into the ground before "
                    "there was anyone who, in theory, knew how to do it.",
                    "There are seven cases. The pillars of Göbekli Tepe, raised by hunter-gatherers before "
                    "agriculture; the swimmers painted in the Gilf Kebir, one of the driest places on the "
                    "planet; the voids that particle detectors mapped inside the Great Pyramid; the basalt "
                    "city of Nan Madol, built on a reef in Micronesia; the Nazca Lines, scraped into the "
                    "Peruvian desert; the H-shaped blocks of Puma Punku, on the Bolivian altiplano; and the "
                    "moai of Rapa Nui, with whole bodies under the hillside.",
                    "In all of them, the chronology comes before the theory: first what is in the ground and "
                    "how it was dated, then the hypotheses, from the most sober to the most improbable, with "
                    "the weight of evidence for each one stated.",
                ],
            },
            "ontem": {
                "titulo": "Discovered Yesterday: recent finds · Vestígio Oculto",
                "descricao": "Lidar in the Amazon, the Herculaneum papyri, Denisovans, Serra da Capivara, "
                             "Antikythera, the Baltic anomaly and ghost DNA: what technology revealed.",
                "intro": [
                    "Discovered Yesterday gathers the finds that only appeared because technology changed: "
                    "lidar, tomography, DNA sequencing, sonar — new instruments rereading old evidence.",
                    "The laser that went through the Amazon canopy and drew streets and earthen pyramids; "
                    "the tomography combined with machine learning that began to read the carbonized papyri "
                    "of Herculaneum; the DNA of a finger-bone fragment that revealed the Denisovans; the "
                    "charcoal of Serra da Capivara, in Piauí, that does not fit the chronology of the "
                    "Americas; the X-rays and tomography that read the gears of the Antikythera mechanism; "
                    "the sonar image of the Baltic anomaly; and the statistical model that estimated a ghost "
                    "DNA in West African populations.",
                    "A recent discovery is not a closed case. In several of these dossiers the data is solid "
                    "and the interpretation is still disputed, and the text keeps the two apart.",
                ],
            },
            "selado": {
                "titulo": "Sealed Archive: unsolved mysteries · Vestígio Oculto",
                "descricao": "The Voynich manuscript, Percy Fawcett, the Dyatlov Pass, the Roanoke colony "
                             "and Kryptos: unsolved mysteries, what is known and what is still open.",
                "intro": [
                    "Sealed Archive gathers undeciphered documents and expeditions without an ending: cases "
                    "in which the record exists, is preserved — and remains illegible or incomplete.",
                    "The Voynich manuscript, on authentic vellum and in a language no one has identified; "
                    "Percy Fawcett, who went into the Upper Xingu in 1925 after a city he called “Z” and "
                    "did not come back; the nine skiers of the Dyatlov Pass, in the Urals, in 1959; the "
                    "Roanoke colony, which left CROATOAN carved on a post; and Kryptos, the sculpture in the "
                    "CIA courtyard whose fourth message still has an unknown method.",
                    "Here the mystery is rarely a missing document. It is the document that exists and does "
                    "not add up — and each dossier shows what has already been ruled out, what is hypothesis "
                    "and what remains open.",
                ],
            },
            "isolados": {
                "titulo": "The Last Isolated: isolated peoples · Vestígio Oculto",
                "descricao": "North Sentinel Island, the Mashco Piro and the Korowai: peoples and territories "
                             "out of reach, what is known of them and what our curiosity costs them.",
                "intro": [
                    "The Last Isolated gathers territories and peoples beyond the reach of the contemporary "
                    "world — and what our curiosity costs them.",
                    "North Sentinel Island, in the Andaman archipelago, whose population has refused contact "
                    "for generations; the Mashco Piro, descendants of those who fled the rubber-boom "
                    "massacres, in voluntary isolation between Peru and Acre; and the Korowai, of Papua, "
                    "whose treetop houses became, over thirty years of photographs, the portrait of an "
                    "entire people.",
                    "In these dossiers the mystery is not buried. Almost everything known was seen from "
                    "afar, and the question changes: it is not only what exists there, it is what we decide "
                    "not to ask.",
                ],
            },
        },
        # Texto alternativo da prévia de compartilhamento (og:image). A imagem
        # é a de assets/img/og/en/<slug>.jpg, com o título em inglês gravado
        # nela (o mesmo que fecha cada alt); ver README, "Idiomas".
        "og_alt": {
            "gobekli-tepe": "Excavated enclosure at Göbekli Tepe with T-shaped pillars, under the title Göbekli Tepe",
            "amazonia-lidar": "Lidar relief with geometric earthen enclosures in the Amazon, under the title Cities of the Amazon",
            "nadadores-do-saara": "Rock painting of a human figure in a swimming pose at Wadi Sura, under the title The Swimmers of the Sahara",
            "papiros-herculano": "Carbonized papyrus scroll from Herculaneum, under the title The Herculaneum Papyri",
            "grande-piramide": "The stone courses of the Great Pyramid of Giza up to the apex, under the title The Great Pyramid",
            "nan-madol": "Columnar basalt walls of Nan Madol among the vegetation, under the title Nan Madol",
            "denisovanos": "View from inside Denisova Cave, in the Altai, under the title The Denisovans",
            "serra-da-capivara": "Sediment with pebbles and gravel at Serra da Capivara, under the title Serra da Capivara",
            "manuscrito-voynich": "Folded leaf of the Voynich manuscript with circular diagrams, under the title The Voynich Manuscript",
            "percy-fawcett": "Portrait of Percy Fawcett in 1911, under the title Percy Fawcett",
            "sentinela-do-norte": "North Sentinel Island seen from an airplane window, under the title North Sentinel Island",
            "anticitera": "Modern replica of the Antikythera mechanism, with its bronze dials exposed, under the title The Antikythera Mechanism",
            "linhas-de-nazca": "The hummingbird of the Nazca Lines seen from above, under the title The Nazca Lines",
            "puma-punku": "H-shaped stone blocks at Puma Punku, under the title Puma Punku",
            "moais-rapa-nui": "Moai on the slope of Rano Raraku, on Easter Island, under the title The Moai of Easter Island",
            "anomalia-do-baltico": "Satellite view of the Gulf of Bothnia, with ice on the Baltic Sea, under the title The Baltic Sea Anomaly",
            "dna-fantasma": "Room of DNA sequencers, under the title Ghost DNA",
            "passagem-dyatlov": "Auspiya River valley in the Urals, with snow on the trees, under the title The Dyatlov Pass",
            "colonia-roanoke": "Theodor de Bry's 1590 map of Virginia, with Roanoke Island, under the title The Roanoke Colony",
            "kryptos": "The Kryptos sculpture, by Jim Sanborn, under the title Kryptos",
            "mashco-piro": "The Las Piedras River winding through the Amazon rainforest of Peru, under the title The Mashco Piro",
            "korowai": "Silhouette of a tree house among palm trees, in Papua, under the title The Korowai",
        },
        "qtd": lambda n: f"{n} dossier" if n == 1 else f"{n} dossiers",
        "contagem_zero": "Coming soon in English",
        "todos": "All",
    },

    # ------------------------------------------------------------ espanhol
    # Ativo desde 03/10/2026, com os 22 dossiês e as quatro páginas de pilar.
    "es": {
        "nome": "Español",
        "sigla": "ES",
        "idioma_aria": "Idioma",
        "sem_traducao": "{idioma}: página de inicio (esta página aún no ha sido traducida)",
        "em_portugues": "en portugués",
        "proximo": "Siguiente en el archivo · Dossier",
        "privacidade": "Política de privacidad",
        "rever_cookies": "Revisar la elección de cookies",
        "sobre": "Acerca de",
        "contato": "Contacto",
        "inicio_aria": "Vestígio Oculto — inicio",
        "slogan": "Un archivo abierto sobre lo que la historia empezó a contar y no terminó.",
        "rodape_selo": "Textos propios · imágenes de recreación señaladas",
        "canal": "Canal",
        "pilares_rotulo": "Pilares",
        "pilares_aria": "Pilares editoriales",
        "pilar": "Pilar",
        "arquivo": "Archivo",
        "dossies_n": "{n:02d} dossieres",
        "dossie_n1": "{n:02d} dossier",
        "dossies_do_pilar": "Los {n} dossieres del pilar",
        "outros_pilares": "Otros pilares",
        "tema_link": "Este dossier es del pilar {link} — vea sus {n} dossieres.",
        "tema_link_sem_pagina": "Este dossier es del pilar {link}.",
        "rotulo_recriacao": "Recreación",
        "rotulo_acervo": "Archivo",
        "consentimento": {
            "aria": "Aviso de cookies",
            "texto": ("Este sitio usa cookies de Google AdSense para mostrar anuncios y medir\n"
                      "      la audiencia. No pedimos registro ni correo electrónico y no tenemos\n"
                      "      formularios. Detalles en la\n"
                      '      <a href="{{RAIZ}}privacidade.html">política de privacidad</a>.'),
            "recusar": "Rechazar anuncios",
            "aceitar": "Entendido",
        },
        "pilares": {
            "pedra": "Piedra y Polvo",
            "ontem": "Descubierto Ayer",
            "selado": "Archivo Sellado",
            "isolados": "Últimos Aislados",
        },
        # Páginas de pilar em espanhol (traduzidas do português, de TEMAS no
        # build.py). Mesma regra do inglês: só saem com o pilar inteiro traduzido.
        "temas": {
            "pedra": {
                "titulo": "Piedra y Polvo: monumentos antiguos · Vestígio Oculto",
                "descricao": "Göbekli Tepe, la Gran Pirámide, Nan Madol, Nazca, Puma Punku, los moáis "
                             "y los nadadores del Sahara: monumentos antiguos leídos por la evidencia.",
                "intro": [
                    "Piedra y Polvo reúne los dossieres sobre monumentos y sitios antiguos que no caben "
                    "en la cronología aceptada: lo que fue erigido, pintado o raspado en el suelo antes "
                    "de que existiera quien, en teoría, supiera hacerlo.",
                    "Son siete casos. Los pilares de Göbekli Tepe, erigidos por cazadores-recolectores antes "
                    "de la agricultura; los nadadores pintados en el Gilf Kebir, uno de los lugares más secos "
                    "del planeta; los vacíos que detectores de partículas cartografiaron dentro de la Gran "
                    "Pirámide; la ciudad de basalto de Nan Madol, construida sobre un arrecife en Micronesia; "
                    "las líneas de Nazca, raspadas en el desierto de Perú; los bloques en H de Puma Punku, en "
                    "el altiplano de Bolivia; y los moáis de Rapa Nui, con el cuerpo entero bajo la ladera.",
                    "En todos, la cronología va antes que la teoría: primero lo que está en el suelo y cómo "
                    "se fechó, después las hipótesis, de la más sobria a la más improbable, con el peso de "
                    "la evidencia de cada una declarado.",
                ],
            },
            "ontem": {
                "titulo": "Descubierto Ayer: hallazgos recientes · Vestígio Oculto",
                "descricao": "Lidar en la Amazonía, papiros de Herculano, denisovanos, Serra da Capivara, "
                             "Anticitera, el Báltico y el ADN fantasma: lo que reveló la tecnología.",
                "intro": [
                    "Descubierto Ayer reúne los hallazgos que solo aparecieron porque la tecnología cambió: "
                    "lidar, tomografía, secuenciación de ADN, sonar — instrumentos nuevos que releen "
                    "evidencias antiguas.",
                    "El láser que atravesó el dosel de la Amazonía y dibujó calles y pirámides de tierra; "
                    "la tomografía sumada al aprendizaje automático que empezó a leer los papiros "
                    "carbonizados de Herculano; el ADN de un fragmento de falange que reveló a los "
                    "denisovanos; el carbón de la Serra da Capivara, en Piauí, que no cabe en la cronología "
                    "de las Américas; los rayos X y la tomografía que leyeron los engranajes del mecanismo "
                    "de Anticitera; la imagen de sonar de la anomalía del Báltico; y el modelo estadístico "
                    "que estimó un ADN fantasma en poblaciones de África Occidental.",
                    "Un descubrimiento reciente no es un caso cerrado. En varios de estos dossieres el dato "
                    "es firme y la interpretación sigue en disputa, y el texto separa una cosa de la otra.",
                ],
            },
            "selado": {
                "titulo": "Archivo Sellado: misterios sin resolver · Vestígio Oculto",
                "descricao": "El manuscrito Voynich, Percy Fawcett, el paso Diatlov, la colonia de Roanoke "
                             "y Kryptos: misterios sin resolver, lo que se sabe y lo que sigue abierto.",
                "intro": [
                    "Archivo Sellado reúne documentos sin descifrar y expediciones sin desenlace: casos en "
                    "los que el registro existe, está preservado — y sigue ilegible o incompleto.",
                    "El manuscrito Voynich, en pergamino auténtico y en un idioma que nadie ha identificado; "
                    "Percy Fawcett, que entró en el Alto Xingú en 1925 tras una ciudad que llamaba “Z” y no "
                    "volvió; los nueve esquiadores del paso Diatlov, en los Urales, en 1959; la colonia de "
                    "Roanoke, que dejó CROATOAN tallado en un poste; y Kryptos, la escultura del patio de la "
                    "CIA cuyo cuarto mensaje sigue con el método desconocido.",
                    "Aquí el misterio rara vez es la falta de un documento. Es el documento que existe y no "
                    "cuadra — y cada dossier muestra lo que ya se descartó, lo que es hipótesis y lo que "
                    "sigue abierto.",
                ],
            },
            "isolados": {
                "titulo": "Últimos Aislados: pueblos aislados · Vestígio Oculto",
                "descricao": "La isla Sentinel del Norte, los mashco piro y los korowai: pueblos fuera de "
                             "alcance, lo que se sabe de ellos y lo que les cuesta nuestra curiosidad.",
                "intro": [
                    "Últimos Aislados reúne territorios y pueblos fuera del alcance del mundo contemporáneo "
                    "— y lo que les cuesta nuestra curiosidad.",
                    "La isla Sentinel del Norte, en el archipiélago de Andamán, cuya población rechaza el "
                    "contacto desde hace generaciones; los mashco piro, descendientes de quienes huyeron de "
                    "las masacres del caucho, en aislamiento voluntario entre Perú y Acre; y los korowai, de "
                    "Papúa, cuyas casas en lo alto de los árboles se convirtieron, en treinta años de "
                    "fotografías, en el retrato de un pueblo entero.",
                    "En estos dossieres el misterio no está enterrado. Casi todo lo que se sabe se vio de "
                    "lejos, y la pregunta cambia: no es solo lo que existe allí, es lo que decidimos no "
                    "preguntar.",
                ],
            },
        },
        # Alt da prévia (og:image) em espanhol: assets/img/og/es/<slug>.jpg,
        # gerada por _src/_og_tmp/gerar_og.py --es (título em TITULO_ES).
        "og_alt": {
            "gobekli-tepe": "Recinto excavado de Göbekli Tepe con pilares en T, bajo el título Göbekli Tepe",
            "amazonia-lidar": "Relieve por lidar con recintos geométricos de tierra en la Amazonía, bajo el título Ciudades de la Amazonía",
            "nadadores-do-saara": "Pintura rupestre de una figura humana en postura de nado en Wadi Sura, bajo el título Los nadadores del Sahara",
            "papiros-herculano": "Rollo de papiro carbonizado de Herculano, bajo el título Los papiros de Herculano",
            "grande-piramide": "Las hiladas de piedra de la Gran Pirámide de Guiza hasta el vértice, bajo el título La Gran Pirámide",
            "nan-madol": "Murallas de basalto columnar de Nan Madol entre la vegetación, bajo el título Nan Madol",
            "denisovanos": "Vista desde el interior de la cueva de Denísova, en el Altái, bajo el título Los denisovanos",
            "serra-da-capivara": "Sedimento con guijarros y grava en la Serra da Capivara, bajo el título Serra da Capivara",
            "manuscrito-voynich": "Hoja plegada del manuscrito Voynich con diagramas circulares, bajo el título El manuscrito Voynich",
            "percy-fawcett": "Retrato de Percy Fawcett en 1911, bajo el título Percy Fawcett",
            "sentinela-do-norte": "La isla Sentinel del Norte vista desde la ventanilla de un avión, bajo el título La isla Sentinel del Norte",
            "anticitera": "Réplica moderna del mecanismo de Anticitera, con los cuadrantes de bronce a la vista, bajo el título El mecanismo de Anticitera",
            "linhas-de-nazca": "El colibrí de las líneas de Nazca visto desde lo alto, bajo el título Las líneas de Nazca",
            "puma-punku": "Bloques de piedra en forma de H en Puma Punku, bajo el título Puma Punku",
            "moais-rapa-nui": "Moáis en la ladera de Rano Raraku, en Isla de Pascua, bajo el título Los moáis de Isla de Pascua",
            "anomalia-do-baltico": "El golfo de Botnia visto por satélite, con hielo en el mar Báltico, bajo el título La anomalía del Báltico",
            "dna-fantasma": "Sala de secuenciadores de ADN, bajo el título El ADN fantasma",
            "passagem-dyatlov": "Valle del río Auspiya, en los Urales, con nieve en los árboles, bajo el título El paso Diatlov",
            "colonia-roanoke": "Mapa de Virginia de Theodor de Bry, 1590, con la isla de Roanoke, bajo el título La colonia de Roanoke",
            "kryptos": "La escultura Kryptos, de Jim Sanborn, bajo el título Kryptos",
            "mashco-piro": "El río Las Piedras serpenteando por la selva amazónica de Perú, bajo el título Los mashco piro",
            "korowai": "Silueta de una casa en el árbol entre palmeras, en Papúa, bajo el título Los korowai",
        },
        "qtd": lambda n: f"{n} dossier" if n == 1 else f"{n} dossieres",
        "contagem_zero": "Próximamente en español",
        "todos": "Todos",
    },
}

# Chaves que todo idioma ativo precisa ter. O build para se faltar alguma.
CHAVES_OBRIGATORIAS = [k for k in T["pt"] if k not in ("temas", "og_alt")]
