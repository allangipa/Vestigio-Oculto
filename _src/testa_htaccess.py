# Uso: python _src/testa_htaccess.py .htaccess
"""Emula as regras de mod_rewrite do .htaccess do Vestígio Oculto (só o que
usamos: RewriteCond com %{HTTP_HOST}/%{HTTPS}/%{REQUEST_URI}, [NC], [OR],
RewriteRule ^ alvo [R=301,L] e RewriteRule padrão - [F]). Mesmo motor do
testa_htaccess.py dos sites Arquitetura do Impossível e Xadrez Bélico.
Sai com código 1 se algum caso não der o resultado esperado."""
import re, sys
def regras(arq):
    out, conds = [], []
    for l in open(arq, encoding="utf-8"):
        l = l.strip()
        if l.startswith("RewriteCond"):
            _, var, pad, *fl = l.split(None, 3)
            fl = fl[0].strip("[]").split(",") if fl else []
            conds.append((var, pad, fl))
        elif l.startswith("RewriteRule"):
            _, pad, alvo, fl = l.split(None, 3)
            out.append((conds, pad, alvo, fl)); conds = []
    return out
def roda(arq, host, https, uri):
    env = {"%{HTTP_HOST}": host, "%{HTTPS}": "on" if https else "off", "%{REQUEST_URI}": uri}
    for conds, pad, alvo, fl in regras(arq):
        ok, acum = True, None
        for var, p, f in conds:
            neg = p.startswith("!"); p = p.lstrip("!")
            r = bool(re.search(p, env[var], re.I if "NC" in f else 0)) != neg
            acum = r if acum is None else (acum or r) if prev_or else (acum and r)
            prev_or = "OR" in f
            if acum is False and not prev_or: break
        if (acum is None or acum) and re.search(pad, uri.lstrip("/")):
            dest = alvo.replace("%{REQUEST_URI}", uri)
            return dest
    return None
P = "https://vestigiooculto.com"
casos = [
    # (host, https, caminho pedido, resultado esperado: URL do 301, "200" ou "403")
    ("vestigiooculto.com.br", True, "/", P + "/"),
    ("www.vestigiooculto.com.br", False, "/dossies/gobekli-tepe.html?x=1", P + "/dossies/gobekli-tepe.html"),
    ("WWW.VESTIGIOOCULTO.COM.BR", True, "/en/dossies/gobekli-tepe.html", P + "/en/dossies/gobekli-tepe.html"),
    ("www.vestigiooculto.com", True, "/temas/pedra-e-poeira.html", P + "/temas/pedra-e-poeira.html"),
    ("vestigiooculto.com", False, "/sobre.html", P + "/sobre.html"),
    ("vestigiooculto.com", True, "/dossies/gobekli-tepe.html", "200"),
    ("vestigiooculto.com", True, "/en/", "200"),
    ("concealedpast.com", True, "/", P + "/en/"),
    ("www.concealedpast.com", False, "/dossies/gobekli-tepe.html", P + "/en/dossies/gobekli-tepe.html"),
    ("concealedpast.com", True, "/sobre.html?a=b", P + "/en/sobre.html"),
    ("concealedpast.com", True, "/en/dossies/gobekli-tepe.html", P + "/en/dossies/gobekli-tepe.html"),
    ("concealedpast.com", True, "/assets/img/og/gobekli-tepe.jpg", P + "/assets/img/og/gobekli-tepe.jpg"),
    ("concealedpast.com", True, "/robots.txt", P + "/robots.txt"),
    ("concealedpast.com", True, "/sitemap.xml", P + "/sitemap.xml"),
    ("CONCEALEDPAST.COM.", True, "/temas/pedra-e-poeira.html", P + "/en/temas/pedra-e-poeira.html"),
    ("vestigiooculto.com", True, "/_src/build.py", "403"),
    ("vestigiooculto.com", True, "/README.md", "403"),
    ("vestigiooculto.com.br", True, "/_src/build.py", P + "/_src/build.py"),
    ("algo.hostingersite.com", True, "/", "200"),
]
falhas = 0
for h, s, u, esperado in casos:
    d = roda(sys.argv[1], h, s, u.split("?")[0])
    q = ("?" + u.split("?")[1]) if "?" in u and d and d != "-" else ""
    obtido = "403" if d == "-" else (d or "200")
    ok = obtido == esperado
    falhas += not ok
    print(f"{'ok ' if ok else 'ERRO'} {'https' if s else 'http '}://{h}{u:40} -> "
          f"{('301 ' + obtido + q) if obtido not in ('200', '403') else obtido}"
          + ("" if ok else f"   (esperado {esperado})"))
print("sem erros" if not falhas else f"{falhas} caso(s) errado(s)")
sys.exit(1 if falhas else 0)
