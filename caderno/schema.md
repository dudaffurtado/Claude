# Formato dos arquivos de questões (caderno/dados/NN-materia.yaml)

```yaml
caderno: 1                 # número do caderno (ordem no volume)
materia: Direito Tributário
meta: 45                   # quantidade prevista (checada com --meta)
temas:
  - titulo: Nome do tema
    base: CTN, arts. 113 a 127
    questoes:              # em ordem crescente de nível
      - nivel: 1           # 1 fácil, 2 média, 3 difícil
        assunto: Rótulo curto
        enunciado: Texto (HTML simples permitido: <i>, <u>, <b>)
        itens: [..., ...]  # opcional: afirmações I, II, III...
        comando: Está correto o que se afirma APENAS em   # opcional, após itens
        alternativas: {A: ..., B: ..., C: ..., D: ..., E: ...}
        resposta: A
        comentario: Por que a correta está certa e as erradas, erradas.
        fundamento: Artigo de lei.
dica: Texto opcional no fim do gabarito.
```
