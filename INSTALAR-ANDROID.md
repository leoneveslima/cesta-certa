# 📱 Instalar o Cesta Certa no Android

O Cesta Certa agora é uma **PWA** (Progressive Web App): instala como um app nativo (ícone na
tela inicial, tela cheia, funciona **offline**), sem precisar de loja de apps.

Uma PWA precisa ser aberta por **HTTPS** ou **localhost** para instalar. Escolha um caminho:

---

## ✅ Opção A — Hospedar grátis (recomendado, gera link permanente)

A forma mais simples de ter um link HTTPS que funciona em qualquer celular.

### Com GitHub Pages
1. Crie um repositório no GitHub e envie estes arquivos:
   - `index.html`, `manifest.json`, `sw.js`
   - `icon-192.png`, `icon-512.png`, `apple-touch-icon.png`
2. No repositório: **Settings → Pages → Branch: main → /(root) → Save**.
3. Em ~1 min o GitHub te dá um link `https://seu-usuario.github.io/seu-repo/`.
4. Abra esse link no **Chrome do celular** e siga a seção **"Instalar"** abaixo.

### Com Netlify Drop (sem conta, mais rápido)
1. Acesse **https://app.netlify.com/drop**
2. Arraste a **pasta inteira** `app_compras` para a página.
3. Ele gera um link `https://....netlify.app` na hora. Abra no celular e instale.

---

## ✅ Opção B — Rede local (mesmo Wi-Fi do PC)

Funciona, mas como é HTTP (não HTTPS), a instalação/offline pode ficar limitada em
alguns Androids. Bom para teste rápido.

1. No PC, dentro da pasta do projeto:
   ```
   npx http-server -p 8080
   ```
2. Descubra o IP do PC (no PowerShell): `ipconfig` → procure "Endereço IPv4" (ex: `192.168.0.10`).
3. No celular (mesmo Wi-Fi), abra no Chrome: `http://192.168.0.10:8080`

---

## 📲 Instalar (depois de abrir o link no Chrome do Android)

1. Toque no menu **⋮** (canto superior direito).
2. Toque em **"Instalar app"** ou **"Adicionar à tela inicial"**.
3. Confirme. O ícone do Cesta Certa aparece na tela inicial como um app normal.
4. Ao abrir pelo ícone, ele roda em tela cheia, sem barra do navegador.

> Em geral o Chrome também mostra sozinho um banner **"Instalar Cesta Certa"** ao abrir o link.

---

## ❓ Quero um arquivo `.apk` de verdade

A PWA cobre 99% dos casos. Se você precisa especificamente de um `.apk` (para distribuir
fora do navegador ou publicar na Play Store), o caminho mais simples a partir desta PWA é:

1. Hospede o app (Opção A) para ter um link HTTPS.
2. Acesse **https://www.pwabuilder.com**, cole o link e clique em **Build → Android**.
3. Baixe o pacote `.apk`/`.aab` gerado (TWA — Trusted Web Activity).

Isso evita instalar o Android SDK (~vários GB) localmente. Se preferir gerar o APK aqui
mesmo na máquina com Capacitor, me avise — exige baixar o SDK e atualizar para o JDK 17.

---

## Arquivos da PWA
| Arquivo | Função |
|---|---|
| `index.html` | O app completo |
| `manifest.json` | Metadados de instalação (nome, ícones, cores) |
| `sw.js` | Service worker — cache offline |
| `icon-192.png` / `icon-512.png` | Ícones do app |
| `apple-touch-icon.png` | Ícone para iOS |
| `icon-source.svg` | Fonte vetorial dos ícones (para regenerar) |
