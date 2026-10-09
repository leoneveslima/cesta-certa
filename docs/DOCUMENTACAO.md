# Cesta Certa — Documentação

> Fonte de verdade do projeto. **Toda mudança deve ser registrada aqui** (seção afetada + Histórico de versões), no `README.md` e no `CLAUDE.md`.
> Última atualização: 08/10/2026 · Versão atual: **1.4.0 (versionCode 9)**

## 1. Visão geral
App de lista de compras para o mercado brasileiro. Um único arquivo web (`index.html`: HTML + CSS + JS, sem frameworks) empacotado como app Android com Capacitor. Sem servidor próprio, sem conta, sem anúncios. Funciona offline; **só a importação de receita por link usa a internet**.

- Nome na loja: **Cesta Certa: Lista de Compras** (29/30 caracteres) · nome no ícone/cabeçalho: **Cesta Certa**
- `applicationId`: `com.cestacerta.lista` (definitivo). O namespace Java interno continua `com.mylist.compras` (a `MainActivity` fica em `com/mylist/compras/`) — intencional, não renomear.
- Público: uso pessoal/familiar e distribuição gratuita na Play Store (teste fechado primeiro). Monetização futura (versão Pro, pagamento único) está só como ideia.

## 2. Telas e funcionalidades
Navegação inferior: **Lista · Carrinho · Histórico · Ferram. · Config**.

| Tela | O que faz |
|---|---|
| Lista | Itens pendentes por categoria **ou por receita** (seletor "Por categoria / Por receita" aparece quando há itens de receita); botão **🗑️ Limpar lista** (aparece quando a lista tem itens) que abre uma confirmação própria "Tem certeza que quer limpar toda a lista?" com **SIM** (neutro) e **NÃO** (vermelho) — SIM remove todos os itens da lista atual, NÃO cancela; banner com total do carrinho e orçamento; botão flutuante **+** para adicionar item. **Cada bloco (categoria ou receita) é recolhível:** toque no título para esconder/mostrar os itens (seta ▾); o progresso/contagem continua visível no título |
| Carrinho | Itens marcados "no carrinho", mesmo agrupamento da Lista, e o botão **✅ Finalizar compra** (grava a compra no Histórico) |
| Histórico (antes "Stats") | **Comparar mercados** (esta lista em cada mercado), **Compras anteriores** (mercado, data, total; toque para ver os itens ou excluir) e **Gastos do carrinho atual** (total, ticket médio, por categoria) |
| Ferram. | Receita → Lista, Preço por litro, Calculadora de churrasco |
| Config | Renomear/orçamento/excluir lista, tema, trocar de lista, **Backup**, histórico de preços |

### 2.1 Cartão de item
Linha de controles: **[− qtd +]** (a quantidade é um campo numérico digitável; vazio/inválido volta ao valor anterior) · **volume/peso** (só Bebidas = ml e Açougue = g) · **preço unitário**. Botão do carrinho à direita e ✕ para remover.
Linha de baixo (aparece quando há preço): um **pill que define como o preço é calculado** — toque para alternar **por unidade → valor total → por kg (ou por litro)** — mais um detalhe e o **Total da linha**:
- **por unidade** (padrão): Total = preço × quantidade; em Bebidas/Açougue mostra também o preço por litro/kg.
- **valor total**: o preço digitado já é de todas as unidades juntas (ex.: **8 maçãs por R$ 24** → Total R$ 24,00; mostra "R$ 3,00 cada"; mudar a quantidade não altera o total).
- **por kg / por litro**: o preço é R$/kg (R$/L em bebidas) e o campo de **peso** (g) aparece em qualquer categoria; Total = preço × peso (ex.: R$ 24/kg × 1.200 g = R$ 28,80). Sem o peso o total é R$ 0,00 e o app avisa "informe o peso".
`itemTotal(item)` é a **única fonte** do valor da linha (carrinho, banner, orçamento por fonte, estatísticas, histórico, compartilhar e comparação) — nunca multiplicar `price*qty` direto. A comparação entre mercados usa o preço unitário efetivo (`precoUnit`: no modo "valor total" é preço ÷ quantidade) e só compara "por kg" com "por kg"; o peso só vale onde o campo aparece (`volEf`).
Em cartões com campo de volume o controle de quantidade é menor (classe `has-vol`) e o campo de volume comporta 4 dígitos (ex.: 2500 ml). O nome do item quebra em até **2 linhas**; a linha de controles tem `flex-wrap`, então em telas estreitas (≈360 px) o preço desce para a linha de baixo em vez de ficar espremido.
Na tela **Config**, as linhas de configuração têm texto à esquerda (flexível) e botão de tamanho uniforme à direita (`.settings-row`); nomes de lista longos quebram linha. Os chips de lista no topo da Lista truncam com reticências (máx. 220 px).

### 2.2 Orçamento
Por lista (ou por fontes, ver 2.5c). No banner: `Limite: R$ 1.048,00 | 12% usado` — o percentual vem separado por "|" e **muda de cor por faixa**: **< 50% verde · 50–74% amarelo · 75–99% laranja · ≥ 100% vermelho** (mostra o valor real, ex.: 112%; a barra é limitada a 100% e usa as mesmas cores). Alerta laranja a partir de 85% do limite e vermelho ao estourar.

### 2.3 Preço por litro (Ferram.)
Presets de embalagem (lata 350, lata palito 269, latão 473, garrafa 600, litrão 1000, 2 L) ou volume livre; preço ÷ volume × 1000.

### 2.4 Calculadora de churrasco (Ferram.)
Entradas: pessoas, bebedores de cerveja, crianças. Regras: carne = 500 g/adulto + 250 g/criança, dividida em 50% bovina, 25% linguiça, 25% frango; **cada carne é arredondada para múltiplos de 0,5 kg** (x,1–x,5 → x,5; x,6–x,9 → próximo inteiro); pão de alho = 2/adulto + 1/criança; cerveja = 8 latas por bebedor; refrigerante 2 L = ⌈(crianças + não-bebedores) × 0,5 ÷ 2⌉ (mínimo 1). O botão "Adicionar tudo" cria itens na lista atual: cerveja (350 ml), refri (2000 ml) e pão de alho entram com quantidade e volume preenchidos; carnes entram como item com a quantidade (kg) no nome.

### 2.5 Receita → Lista (Ferram.)
1. Cole o **link** da receita **ou** o texto (completo ou só ingredientes) e toque **Ler ingredientes**. Se o campo tiver só um endereço (até 3 linhas contendo uma URL), o app baixa a página e lê nome + ingredientes sozinho; senão lê o texto.
2. Modal de prévia: campo **Nome da receita** (editável; vem do título quando detectado, senão "Receita"), lista com caixinhas e opção **Criar uma nova lista só para esta receita**.
3. Itens que "costumam ter em casa" (água, sal, pimenta, óleo, azeite, gelo) e itens que **já estão na lista** chegam desmarcados.
4. Ao confirmar: itens recebem `recipe = nome` e a tela passa para **Por receita** (cada receita é um bloco com progresso "N/M no carrinho" ou "✅ completo"; itens avulsos ficam em "🛒 Outros itens"). O usuário alterna para "Por categoria" no seletor.

**Receita por link** (desde 1.2.0): `lerReceitaLink(url)` faz `fetch` da página (timeout 20 s; `http://` vira `https://`) e `extrairReceitaHtml(html)` procura, em ordem: (1) **JSON-LD schema.org/Recipe** — escolhe a Recipe com mais `recipeIngredient` (páginas podem ter várias), nome vindo de `name`; (2) **microdata** `itemprop=recipeIngredient`; (3) cabeçalho **"Ingredientes"** seguido de itens `<li>` (subtítulos de grupo viram linhas ignoradas). Título limpo (corta `:`, ` - `, ` | `). As linhas passam por `_itemsDeLinhas` (o mesmo leitor do texto colado) e abrem a prévia. Avisos: sem internet; link que não abre; página sem receita ("Cole o texto dela"). Testado com Nestlé, TudoGostoso e Receiteria. **No app Android** o `fetch` é nativo (`CapacitorHttp` ligado em `capacitor.config.json`), sem bloqueio de CORS; **no navegador/PWA** a maioria dos sites bloqueia a leitura (CORS) e o app pede para colar o texto. A permissão `INTERNET` já existia no Manifest. Instagram e páginas que exigem login não funcionam por link.

**Regras do leitor** (`parseReceita` / `_itemsDeLinhas`, entre `// <recipe-parser>` e `// </recipe-parser>` em `index.html`):
- Bloco de ingredientes: da linha "Ingredientes" até "Modo de preparo/Preparo/Utensílios/…". Sem cabeçalho: usa linhas curtas que começam com marcador ou quantidade.
- Ruído descartado: "Continua após patrocínio", "Veja o passo a passo", "Play", etc. Subtítulos de grupo ("Calda", "Recheio:") são ignorados.
- Quantidade: inteiros, decimais (`,`/`.`), frações (`1/2`, `½`, `1½`, `1 1/2`), "meia", "um/dois…", intervalos ("5 a 10" → 5). Variante "1 xícara e 1/2" → 1,5.
- Unidades: g/grama(s), kg/quilo(s), mg, ml/mililitro(s), l/litro(s), xícara, colher (sopa/chá/café/sobremesa — também "colher **de** sopa"), pitada, dente, folha, rama, lata, pacote, fatia, gomo, medida etc. `(chá)`/`(sopa)` coladas à unidade são preservadas; outros parênteses/colchetes são removidos.
- Nome: remove preparo ("picado", "cortado em cubos", "a gosto", "opcional", "para refogar", "quente"…), adjetivos de tamanho, marca de quantidade no fim; "Sal e pimenta" vira dois itens.
- Destino da quantidade: Açougue em g/kg → campo **peso**; Bebidas em ml/l → campo **volume**; item contável sem unidade ("2 cebolas") → `qty`; demais unidades ("2 colheres (sopa)", "400 g") → anotação no nome (`Nome — 400 g`), `qty = 1`. **Não converte medidas de receita para pacotes.**
- Categoria: `detectCategory` (palavras-chave; ordem das regras importa — Grãos e Enlatados são testados antes de Hortifrúti).

### 2.5b Mercados, compras e comparação de preços (desde 1.3.0)
- **Mercado da compra:** cada lista tem `store`. Aparece no topo do banner ("📍 Supermercados Guanabara"; tocar para trocar), na Config (linha "Mercado") e ao criar a lista. Nomes são sugeridos a partir dos já usados e unificados ignorando maiúscula, acento e espaços extras (`canonMercado`).
- **Finalizar compra** (aba Carrinho): pede mercado e data (hoje por padrão; dá para registrar compras passadas), mostra o total e, se houver histórico, uma comparação com outro mercado. Grava `state.purchases` com os itens do carrinho (nome, categoria, qtd, preço, volume, receita). Duas opções: *remover da lista os itens comprados* (padrão; os pendentes ficam) ou *manter os itens sem preços* para reutilizar a lista.
- **Dica por item** (no cartão, enquanto digita o preço): "▼ R$ 0,30 mais barato que no Guanabara (12/09: R$ 3,49)" / "▲ … mais caro …"; sem preço digitado mostra "Guanabara: R$ 3,49 · 12/09". Compara com o **menor preço entre os outros mercados** (último de cada um). Itens com volume são ajustados proporcionalmente (preço por litro/kg); se só um dos dois tem volume, não compara.
- **Casamento de nomes** (`normNome`/`similar`): ignora acento, maiúscula, pontuação, plural simples, artigos e medidas ("2L", "350ml"); casa quando os nomes normalizados são iguais ou têm ≥ 80% das palavras em comum. "Leite" e "Leite integral" são tratados como produtos diferentes de propósito. Ao adicionar itens, as **sugestões começam pelos nomes já comprados**, para manter os nomes iguais entre compras.
- **Comparar mercados** (aba Histórico): `compararItens` estima, para cada mercado, o total dos itens da lista que têm preço registrado ali; o **veredito** — e o valor mostrado em cada linha do card — usa só os **itens em comum** entre os mercados elegíveis, para a comparação ser justa (mercados sem itens em comum suficientes mostram o total do que cobrem, "cobre n de N itens"). O veredito aparece em tom de alerta (laranja) quando o mercado atual está mais caro (mínimo 3 itens, ou todos se a lista tiver menos; mercado elegível = cobre ≥ 30% da lista e ≥ 2 itens). Se a lista tem mercado definido, ele entra com os **preços digitados hoje** e o texto é do tipo "⚠️ Mundial está R$ 0,80 mais caro que Guanabara nos 3 itens em comum (compra de 12/09)"; sem mercado, compara os dois mais baratos.
- Só passa a ter valor com 2+ compras registradas; com nenhuma, o Histórico orienta o primeiro registro.

### 2.5c Orçamento por fonte (desde 1.3.0)
Config → **Orçamento → Definir** abre o editor de **fontes** (até 4): nome, valor e a opção *só para alimentos* (modelo vale-alimentação). Atalhos: "+ Vale-alimentação", "+ Saldo em conta", "+ Outra". O orçamento da lista (`budget`) passa a ser a **soma** das fontes, então a barra e os alertas continuam como antes. Com fontes, o banner mostra cada uma ("Vale-alimentação 280 de 300 · sobra 20"). **Alocação** (`fundsReport`): limpeza e higiene só saem de fontes gerais; alimentos usam primeiro as fontes "só alimentos" e o que sobrar usa as gerais. Alerta específico quando falta dinheiro, inclusive quando sobra no vale mas limpeza/higiene passam do saldo ("limpeza/higiene não podem usar o vale"). A regra de quais categorias o vale cobre (hoje: tudo exceto Limpeza e Higiene) varia por cartão; bebidas alcoólicas não são detectadas. Criar a lista com um valor único continua funcionando (orçamento simples, sem fontes).

### 2.6 Backup (Config → Backup)
Gera um JSON `{ app:'cesta-certa', v:1, exportedAt, state }` no campo de texto; **Copiar** envia para a área de transferência; **Restaurar** valida o texto colado (listas com `id`, `name`, `items`) e **substitui** os dados atuais após confirmação. Não há backup em nuvem.

### 2.7 Compartilhar
Botão no cabeçalho: monta texto com categorias, itens e total; copiar ou enviar por WhatsApp.

## 3. Modelo de dados (`localStorage`, chave `mylist_v2`)
```js
state = {
  lists: [{ id, name, budget, items: [Item], createdAt }],
  currentListId, priceHistory: { [nomeDoItem]: preco }, theme: 'dark'|'light',
  groupMode: 'cat'|'recipe',           // preferência de agrupamento
  collapsed: { [listId]: { [chave]: 1 } },  // blocos recolhidos; chave = 'l:r:<receita>' | 'l:c:<categoria>' (Lista) ou 'c:…' (Carrinho)
  purchases: [{ id, store, date /*ms (meio-dia local)*/, listName, total, items:[{ name, category, qty, price, vol, recipe, mode:'un'|'total'|'kg', total /*valor da linha*/ }] }],
  stores: [string]                         // mercados já usados (sugestões)
}
// list também pode ter: store (mercado atual) e funds: [{ label, amount, foodOnly }]
Item = { id, name, category, qty, price, inCart, createdAt,
         priceMode?: 'total'|'kg',     // ausente = por unidade (preço × qtd); 'total' = preço já é o total; 'kg' = preço por kg/L × peso (vol)
         vol?: number,                 // ml (Bebidas) ou g (Açougue); 0/ausente = não informado
         recipe?: string }             // nome da receita de origem
```
A chave `mylist_v2` foi mantida de propósito (compatibilidade). Campos novos são opcionais, então dados antigos continuam válidos. Gravação com debounce de 400 ms (`saveState`) ou imediata (`saveNow`).

## 4. Visual
- Paleta **Mercado Moderno**: verde frescor `#10B981` (botões/ativos), azul marinho `#1E293B` (cards, cabeçalho e banner — também no modo claro), laranja `#F59E0B` (destaques de preço/alertas), fundo escuro `#0F172A` e claro `#F8FAFC`. Texto sobre o verde é escuro (`--on-accent`) por contraste.
- Tokens CSS em `:root` e `[data-theme="light"]` no início do `<style>` (`--accent`, `--cyan` = verde de valores, `--hl` = laranja, `--surface*`, `--border*`).
- **Ícone**: sacola branca com check verde e selo laranja sobre fundo verde. Fontes: `icon-source.svg` (completo) e `icon-foreground.svg` (adaptativo); gerar PNGs com `node gen-icons.cjs && node gen-android-icons.cjs`. Cor de fundo do ícone adaptativo: `android/app/src/main/res/values/ic_launcher_background.xml` (`#10B981`).
- **Barra de status (Android 15+)**: o WebView não informa a safe-area do topo de forma confiável. `MainActivity` aplica o padding da barra de status nativamente e pinta o fundo (`#0F172A` janela, `#1E293B` atrás do cabeçalho). O CSS usa só `env(safe-area-inset-bottom)` (`--sab`); `--sat` fica `0px`.

## 5. Android / build
- Capacitor 8, `compileSdk/targetSdk` 36, `minSdk` 24, JDK 21.
- `android/app/build.gradle`: `applicationId "com.cestacerta.lista"`, `versionCode`/`versionName`, assinatura de release lida de `C:\Users\<usuario>\keystore-cestacerta\keystore.properties` (via `user.home`).
- **Chave de assinatura** (`upload.jks` + `keystore.properties`) fica **fora do OneDrive e do projeto**. Fazer backup externo. Com o Play App Signing, a Google guarda a chave definitiva.
- **Build de release** — compilar numa cópia fora do OneDrive (o OneDrive causa `Accessing unreadable inputs`/`AccessDenied` no Gradle):
  1. `robocopy <projeto> C:\Users\<usuario>\build-cestacerta /MIR /XD build .gradle .git store .claude /XF *.apk *.aab`
  2. em `build-cestacerta`: `npx cap sync android`
  3. `cd android` → `gradlew.bat bundleRelease assembleRelease --no-daemon`
  4. copiar `app-release.aab` e `app-release.apk` para `store/CestaCerta-<versão>.{aab,apk}`.
- Antes de gerar: subir `versionCode` (e `versionName`) e o `CACHE` do `sw.js`; espelhar `index.html`/`manifest.json`/`sw.js` em `dist/`.
- **Service worker:** no navegador/PWA é cache-first (versão nova só aparece na 2ª abertura; subir o `CACHE` de `sw.js` a cada mudança). **No app Android ele é desativado** (desde a 1.1.1): o `index.html` detecta `Capacitor.isNativePlatform()`, remove service workers e caches existentes e usa os arquivos embutidos no APK, então uma versão nova aparece na primeira abertura.
- Instalar no celular: `adb install -r store\CestaCerta-<versão>.apk` (mesma assinatura preserva os dados). Conferir o app em foco (`mCurrentFocus`) antes de enviar toques/teclas via adb.
- O app antigo `com.mylist.compras` (My List) é outro pacote; pode coexistir no celular e tem dados de teste próprios.

## 6. Play Store
Ver [`../PLAY-STORE.md`](../PLAY-STORE.md) (passo a passo, textos da ficha, formulário de dados). Materiais prontos em `store/`: AAB, APK, ícone 512, gráfico 1024×500, política de privacidade (HTML; falta preencher o e-mail de contato e hospedar numa URL pública).
Conta pessoal nova: teste fechado com 12+ testadores por 14 dias contínuos antes de pedir produção (confirmar regra atual no Console).
A importação de receita por link usa a internet (já refletido na política de privacidade e na descrição). Futuras funções com câmera/internet (código de barras) exigem nova revisão da política, do formulário de segurança de dados e da descrição.

### 6.1 Capturas de tela (documentação e loja)
Pasta `docs/prints/` (1236×2676, com moldura de celular; versões sem moldura em `docs/prints/sem-moldura/`): `00-visao-geral.png` (4 telas lado a lado), `01-lista-por-receita`, `02-lista-por-categoria`, `03-carrinho`, `04-receita-por-link`, `05-previa-da-receita`, `06-calculadora-de-churrasco`, `07-estatisticas`, `08-configuracoes`, `09-tema-claro`. Usam **dados de exemplo** (nunca a lista real do usuário) e servem também para a ficha da Play Store (usar as versões sem moldura; a loja aceita 320–3840 px).
**Regerar após mudar o visual do app:** espelhar `index.html` em `dist/` → `python tools/gerar-prints.py` (Edge headless, 412 px @3x) → `node tools/moldura-prints.cjs`. Os dados de exemplo ficam no bloco `SEED` do `tools/gerar-prints.py`. Estas capturas são simuladas no computador, não do aparelho físico.

### 6.2 Documento de apresentação do produto
`docs/apresentacao/Cesta-Certa-Apresentacao.pdf` (A4, 11 páginas, pt-BR, tom de usuário final): capa; o que é e para quem; conhecendo o app (5 abas e instalação do APK); passo a passo — **cadastrar lista**, **adicionar itens e acompanhar o total**, **como o preço é calculado** (por unidade / valor total / por kg), **enviar uma receita** (link ou texto, prévia, limitações), **orçamento simples e por fonte** (cores do percentual), **finalizar compra e comparar mercados**; ferramentas e backup; dicas e perguntas frequentes. Fonte: `docs/apresentacao/apresentacao.html` (usa as imagens de `docs/prints/`).
**Atualizar quando o app mudar** (regra do CLAUDE.md): regerar os prints (`python tools/gerar-prints.py` → `node tools/moldura-prints.cjs`), ajustar o texto do HTML e rodar `python tools/gerar-apresentacao.py` (opção `--paginas` salva um PNG por página em `%TEMP%/cesta-apresentacao` para conferir o layout). Gera o PDF pelo Edge (`--print-to-pdf`); o texto de contato foi omitido de propósito (a capa/fecho diz para falar com quem enviou o app).

## 7. Pendências e ideias (backlog)
**Do usuário (Play Store):** conta de desenvolvedor, hospedar política de privacidade, capturas de tela (2–8), 12+ testadores/14 dias, backup da chave.
**Ideias avaliadas, ainda não implementadas:**
- Leitor de código de barras (ML Kit offline + Open Food Facts para o nome, com cache local) — exige permissão de câmera e internet.
- Receber receita pelo botão **Compartilhar** do Android (Instagram/navegador/WhatsApp) — o link por colar já existe; leitura de print/foto (OCR) por último.
- ✅ **Implementado na 1.3.0:** comparar preços entre mercados, aba Histórico e orçamento por fonte (ver 2.5b e 2.5c). Melhorias possíveis: editar uma compra já salva, gráfico de evolução do preço de um item, comparar por categoria, escolher qual compra anterior usar na comparação.
- **Ideia futura a validar — foto da etiqueta de gôndola (proposta do usuário, 08/10/2026):** apontar a câmera para a etiqueta de preço na gôndola e o app preencher **nome e preço** do item, restando ao usuário informar só a quantidade. Resolve o ponto fraco da comparação de preços (depender de digitar). Como validar antes de construir: (1) fotografar 30–50 etiquetas reais de supermercados diferentes (Guanabara, Mundial etc.) com luz ruim/reflexo e ver se a leitura de texto (ML Kit Text Recognition, funciona offline) acerta nome e preço; (2) checar formatos: preço grande "R$ 3,49", preço por kg/L ("R$ 12,45/kg"), promoção "de/por", etiquetas de atacado (preço por quantidade), nomes abreviados; (3) combinar com o **código de barras** da etiqueta (EAN) quando houver, para identificar o produto; (4) sempre mostrar uma **tela de confirmação** com nome e preço lidos (editáveis) antes de adicionar; (5) impacto na loja: permissão de câmera e atualização da política de privacidade/formulário de segurança de dados (processamento no aparelho, nada enviado). Riscos: etiquetas muito variadas, preço lido errado (por isso a confirmação), cobertura de produtos sem etiqueta (hortifrúti por kg).
- Ideia futura a validar: importar a compra pelo QR da nota fiscal (NFC-e) — formato varia por estado e nomes dos itens vêm abreviados.
- Compartilhar lista com a família / backup em nuvem (precisa de servidor) e versão **Pro** (pagamento único R$ 9,90–14,90).
**Limitações atuais:** sem sincronização entre aparelhos; backup é manual (texto); medidas de receita não viram pacotes; `calculadora_*.{css,html,js}` e `MyList.apk` na raiz são obsoletos.

### 7.1 Análise de concorrentes (08/10/2026)
Fontes: buscas na web (blogs e páginas dos próprios apps). **Não verificado direto nas lojas** — conferir antes de usar em material comercial. Legenda: ✅ confirmado em fonte · ⚠️ parcial · ❌ não tem / não encontrei · ? sem confirmação.

| Recurso | Cesta Certa | Bring! | AnyList | Listonic | Out of Milk | Google Keep |
|---|---|---|---|---|---|---|
| Total do carrinho / preço por item | ✅ | ? | ✅ (premium) | ✅ | ✅ | ❌ |
| Orçamento com alerta | ✅ | ? | ? | ? | ? | ❌ |
| Preço por litro/kg | ✅ | ? | ? | ? | ? | ❌ |
| Calculadora de churrasco | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Receita por link → lista | ✅ grátis | ✅ | ✅ (premium) | ? | ⚠️ fraco | ❌ |
| Receita por texto colado | ✅ | ? | ⚠️ | ? | ❌ | ❌ |
| Lista agrupada por receita | ✅ | ? | ? | ? | ❌ | ❌ |
| Sem conta/cadastro | ✅ | ? | ? | ✅ | ? | ❌ (conta Google) |
| Sem anúncios | ✅ | ⚠️ (premium remove) | ? | ⚠️ (pago remove) | ? | ✅ |
| Funciona offline | ✅ | ? | ? | ? | ? | ✅ |
| Listas compartilhadas em tempo real | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Sincroniza entre aparelhos / web | ❌ (backup manual) | ✅ | ✅ (pago) | ✅ | ✅ | ✅ |
| Entrada por voz | ⚠️ (microfone do teclado) | ✅ | ? | ✅ | ✅ | ✅ |
| Código de barras | ❌ (planejado) | ? | ? | ? | ✅ | ❌ |
| Despensa (o que tenho em casa) | ❌ | ? | ? | ? | ✅ | ❌ |
| Planejamento de cardápio | ❌ | ⚠️ | ✅ | ? | ❌ | ❌ |
| Lembrete por local | ❌ | ? | ✅ (premium) | ? | ? | ✅ |
| Sugestões pelo histórico | ⚠️ | ? | ? | ✅ | ✅ | ❌ |
| Alexa / relógio | ❌ | ✅ | ? | ? | ? | ✅ (Google) |
| iOS | ❌ (só Android) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Preço | Grátis (Pro planejado) | Grátis + premium (≈ € 7–14/ano, fontes divergem) | Grátis + US$ 9,99/ano (família US$ 14,99) | Grátis + remover anúncios | Grátis | Grátis |

**Diferenciais do Cesta Certa:** (1) receita por link **grátis**, integrada à lista, com agrupamento por receita, progresso e blocos recolhíveis; (2) controle de gastos no mercado (total ao vivo, orçamento com alerta, preço por litro/kg, volume/peso por item); (3) calculadora de churrasco (nicho brasileiro; nenhum concorrente encontrado tem); (4) privacidade: sem conta, sem anúncios, dados no aparelho; (5) leitor de ingredientes em português (xícara (chá), colher de sopa, "a gosto", frações).
**Lacunas frente aos concorrentes:** compartilhamento e sincronização em tempo real (a maior), voz dedicada, código de barras, despensa, lembretes por local, planejamento de cardápio, integrações (Alexa/relógio), iOS/web e maturidade (avaliações e base de usuários).
**Apps brasileiros** (Lista de compras da TK Solution, ListOn, SoftList): citados em blogs (TK Solution com nota 4,7 e mais de 96 mil avaliações), mas não consegui confirmar as funções; avaliar manualmente nas lojas.

## 8. Histórico de versões
Mais recente primeiro. Formato: data · versão · mudanças.

| Data | Versão | Mudanças |
|---|---|---|
| 09/10/2026 | (sem mudança de versão) | **`docs/portfolio/` (post do LinkedIn) deixou de ser versionado:** removido do GitHub e adicionado ao `.gitignore`; o arquivo continua só na máquina local |
| 09/10/2026 | (sem mudança de versão) | **Post do LinkedIn** (`docs/portfolio/linkedin-post.md`) reescrito para apresentar o app **e** o pipeline `cesta-certa-analytics` (foco em engenharia de dados), com versão curta e texto do primeiro comentário. Não publicado |
| 09/10/2026 | (sem mudança de versão) | **Novo projeto irmão `cesta-certa-analytics`** (pasta `C:\Users\<usuario>\cesta-certa-analytics`, fora do OneDrive; ainda só local, não publicado): pipeline de dados bronze/silver/gold em Python + SQLite que lê o **backup JSON do app** (Config → Backup) e gera comparação entre mercados, índice de preços da cesta e gasto mensal, com quarentena de itens inválidos e testes de qualidade em SQL. Dados sintéticos; reaproveita as regras do app (modos de preço, veredito só sobre itens em comum, `normNome`/`similar`). Nenhuma mudança no app |
| 09/10/2026 | (sem mudança de versão) | **Repositório GitHub** (`leoneveslima/cesta-certa`): removido o nome de usuário do Windows dos documentos (`C:\Users\<usuario>\`) e apagados os arquivos obsoletos `calculadora_*.{css,html,js}` e `MyList.apk` (build antigo `com.mylist.compras`) |
| 08/10/2026 | (sem mudança de versão) | **Portfólio:** projeto preparado para o GitHub — `.gitignore` (exclui `node_modules`, builds, APK/AAB e chaves), `LICENSE` MIT (preencher o nome), seção "Construído com IA (Claude)" e capturas no `README.md`, caminhos pessoais removidos do README; rascunho do post do LinkedIn em `docs/portfolio/linkedin-post.md`. Nada foi publicado ainda |
| 08/10/2026 | (sem mudança de versão) | **Documento de apresentação do produto** (PDF A4, 11 páginas) com o que o app faz e passo a passo ilustrado (cadastrar lista, adicionar itens, modos de preço, enviar receita, orçamento por fonte, finalizar compra e comparar mercados, extras, FAQ). Novos prints (adicionar item, nova lista, modos de preço) e scripts `tools/gerar-apresentacao.py` |
| 08/10/2026 | 1.4.0 (code 9) | **Modos de preço por item:** além de "por unidade", agora **"valor total"** (ex.: 8 maçãs por R$ 24 não multiplica) e **"por kg/litro"** (preço × peso, com campo de peso em qualquer categoria), alternados por um pill na linha de resumo do item; todos os totais passam por `itemTotal()`; histórico guarda modo e total da linha; comparação entre mercados respeita o modo. **Orçamento:** percentual separado do limite por "|" e **cor por faixa** (verde < 50%, amarelo 50–74%, laranja 75–99%, vermelho ≥ 100%), também nas barras das fontes. Corrigido: peso do modo "por kg" ficava escondido no item e atrapalhava a comparação. Testes jsdom (caso das maçãs, modos, faixas de cor) |
| 08/10/2026 | 1.3.0 (code 8) | **Comparação de preços entre mercados (3 fases):** (1) mercado por lista, **Finalizar compra**, aba **Histórico** (substitui Stats) e **dica por item** ("mais barato/mais caro que no Guanabara em 12/09"); (2) **comparação pela lista inteira** com veredito sobre os itens em comum, também no modal de finalizar; (3) **orçamento por fonte** (saldo em conta + vale-alimentação, com alocação por tipo de item e alertas). Sugestões de item começam pelos nomes já comprados; mercados unificados sem acento/maiúscula. Backup inclui compras, mercados e fontes. Estados antigos continuam válidos. Testado em jsdom ponta a ponta (cenário Guanabara × Mundial). Prints novos em `docs/prints/` (histórico/comparação, finalizar compra, orçamento por fonte) |
| 08/10/2026 | (sem mudança de versão) | **Backlog:** ideia de ler nome e preço pela **foto da etiqueta de gôndola** (OCR no aparelho), com plano de validação, registrada na seção 7 |
| 08/10/2026 | (sem mudança de versão) | **Backlog:** proposta de comparação de preços entre mercados + aba Histórico + orçamento por fonte (vale-alimentação/conta), registrada na seção 7 |
| 08/10/2026 | (sem mudança de versão) | **Análise de concorrentes** (seção 7.1): comparação com Bring!, AnyList, Listonic, Out of Milk e Google Keep, diferenciais e lacunas |
| 08/10/2026 | (sem mudança de versão) | **Capturas de tela para documentação/loja** em `docs/prints/` (9 telas + imagem-resumo, com e sem moldura) e scripts `tools/gerar-prints.py` e `tools/moldura-prints.cjs` para regerá-las |
| 08/10/2026 | 1.2.0 (code 7) | **Receita por link:** cole o endereço de uma receita e o app lê nome do prato e ingredientes sozinho (JSON-LD → microdata → cabeçalho "Ingredientes"); `CapacitorHttp` ligado para buscar páginas sem bloqueio de CORS; botão mostra "Buscando receita…"; avisos para sem internet/link inválido/sem receita. Leitor de ingredientes agora entende "gramas", "quilo", "mililitros", "colher **de** sopa" e não transforma "800 gramas" em 99 unidades; "cenoura inteira" → Cenoura. Política de privacidade e textos da loja atualizados (internet só para links). Testado com páginas reais e fluxo de tela em jsdom |
| 08/10/2026 | 1.1.4 (code 6) | **Limpar lista na tela principal:** botão "🗑️ Limpar lista" ao lado do seletor Por categoria/Por receita; abre janela de confirmação própria (não usa `confirm()` do sistema) com SIM e NÃO (NÃO em botão vermelho) e mostra quantos itens serão removidos. O botão antigo saiu da aba Config (que mantém Excluir lista). Validado em jsdom (NÃO mantém os itens, SIM limpa) e em prints |
| 08/10/2026 | 1.1.3 (code 5) | **Correções de layout:** botões da tela Config esticavam e empurravam o texto (agora tamanho uniforme, texto flexível); campo de volume cortava "2500"; nomes de item longos viravam "…" cedo (agora 2 linhas); chip de lista com nome longo cortava (reticências); controles do item quebram linha em telas estreitas. Todas as telas e modais conferidos por prints (Edge headless, 412 px e 360 px; escuro e claro) |
| 08/10/2026 | 1.1.2 (code 4) | **Blocos recolhíveis** na Lista e no Carrinho: tocar no título de uma receita ou categoria esconde/mostra os itens; o estado é salvo por lista (`state.collapsed`) e Lista/Carrinho recolhem de forma independente. Validado em jsdom (recolher, expandir, persistir ao trocar de aba) |
| 08/10/2026 | 1.1.1 (code 3) | **Correção:** a versão com agrupamento por receita não aparecia no celular porque o service worker servia a tela antiga do cache. No app Android o service worker agora é desligado e os caches antigos são apagados; `CACHE` do `sw.js` → `cestacerta-v3`. Fluxo Receita → Lista validado ponta a ponta num navegador simulado (jsdom): ler receita, prévia, confirmar, blocos por receita, alternar Por categoria/Por receita |
| 08/10/2026 | 1.1.0 (code 2) | **Receita → Lista** (leitor de ingredientes pt-BR, prévia com caixinhas, nome editável, itens de despensa/duplicados desmarcados). **Agrupar por receita** com seletor Por categoria/Por receita e progresso por receita. Correções: "1 xícara e 1/2" → 1,5; "Macarrão" não cai mais em Hortifrúti (ordem das regras de categoria); novas palavras-chave (abóbora, canela, louro, cheiro-verde, ovos…). Churrasco: cerveja/refri/pão entram com quantidade e volume. Documentação criada (README, DOCUMENTACAO) e regra de manter docs atualizadas no CLAUDE.md |
| 08/10/2026 | 1.0.0 (code 1) | Primeira versão de release assinada para Play Store: nome **Cesta Certa**, `applicationId com.cestacerta.lista`, **Backup/Restaurar** em texto, assinatura de release (chave fora do OneDrive), materiais da loja (`store/`, `PLAY-STORE.md`), política de privacidade |
| 08/10/2026 | (debug, pré-release) | Campo de **volume/peso** em Bebidas (ml) e Açougue (g) com preço por litro/kg; quantidade digitável; total movido para linha própria; paleta **Mercado Moderno** (verde/azul marinho/laranja) e **ícone novo**; botão + menor e solto; correção do botão de check que cobria o valor; correção da barra de status sobre o app (padding nativo na MainActivity); churrasco com arredondamento 0,5/1 kg; nome "Lista de Compras" → "Cesta Certa" |
| 08/10/2026 | (debug, pré-release) | Nova aba **Ferram.** com **Preço por litro** e **Calculadora de churrasco** (+ "Adicionar tudo à lista"); cache do service worker passa a ser versionado |
| 26/06/2026 | 1.0 (My List) | App original "My List": PWA de arquivo único (lista, carrinho, stats, config), APK debug via Capacitor (`com.mylist.compras`), ícones, instruções de instalação |
