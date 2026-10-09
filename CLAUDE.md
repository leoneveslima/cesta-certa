# CLAUDE.md - Cesta Certa Context

## ⚠️ REGRA Nº 1 — Documentação é parte da entrega
**Toda atualização do projeto (código, visual, build, loja, decisão) deve ser registrada na MESMA sessão, antes de dar a tarefa como concluída:**
1. `docs/DOCUMENTACAO.md` → seção afetada **+ nova linha no Histórico de versões** (data, versão, o que mudou).
2. `README.md` → se mudou funcionalidade, requisito, comando ou estado do projeto.
3. `CLAUDE.md` (este arquivo) → se mudou estado, versão, caminho, comando ou regra.
4. `PLAY-STORE.md` → se afetou loja, textos da ficha, permissões, política de privacidade ou formulário de dados.
Ao encerrar uma entrega, confirme ao usuário em uma linha quais docs foram atualizados. Se nada precisou mudar, diga isso.

## Contexto Rápido
App **Cesta Certa: Lista de Compras** (ex-"My List"): PWA em arquivo único + Android via Capacitor. `applicationId` `com.cestacerta.lista` (NÃO muda mais). Versão atual: **1.4.0 (versionCode 9)**.
Sem backend próprio, sem sync, offline (exceto importar receita por link, que usa `CapacitorHttp` nativo). Dados em `localStorage` (chave `mylist_v2`, mantida por compatibilidade).
Estado: pronto para Play Store (teste fechado) — passos em `PLAY-STORE.md`. Pendentes do usuário: conta Play Console, política de privacidade publicada, capturas de tela, 12 testadores por 14 dias.
Docs completos: `docs/DOCUMENTACAO.md` (arquitetura, modelo de dados, regras, build, histórico).

## Projeto irmão
`C:\Users\<usuario>\cesta-certa-analytics` (repositório separado, Python + SQLite): pipeline de dados que lê o **backup JSON do app** (`backupJSON()`: `{app:'cesta-certa',v:1,state:{purchases:[...]}}`). **Se o formato do backup ou de `state.purchases` mudar, atualizar o parser (`pipeline.ingerir`) e o gerador sintético de lá.**

## Arquivos Chave
- `index.html` / `dist/index.html`: telas (Lista, Carrinho, **Histórico** (ex-Stats), Ferram., Config), CSS e JS. **Edite `index.html` e espelhe em `dist/`.**
- `sw.js` (+ `dist/sw.js`): service worker cache-first, só para navegador/PWA (no app Android é desligado pelo `index.html`); subir `CACHE` `cestacerta-vN` a cada mudança web.
- `capacitor.config.json` (`webDir: dist`), `manifest.json`.
- `android/`: projeto nativo. `MainActivity.java` aplica o padding da barra de status. `app/build.gradle`: `applicationId`, `versionCode/Name`, assinatura.
- `store/`: AAB/APK de release, ícone 512, gráfico 1024×500, política de privacidade.
- `docs/apresentacao/`: PDF de apresentação do produto (+ HTML-fonte). **Atualizar o texto/prints e regerar (`python tools/gerar-apresentacao.py`) quando uma funcionalidade mudar.**
- `docs/portfolio/linkedin-post.md`: rascunho do post de portfólio. `.gitignore` e `LICENSE` (MIT) prontos para publicar no GitHub; o projeto declara no README que foi **construído com IA (Claude)** — manter essa transparência.
- `docs/prints/` + `tools/`: capturas de tela com dados de exemplo e os scripts que as geram (`python tools/gerar-prints.py` → `node tools/moldura-prints.cjs`). Regerar sempre que o visual mudar.
- Chave de assinatura FORA do projeto: `C:\Users\<usuario>\keystore-cestacerta\` (nunca no OneDrive/commit).

## Comandos Úteis
- Sync: `npx cap sync android`
- **Build de release (use a cópia fora do OneDrive — o OneDrive quebra o Gradle):**
  `robocopy <projeto> C:\Users\<usuario>\build-cestacerta /MIR /XD build .gradle .git store .claude /XF *.apk *.aab` → em `build-cestacerta`: `npx cap sync android` → `cd android` → `gradlew bundleRelease assembleRelease --no-daemon` (JDK 21).
  Saídas em `android\app\build\outputs\{bundle,apk}\release\` → copiar para `store/`.
- Ícones: `node gen-icons.cjs && node gen-android-icons.cjs`
- Conferir layout sem celular: Edge headless (`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe --headless --screenshot=… --window-size=700,892 --virtual-time-budget=3000`) abrindo uma página com `<iframe>` de 412 px (ou 360 px) que carrega `dist/index.html` + script que semeia `state` e chama `renderView()`. Usar `--user-data-dir` novo por captura, **esperar o PNG aparecer** (o Edge grava depois que o processo sai) e cortar a largura com sharp.
- Teste ponta a ponta sem celular: jsdom (`npm i jsdom` numa pasta temporária) carregando `dist/index.html`; ver `state`/`currentView` com `window.eval` (são `let`, não aparecem em `window`).
- Testar receita por link com páginas reais: carregar `dist/index.html` no jsdom, `fetch` do Node para obter o HTML e chamar `window.extrairReceitaHtml(html)` + `window._itemsDeLinhas(linhas)`.
- Teste ponta a ponta do histórico/comparação/orçamento por fonte: jsdom com o cenário Guanabara × Mundial (comprar, finalizar, dica por item, veredito, fontes). Lembrar: `state.purchases`, `state.stores`, `list.store`, `list.funds`.
- **Valor da linha do item = `itemTotal(item)`** (modos por unidade / valor total / por kg). Nunca calcule `price*qty` direto. Itens: `priceMode` (ausente = unidade).
- Testar parser de receita em Node: extrair o trecho entre `// <recipe-parser>` e `// </recipe-parser>` do `index.html`.
- Testar no celular (adb): conferir `dumpsys window | grep mCurrentFocus` = `com.cestacerta.lista` ANTES de qualquer `input`. Screenshot: `screencap -p /sdcard/s.png` + `adb pull` (não usar `exec-out` no PowerShell).

## Regras de Código & Resposta
1. Altere `index.html` e espelhe em `dist/index.html`; suba o cache do `sw.js`.
2. Seja direto nas respostas. Evite introduções e explicações óbvias.
3. Forneça apenas o código modificado ou o bloco relevante, sem reescrever o arquivo inteiro a menos que solicitado.
4. Mantenha suporte offline e layout responsivo mobile. Safe-area: topo é nativo (MainActivity), CSS só usa `env(safe-area-inset-bottom)`.
5. Scripts Python com acentos: escrever com a ferramenta Write e rodar o arquivo (heredoc quebra codificação). Não usar `Set-Content` do PowerShell em arquivos de código (adiciona BOM).
6. Não publicar nada externo (GitHub, loja) nem mexer em dados reais do celular sem confirmar com o usuário.
7. **Testes por toque/teclado no celular (adb `input`) só com o usuário avisando que o aparelho está livre.** Ele costuma usar o app ao mesmo tempo; já aconteceu de toques e texto caírem na sessão dele. Para validar, prefira jsdom/Edge headless; se precisar do aparelho, peça "deixe o celular parado" e use só leitura (`screencap`) quando possível.
