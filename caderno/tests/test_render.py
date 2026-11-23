import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import render  # noqa: E402


def q(i, resposta="A"):
    return {"nivel": 1, "assunto": f"assunto {i}", "enunciado": f"enunciado {i}",
            "alternativas": {k: f"alt {k}" for k in "ABCDE"}, "resposta": resposta,
            "comentario": f"COMENTARIO-SECRETO-{i}", "fundamento": "CTN"}


def cad(n, num=1, materia="Matéria"):
    return {"caderno": num, "materia": materia, "meta": n,
            "temas": [{"titulo": "Tema", "base": "Base", "questoes": [q(i) for i in range(n)]}]}


def test_numeracao_global():
    html_q, _ = render.html_caderno(cad(3), inicio=46)
    assert '<span class="num">46</span>' in html_q
    assert '<span class="num">48</span>' in html_q
    assert '<span class="num">45</span>' not in html_q


def test_gabarito_faixa():
    _, html_g = render.html_caderno(cad(12), inicio=1)
    assert html_g.count('<table class="gtab">') == 2


def test_sem_resposta_nas_questoes():
    html_q, html_g = render.html_caderno(cad(3), inicio=1)
    assert "COMENTARIO-SECRETO" not in html_q
    assert "COMENTARIO-SECRETO-0" in html_g


def test_volume_tem_sumario():
    cads = [cad(2, num=i, materia=f"Materia {i}") for i in range(1, 13)]
    html = render.html_volume(cads)
    assert 'class="sumario"' in html
    for i in range(1, 13):
        assert f"Materia {i}" in html


def test_itens_renderizados():
    c = cad(1)
    c["temas"][0]["questoes"][0]["itens"] = ["primeiro", "segundo"]
    c["temas"][0]["questoes"][0]["comando"] = "Está correto o que se afirma APENAS em"
    html_q, _ = render.html_caderno(c, inicio=1)
    assert "<b>II.</b>" in html_q and "APENAS em" in html_q


def test_texto_do_tema_renderizado():
    c = cad(1)
    c["temas"][0]["texto"] = ["Primeiro parágrafo.", "Segundo parágrafo."]
    html_q, _ = render.html_caderno(c, inicio=1)
    assert '<div class="texto">' in html_q
    assert "<p><b>[2]</b> Segundo parágrafo.</p>" in html_q
    assert html_q.index('class="texto"') < html_q.index('class="q"')


def test_grade_so_para_alternativas_bem_curtas():
    c = cad(1)
    q0 = c["temas"][0]["questoes"][0]
    q0["alternativas"] = {k: "por conglomerados." for k in "ABCDE"}
    html_q, _ = render.html_caderno(c, inicio=1)
    assert "repeat(3,1fr)" not in html_q
    q0["alternativas"] = {k: "I, II e IV." for k in "ABCDE"}
    html_q, _ = render.html_caderno(c, inicio=1)
    assert "repeat(3,1fr)" in html_q


def test_volume_sem_capa_interna():
    cads = [cad(2, num=1, materia="Materia 1")]
    html = render.html_volume(cads)
    assert 'class="capa"' not in html
    assert html.index('class="sumario"') < html.index('class="q"')
