"""3 opções minimalistas de quarta capa no estilo da capa escolhida. Uso: python3 gerar_quarta_minimal.py"""
import pathlib
from gerar_capas2 import AVISO, estrela_raios

AQUI = pathlib.Path(__file__).resolve().parent
CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
:root { --bege:#e8dac7; --creme:#fbf5ec; --laranja:#ee8a58; --rosa:#e6a3c8; --marrom:#6e5140; }
body { -webkit-print-color-adjust: exact; print-color-adjust: exact; font-family:"DM Sans",sans-serif; }
.pg { width:210mm; height:297mm; position:relative; overflow:hidden; background:var(--bege); color:var(--marrom); }
.aviso { position:absolute; left:0; right:0; bottom:11mm; text-align:center; font-size:6.4pt; opacity:.6; padding:0 40mm; line-height:1.4; }
.it { font-family:"Fraunces",serif; font-style:italic; font-weight:400; }
.caps { font-size:8pt; letter-spacing:.32em; text-transform:uppercase; font-weight:600; }
"""


def pagina(corpo, extra_css=""):
    return ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Quarta capa</title>'
            f'<link rel="stylesheet" href="fontes/fontes.css"><style>{CSS}{extra_css}</style></head><body>'
            f'<section class="pg">{corpo}<div class="aviso">{AVISO}</div></section></body></html>')


def opcao_a():
    """Só a frase, centralizada."""
    css = """
.centro { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; }
.frase { font-size:30pt; line-height:1.15; }
.frase b { font-weight:400; color:var(--laranja); }
.fio { width:14mm; height:1.2pt; background:var(--laranja); margin:9mm 0 6mm; }
"""
    corpo = ('<div class="centro"><div class="frase it">Questão por questão,<br><b>a aprovação vem.</b></div>'
             '<div class="fio"></div><div class="caps">SEFAZ-RS · 2027</div></div>')
    return pagina(corpo, css)


def opcao_b():
    """Só a escrita, no terço inferior."""
    css = """
.sol { position:absolute; left:50%; top:96mm; width:70mm; height:70mm; transform:translateX(-50%); }
.info { position:absolute; left:0; right:0; top:206mm; text-align:center; }
.info .it { font-size:20pt; margin-bottom:5mm; }
"""
    corpo = ('<div class="info"><div class="it">Caderno de Questões</div>'
             '<div class="caps">300 questões · 12 cadernos · estilo FCC</div></div>')
    return pagina(corpo, css)


def opcao_c():
    """Palavra gigante cortada na base, com um selo rosa pequeno."""
    css = """
.aviso { top:11mm; bottom:auto; }
.gigante { position:absolute; left:-10mm; right:-10mm; bottom:-11mm; text-align:center; font-size:140pt; line-height:1; color:var(--creme); }
.selo { position:absolute; left:50%; top:104mm; transform:translateX(-50%) rotate(-6deg); width:48mm; height:48mm; border-radius:50%;
        background:var(--rosa); color:var(--creme); display:flex; align-items:center; justify-content:center; text-align:center; font-size:15pt; line-height:1.1; }
"""
    corpo = ('<div class="selo it">rumo à<br>aprovação</div>'
             '<div class="gigante it">Auditor</div>')
    return pagina(corpo, css)


if __name__ == "__main__":
    for nome, f in (("a", opcao_a), ("b", opcao_b), ("c", opcao_c)):
        (AQUI / f"quarta-minimal-{nome}.html").write_text(f(), encoding="utf-8")
    print("ok")
