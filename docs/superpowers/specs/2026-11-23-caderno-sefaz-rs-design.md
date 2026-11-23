# Caderno de Questões SEFAZ-RS (Auditor-Fiscal) — Design

## Intenção
Material impresso e encadernado para estudar resolvendo questões à mão, mirando o concurso de
Auditor-Fiscal da Receita Estadual (AFRE) da SEFAZ-RS, previsto para 2027, com banca FCC
(contratada em nov./2026; edital ainda não publicado). Estudante iniciante.

## Objetivos
- ~300 questões inéditas, estilo FCC (5 alternativas A–E, cobrança literal da lei, itens I–IV, casos práticos).
- Organizadas por matéria → tema; dificuldade crescente (● ●● ●●●) dentro de cada tema.
- Gabarito com letra + comentário curto + fundamento legal, no fim de cada caderno (matéria).
- Conteúdo atualizado à legislação vigente em nov./2026, incluindo Reforma Tributária (EC 132/2023, LC 214/2025).

## Não-objetivos / anti-objetivos
- Não reproduzir questões reais de provas (risco de enunciado/gabarito errado e desatualizado).
- Não errar a lei: gabarito errado é pior que questão nenhuma. Evitar números frágeis (alíquotas,
  prazos regulamentares) quando não houver certeza; preferir regras estáveis da CF, CTN, LC 87/96, Lei 8.820/89.

## Distribuição (aprovada)
| Caderno | Matéria | Qtd |
|---|---|---|
| 1 | Direito Tributário (CTN e CF) | 45 |
| 2 | ICMS/RS (CF art. 155, LC 87/96, Lei 8.820/89, RICMS) | 45 |
| 3 | Reforma Tributária (IBS/CBS) | 15 |
| 4 | Contabilidade Geral e Avançada | 45 |
| 5 | Contabilidade de Custos | 15 |
| 6 | Auditoria | 20 |
| 7 | Direito Constitucional | 20 |
| 8 | Direito Administrativo | 20 |
| 9 | Direito Empresarial | 15 |
| 10 | Língua Portuguesa | 25 |
| 11 | Raciocínio Lógico e Matemática Financeira | 20 |
| 12 | Estatística | 15 |

## Formato (aprovado na amostra `amostra/amostra-sefaz-rs.pdf`)
- A4, margem interna 22 mm para encadernação; 2 colunas; corpo Caladea 9 pt; títulos Inter.
- Questão pode continuar na coluna seguinte; alternativa nunca é partida.
- Por questão: número, nível, assunto, bolhas A–E, caixas “dúvida/revisar”, linha de anotação.
- Abertura de tema: nome, base legal, tabela de controle (1ª resolução / revisão).
- Gabarito: faixa compacta de respostas (10 por linha), comentários em 7,6 pt, fundamento em 6,4 pt, 2 colunas.

## Abordagens consideradas
1. **Inéditas estilo FCC (escolhida)** — atualizadas, inclusive Reforma; não são questões reais.
2. Reais de provas anteriores — descartada: reprodução de memória não confiável, muitas desatualizadas.
3. Inéditas + roteiro de filtros para questões reais — descartada pelo usuário.

## Decisões do builder (minhas)
- Questões em YAML por caderno; script Python gera HTML a partir do CSS da amostra; Playwright gera o PDF.
- Volume único com capa, sumário e os 12 cadernos; cada caderno começa em página nova.
- Nota na capa: questões inéditas, legislação vigente em nov./2026, ajustar quando o edital sair.
