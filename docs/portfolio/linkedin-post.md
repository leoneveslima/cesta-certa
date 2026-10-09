# Post do LinkedIn — Cesta Certa (app + pipeline de dados)

> Rascunho para colar no LinkedIn. Troque os trechos entre [colchetes]. Anexe 3–4 imagens (sugestão: `docs/prints/01`, `07`, `11` e uma captura do `reports/resumo.md` do repositório de analytics) ou o PDF `docs/apresentacao/Cesta-Certa-Apresentacao.pdf` como documento (carrossel).
> Repositórios: https://github.com/leoneveslima/cesta-certa · https://github.com/leoneveslima/cesta-certa-analytics

## Versão principal (≈ 1.800 caracteres)

Construí um app de compras e um pipeline de dados em cima dele. Os dois com ajuda de IA. 🛒📊

**1) O app:** Cesta Certa, uma lista de compras para Android que nasceu de um problema meu. Ele soma o carrinho em tempo real, controla orçamento por vale-alimentação e saldo, transforma o link de uma receita em lista e compara preços entre mercados. Funciona offline, sem cadastro e sem anúncios.

**2) O pipeline:** o app exporta o histórico de compras, e eu montei o Cesta Certa Analytics para transformar isso em respostas: qual mercado é mais barato para a minha cesta? Quanto os preços subiram para mim?

O que tem lá:
→ Camadas bronze → silver → gold
→ Ingestão idempotente (reprocessar o mesmo backup não duplica nada)
→ Quarentena de itens inválidos, com o motivo, em vez de descartar
→ Casamento de produtos ("ARROZ BRANCO 5 KG" = "Arroz branco") com similaridade + aliases curados
→ Índice de preços da cesta (base 100) e comparação de mercados só sobre itens em comum
→ 7 testes de qualidade em SQL, com severidade (erro quebra o pipeline, alerta só avisa)
→ 10 testes automatizados em Python

**Como foi feito:** com o Claude (Anthropic), via Claude Code. Eu defini o problema e as regras de negócio, testei no celular, revisei as decisões e validei os resultados. A IA implementou, testou e documentou.

Um aprendizado honesto: planejei usar DuckDB e dbt, mas o dbt não roda no meu Python 3.14 e o DuckDB foi bloqueado por uma política de segurança do Windows. Em vez de contornar, usei SQLite com SQL puro e deixei a migração registrada como próximo passo. Os dados do pipeline são sintéticos.

Próximo passo: ler notas fiscais (NFC-e) pelo QR Code para alimentar o pipeline com dados reais.

Código aberto (MIT) nos comentários 👇

#EngenhariaDeDados #Python #SQL #Android #IA #ClaudeCode #Portfolio

**Primeiro comentário:**
App: https://github.com/leoneveslima/cesta-certa
Pipeline de dados: https://github.com/leoneveslima/cesta-certa-analytics

---

## Versão curta (≈ 700 caracteres)

Criei um app de lista de compras para Android e um pipeline de dados sobre ele, ambos com ajuda do Claude (Anthropic). 🛒📊

O app compara preços entre mercados e controla orçamento por vale-alimentação. O pipeline (Python + SQL, camadas bronze/silver/gold) ingere o histórico de compras, isola itens inválidos, casa produtos com nomes diferentes e calcula um índice de preços da cesta, com testes de qualidade.

Eu defini o problema e validei; a IA implementou e documentou. Dados sintéticos, código aberto.

App e pipeline nos comentários 👇

#EngenhariaDeDados #Python #SQL #ClaudeCode

---

## Dicas de publicação
- **Imagem de abertura:** uma captura do `resumo.md` (tabelas de comparação e índice) mostra o lado de dados; um print do app (`01-lista-por-receita`) mostra o produto. O carrossel com as duas funciona bem.
- **Links no primeiro comentário:** o LinkedIn reduz o alcance de posts com link no corpo.
- **Transparência sobre a IA** é o diferencial: diga o que você decidiu e o que a IA executou.
- **Não escreva "disponível na Play Store":** o app ainda não foi publicado lá.
- Os dados e os prints usam exemplos sintéticos (nada da sua lista real).
