import copy
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import validar  # noqa: E402

DADOS = pathlib.Path(__file__).resolve().parents[1] / "dados"


def q(resposta="A", nivel=1, alternativas=None, itens=None):
    return {
        "nivel": nivel,
        "assunto": "x",
        "enunciado": "x",
        "alternativas": alternativas or {k: k for k in "ABCDE"},
        "resposta": resposta,
        "comentario": "c",
        "fundamento": "f",
        **({"itens": itens} if itens else {}),
    }


def cad(questoes, meta=None):
    return {"caderno": 1, "materia": "M", "meta": meta or len(questoes),
            "temas": [{"titulo": "T", "base": "B", "questoes": questoes}]}


def test_cinco_alternativas():
    c = cad([q(alternativas={k: k for k in "ABCD"})])
    assert any("alternativas" in e for e in validar.erros(c, checar_meta=False))


def test_resposta_valida():
    c = cad([q(resposta="F")])
    assert any("resposta" in e for e in validar.erros(c, checar_meta=False))


def test_nivel_crescente():
    c = cad([q(nivel=2), q(nivel=1)])
    assert any("nível" in e for e in validar.erros(c, checar_meta=False))


def test_itens_romanos():
    alts = {"A": "I e II.", "B": "I e V.", "C": "II e IV.", "D": "III.", "E": "IV."}
    c = cad([q(alternativas=alts, itens=["a", "b", "c", "d"])])
    assert any("item" in e for e in validar.erros(c, checar_meta=False))


def test_itens_romanos_validos_ok():
    alts = {"A": "I e II.", "B": "I e III.", "C": "II e IV.", "D": "I, III e IV.", "E": "II, III e IV."}
    c = cad([q(alternativas=alts, itens=["a", "b", "c", "d"])])
    assert validar.erros(c, checar_meta=False) == []


def test_balanco_letras():
    qs = [q("A") for _ in range(8)] + [q(l) for l in "BCDE" * 3]
    c = cad(qs)
    assert any("letra" in e for e in validar.erros(c, checar_meta=True))
    assert validar.erros(c, checar_meta=False) == []


def test_meta():
    c = cad([q(l) for l in "ABCDE"], meta=6)
    assert any("meta" in e for e in validar.erros(c, checar_meta=True))


def test_campos_obrigatorios():
    item = q()
    del item["comentario"]
    assert any("comentario" in e for e in validar.erros(cad([item]), checar_meta=False))


def test_amostra_ok():
    c = validar.carregar(DADOS / "01-direito-tributario.yaml")
    assert validar.erros(c, checar_meta=False) == []
