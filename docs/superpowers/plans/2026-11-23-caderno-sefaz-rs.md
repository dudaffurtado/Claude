# Caderno de Questões SEFAZ-RS (AFRE) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Gerar um PDF A4 único, pronto para imprimir e encadernar, com ~300 questões inéditas estilo FCC em 12 cadernos, cada um com gabarito comentado ao final.

**Architecture:** Questões em YAML (um arquivo por caderno) → validador Python → renderizador Python que monta HTML com o CSS aprovado na amostra → Playwright gera o PDF.

**Tech Stack:** Python 3 + PyYAML 6, pytest, Node + Playwright (Chromium pré-instalado), fontes Caladea e Inter.

**Spec:** `docs/superpowers/specs/2026-11-23-caderno-sefaz-rs-design.md`

## Global Constraints
- Contagens por caderno: 1 Tributário 45; 2 ICMS/RS 45; 3 Reforma 15; 4 Contab. Geral/Avançada 45; 5 Custos 15; 6 Auditoria 20; 7 Constitucional 20; 8 Administrativo 20; 9 Empresarial 15; 10 Português 25; 11 RLM + Mat. Financeira 20; 12 Estatística 15. Total 300.
- Toda questão: 5 alternativas A–E, exatamente uma correta, nível 1–3, assunto, comentário curto, fundamento.
- Dentro de cada tema, questões em ordem de nível crescente.
- Layout idêntico à amostra aprovada (`amostra/amostra.html`): A4, margem interna 22 mm, 2 colunas, Caladea 9 pt, gabarito 7,6 pt / fundamento 6,4 pt, faixa de respostas compacta (10 por linha).
- Cada caderno começa em página nova; o gabarito do caderno começa em página nova após as questões.
- Legislação vigente em nov./2026; sem números frágeis (alíquotas/prazos regulamentares) sem certeza.

## Review Focus
- Gabarito concentrado numa letra → validador exige que nenhuma letra passe de 30% por caderno (Task 1).
- Questão de itens (I–IV) cuja alternativa cita item inexistente → validador checa numerais romanos (Task 1).
- Comentário que contradiz a letra marcada (ex.: comentário explica "B" mas `resposta: C`) → revisão manual por caderno, checklist na Task 2+.
- Questão longa que estoura uma coluna inteira → checagem visual das páginas renderizadas (Task 2+).
- Ordem de nível violada dentro do tema → validador (Task 1).

---

### Task 1: Pipeline (schema, validador, renderizador, build)

**Files:**
- Create: `caderno/schema.md` (formato YAML documentado em 20 linhas)
- Create: `caderno/validar.py`, `caderno/render.py`, `caderno/estilo.css` (CSS extraído da amostra), `caderno/build.sh`
- Create: `caderno/dados/01-direito-tributario.yaml` (inicial: só o tema 4 da amostra, 5 questões)
- Test: `caderno/tests/test_validar.py`, `caderno/tests/test_render.py`

**Interfaces:**
- Produces: YAML por caderno:
  ```yaml
  caderno: 1
  materia: Direito Tributário
  meta: 45
  temas:
    - titulo: Obrigação Tributária, Fato Gerador e Sujeição Passiva
      base: CTN, arts. 113 a 127
      questoes:
        - nivel: 1            # 1..3
          assunto: Obrigação principal e acessória
          enunciado: "..."
          itens: ["...", "..."]   # opcional (I, II, III...)
          comando: "Está correto o que se afirma APENAS em"  # opcional, após itens
          alternativas: {A: "...", B: "...", C: "...", D: "...", E: "..."}
          resposta: A
          comentario: "..."
          fundamento: "CTN, art. 113, §1º."
  dica: "Olho na FCC: ..."   # opcional, ao fim do gabarito
  ```
- Produces: `validar.carregar(path) -> dict`; `validar.erros(caderno: dict, checar_meta: bool) -> list[str]`
- Produces: `render.html_caderno(caderno: dict, inicio: int) -> tuple[str, str]` (HTML questões, HTML gabarito; numeração global contínua a partir de `inicio`); `render.html_volume(cadernos: list[dict]) -> str` (capa + sumário + cadernos)
- `build.sh` → `caderno/saida/SEFAZ-RS_AFRE_Caderno_de_Questoes.pdf`

- [ ] **Step 1: Testes do validador** — `test_cinco_alternativas` (falta E → erro), `test_resposta_valida` (resposta "F" → erro), `test_nivel_crescente` (níveis 2,1 no mesmo tema → erro), `test_itens_romanos` (alternativa "I e V" com 4 itens → erro), `test_balanco_letras` (8 de 20 com "A" → erro >30%; só quando `checar_meta`), `test_meta` (contagem ≠ meta → erro quando `checar_meta`), `test_amostra_ok` (arquivo inicial → `[]` com `checar_meta=False`).
- [ ] **Step 2:** `pytest caderno/tests -v` → FAIL (módulo inexistente).
- [ ] **Step 3:** Implementar `validar.py`; CLI `python3 caderno/validar.py caderno/dados/*.yaml [--meta]` imprime erros e sai com código 1 se houver.
- [ ] **Step 4: Testes do render** — `test_numeracao_global` (inicio=46 → primeira questão "46"), `test_gabarito_faixa` (12 questões → faixa com 2 linhas: 10 + 2), `test_sem_resposta_nas_questoes` (HTML de questões não contém o texto do `comentario`), `test_volume_tem_sumario` (sumário lista as 12 matérias quando recebidas).
- [ ] **Step 5:** Implementar `render.py` reaproveitando as classes CSS da amostra (`.cols`, `.q`, `.qhead`, `.alt`, `.itens`, `.marca`, `.gtab`, `.gc`, `.pegadinha`); `build.sh` roda validador, render e o PDF via Playwright (`preferCSSPageSize: true`).
- [ ] **Step 6:** `pytest caderno/tests -v` → PASS; `bash caderno/build.sh` gera PDF; conferir página 1 de questões contra a amostra (pdftoppm, olhar).
- [ ] **Step 7:** Commit `feat: pipeline do caderno de questões`.

### Tasks 2–13: Conteúdo, um caderno por task

Uma task por caderno (2 = caderno 1 … 13 = caderno 12), na ordem da tabela de Global Constraints. Cada uma:

**Files:** Create/Modify `caderno/dados/NN-<materia>.yaml`

- [ ] **Step 1:** Definir temas do caderno (3–12 temas, conforme o peso típico da FCC) e escrever as questões até atingir a `meta`; níveis crescentes por tema; misturar formatos (direta, itens I–IV, caso prático, "é correto/incorreto afirmar").
- [ ] **Step 2:** `python3 caderno/validar.py caderno/dados/NN-*.yaml --meta` → sem erros.
- [ ] **Step 3: Revisão de conteúdo** — reler cada questão: (a) exatamente uma alternativa correta; (b) comentário bate com `resposta`; (c) artigo citado existe e diz isso; (d) nenhum número frágil sem certeza; (e) distratores plausíveis no estilo FCC.
- [ ] **Step 4:** `bash caderno/build.sh` e olhar as páginas do caderno (nenhuma alternativa partida, nenhuma questão maior que uma coluna, gabarito em página nova).
- [ ] **Step 5:** Commit `content: caderno NN – <matéria>`.

Notas específicas:
- Caderno 1 já contém o tema 4 da amostra; incorporar e completar.
- Caderno 2 (ICMS/RS): priorizar CF art. 155 §2º, LC 87/96, Lei 8.820/89; RICMS/RS só em regras estáveis.
- Caderno 3 (Reforma): EC 132/2023 e LC 214/2025 — princípios, IBS/CBS, Comitê Gestor, cronograma de transição, Imposto Seletivo.
- Cadernos 11 e 12: cálculos com resposta numérica exata; comentário mostra a conta.

### Task 14: Volume final

**Files:** Modify `caderno/render.py` (capa), Create `caderno/saida/SEFAZ-RS_AFRE_Caderno_de_Questoes.pdf`

- [ ] **Step 1:** `python3 caderno/validar.py caderno/dados/*.yaml --meta` → sem erros, total 300.
- [ ] **Step 2:** `bash caderno/build.sh`; `pdfinfo` → entre 80 e 130 páginas.
- [ ] **Step 3:** Inspeção visual: capa, sumário, primeira e última página de 3 cadernos sorteados.
- [ ] **Step 4:** Commit do PDF + push para `ccr-1fe6f362-obfnlx`; enviar PDF ao usuário.
