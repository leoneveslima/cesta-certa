# Post do LinkedIn — Cesta Certa

> Rascunho para colar no LinkedIn. Troque os trechos entre [colchetes]. Anexe 3–4 imagens de `docs/prints/` (sugestão: `01`, `07`, `11`, `05`) ou o PDF `docs/apresentacao/Cesta-Certa-Apresentacao.pdf` como documento (carrossel).

## Versão principal (≈ 1.500 caracteres)

Construí um app Android do zero, conversando com uma IA. 🛒

Chama **Cesta Certa: Lista de Compras** e nasceu de um problema meu: no mercado, eu perdia o controle do total e esquecia ingredientes de receita.

O que ele faz:
✅ Total do carrinho em tempo real
✅ Orçamento por fonte (vale-alimentação + saldo em conta)
✅ Cole o link de uma receita e os ingredientes viram lista
✅ Compara preços entre mercados que eu frequento
✅ Calculadora de churrasco e preço por litro/kg
✅ Funciona offline, sem cadastro e sem anúncios

**Como foi feito:** o código foi escrito com o Claude (Anthropic), via Claude Code. Eu fiz o papel de produto e QA: defini o que o app precisava fazer, testei no meu celular, apontei o que estava errado (botão tapando valor, receita que não agrupava...) e decidi as prioridades. A IA implementou, testou e documentou.

Meu aprendizado:
→ IA acelera muito a implementação, mas não substitui saber o que construir
→ Pedidos pequenos e incrementais funcionaram melhor que um "faça tudo"
→ Documentação virou parte da entrega (o repositório tem histórico de versões, regras e decisões)
→ Testar no aparelho real revela o que nenhum teste automático mostra

Stack: HTML/CSS/JS (PWA de arquivo único) + Capacitor 8 para Android, dados locais, build assinado para a Play Store.

O código está aberto (licença MIT) 👇
[link do GitHub]

Se você usa vale-alimentação ou monta lista de compras por receita, adoraria seu feedback. [Se quiser testar o app, me chame.]

#Android #IA #ClaudeCode #DesenvolvimentoDeSoftware #Capacitor #PWA #Portfolio #ProductBuilding

---

## Versão curta (≈ 600 caracteres)

Criei um app de lista de compras para Android conversando com o Claude (Anthropic). 🛒

Eu defini o produto, testei no celular e priorizei. A IA escreveu o código, os testes e a documentação.

Ele soma o carrinho em tempo real, controla orçamento por vale-alimentação e saldo, transforma o link de uma receita em lista e compara preços entre mercados. Offline, sem cadastro, sem anúncios.

Código aberto: [link do GitHub]

#IA #ClaudeCode #Android #Portfolio

---

## Dicas de publicação
- **Imagem de abertura:** o print `01-lista-por-receita` ou a página 1 do PDF. Posts com imagem ou documento rendem mais.
- **Primeiro comentário:** coloque o link do GitHub (o LinkedIn reduz o alcance de posts com link no corpo).
- **Honestidade sobre a IA** é o diferencial do post: diga o que você decidiu e o que a IA executou.
- Os prints usam dados de exemplo (nada da sua lista real).
