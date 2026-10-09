# Cesta Certa — Publicação na Play Store (teste gratuito)

Nome: **Cesta Certa: Lista de Compras** · `applicationId`: `com.cestacerta.lista` (não muda mais depois de publicado) · Versão **1.4.0 (versionCode 9)**
Documentação completa e histórico: [`docs/DOCUMENTACAO.md`](docs/DOCUMENTACAO.md)

## Arquivos prontos (pasta `store/`)
| Arquivo | Uso |
|---|---|
| `CestaCerta-1.4.0.aab` | Pacote assinado para enviar ao Play Console |
| `CestaCerta-1.2.0.apk` | Mesmo build para instalar direto no celular (testes) |
| `icone-512.png` | Ícone do app na loja (512×512) |
| `feature-graphic-1024x500.png` | Imagem de destaque (1024×500) |
| `politica-de-privacidade.html` | Hospedar numa URL pública (obrigatório) |

## Chave de assinatura — GUARDE EM LUGAR SEGURO
Pasta: `C:\Users\<usuario>\keystore-cestacerta\` (`upload.jks` + `keystore.properties` com a senha).
Fica **fora do OneDrive de propósito**. Faça cópia em pendrive ou cofre de senhas. Ao ativar o *Play App Signing* (padrão), a Google guarda a chave definitiva e esta é só a chave de envio — se perdê-la, dá para pedir reset à Google, mas dá trabalho.
Para gerar um novo AAB: compile na cópia fora do OneDrive (ver README/DOCUMENTACAO §5) e suba `versionCode` em `android/app/build.gradle` a cada envio.

## Passo a passo (só você consegue fazer: exige login, identidade e pagamento)
1. **Conta**: https://play.google.com/console → conta de desenvolvedor **pessoal**, taxa única ≈ US$ 25, verificação de identidade (documento) e do telefone.
2. **Política de privacidade**: publicar `store/politica-de-privacidade.html` numa URL pública (ex.: GitHub Pages) **depois de trocar `[SEU E-MAIL DE CONTATO]`** pelo seu e-mail.
3. **Criar app**: nome `Cesta Certa: Lista de Compras`, idioma pt-BR, tipo *App*, *Gratuito*.
4. **Ficha da loja**: usar os textos abaixo + ícone, gráfico de destaque e **mín. 2 capturas de tela** do celular (tire no app já com alguns itens de exemplo).
5. **Conteúdo do app** (Painel → Configurar): política de privacidade (URL), anúncios = **Não**, acesso ao app = sem restrição, público-alvo = 18+ ou geral (sem foco em crianças), classificação de conteúdo (questionário: tudo "não" → Livre), segurança dos dados (abaixo), categoria **Compras** ou **Produtividade** (sugestão: *Compras*).
6. **Teste fechado**: *Testes → Teste fechado* → criar faixa, enviar o `.aab`, adicionar uma lista de e-mails (Gmail) de **12+ testadores** e mandar o link de convite para eles.
7. **Aguardar 14 dias** com os 12+ testadores **continuamente** inscritos (quem sair pode reiniciar a contagem). Peça que abram o app de vez em quando.
8. **Pedir acesso à produção** no Painel quando liberar → enviar a versão para *Produção*. Revisão da Google leva de horas a poucos dias.

> A regra dos 12 testadores/14 dias vale para contas pessoais novas. Confira o texto atual da Google no Console — ele pode mudar.

## Textos da ficha da loja (pt-BR)

**Título (29/30):** `Cesta Certa: Lista de Compras`

**Descrição curta (≤80):**
`Lista de compras com total em tempo real, preço por litro e churrasco.`

**Descrição completa:**
```
Faça a compra do mercado sem susto no caixa. O Cesta Certa mostra o total do carrinho em tempo real e avisa quando você chega perto do limite do orçamento.

🛒 LISTA E CARRINHO
• Monte várias listas (compra do mês, feira, churrasco…)
• Itens organizados por categoria: açougue, hortifrúti, bebidas, padaria e mais
• Marque o que já está no carrinho e veja o total subir na hora
• Quantidade digitável: use + e − ou digite números grandes direto

💰 CONTROLE DE GASTOS
• Orçamento por fonte: some saldo em conta e vale-alimentação e veja quanto sobra em cada um
• Compare mercados: informe onde está comprando, finalize a compra e o app mostra se cada item está mais barato ou mais caro que no outro mercado, e em qual mercado a sua lista sai mais barata
• Defina um orçamento e receba alertas ao chegar perto do limite
• Escolha como o preço é calculado em cada item: por unidade, valor total (8 maçãs por R$ 24) ou por quilo
• Preço por litro (bebidas) e por quilo (carnes) calculado automaticamente
• Histórico de preços: o app lembra quanto você pagou antes
• Estatísticas por categoria

🧮 FERRAMENTAS
• Receita para lista: cole o link de uma receita (o app lê o nome e os ingredientes sozinho) ou o texto dela; veja a lista por receita para não esquecer nada
• Preço por litro: compare latas, garrafas e embalagens e descubra a mais barata
• Calculadora de churrasco: carne, linguiça, frango, pão de alho, cerveja e refri por número de pessoas, com arredondamento prático para o açougue — e adiciona tudo na sua lista com um toque

🔒 PRIVADO E SIMPLES
• Funciona offline (só a leitura de receita por link usa a internet), sem cadastro e sem anúncios
• Seus dados ficam só no seu celular
• Backup e restauração em texto para trocar de aparelho
• Modo escuro e claro

Feito para o mercado brasileiro. Baixe e compre com mais controle.
```

**Notas da versão 1.4.0:** `Novo: preço por unidade, valor total ou por quilo em cada item; percentual do orçamento com cores. Também: informe o mercado, finalize a compra e compare preços entre mercados; orçamento por fonte (conta + vale-alimentação); aba Histórico. Também: cole o link de uma receita e o app lê o nome e os ingredientes sozinho (ou cole o texto), monta a lista de ingredientes, com visão separada por receita e blocos que você pode recolher. Também: lista, carrinho com total em tempo real, orçamento, preço por litro/kg, calculadora de churrasco e backup.`

## Segurança dos dados (formulário)
- O app coleta ou compartilha dados de usuário? **Não.** (A leitura de receita por link baixa a página no próprio aparelho, por ação do usuário; o endereço vai só ao site da receita, nada vai para nós. Ao preencher o formulário, revise se a Google considera isso "compartilhamento" e, na dúvida, descreva na política.)
- Dados criptografados em trânsito / exclusão: não se aplica (nenhum dado sai do aparelho).
- Política de privacidade: URL do passo 2.

## Antes de enviar a produção
- [ ] E-mail de contato preenchido na política de privacidade e publicada
- [ ] Capturas de tela tiradas (2 a 8)
- [ ] Backup da pasta `keystore-cestacerta`
- [ ] 12+ testadores com convite aceito, 14 dias completos
- [ ] Versão testada em pelo menos 2 aparelhos diferentes (se possível)

## Melhorias para depois do lançamento
Compartilhar lista com a família (exige servidor), backup em nuvem, versão Pro (pagamento único) — ver conversa de estratégia.
