# 📦 Cesta Certa — APK Android (offline)

**Arquivo:** `store/CestaCerta-1.4.0.apk` (≈3,0 MB) — na pasta `app_compras`. Pacote `com.cestacerta.lista`.

Este APK **embute o app inteiro**: funciona 100% offline, sem precisar de link ou internet.
Pode ser compartilhado por WhatsApp, e-mail, Google Drive, cabo USB, etc.

---

## 📲 Como instalar (você e seus familiares)

1. Envie o arquivo `CestaCerta-1.2.0.apk` para o celular (WhatsApp, e-mail, Drive…).
2. No celular, toque no arquivo para abrir.
3. O Android vai pedir permissão: **"Permitir instalar apps desta fonte"**
   → ative para o app usado (Arquivos / WhatsApp / Chrome) e volte.
4. Toque em **Instalar**.
5. Se aparecer o **Play Protect** ("app não reconhecido"), toque em
   **"Instalar mesmo assim"** — é normal para apps fora da Play Store.
6. Pronto! O ícone do **Cesta Certa** aparece na gaveta de apps.

> Funciona em Android 6.0 ou superior.

---

## ⚠️ Observações importantes

- **APK de release assinado:** é o mesmo build enviado à Play Store (versão 1.4.0), assinado com a
  chave de upload. Serve para uso pessoal/familiar fora da loja.
- **Dados locais:** cada celular guarda a sua própria lista (não sincroniza entre
  aparelhos). Use **Config → Backup** para copiar seus dados e restaurar em outro aparelho.
- **Atualizar o app:** instale a nova versão por cima — os dados são preservados
  (mesmo `applicationId` e mesma assinatura).
- **App antigo "My List"** (`com.mylist.compras`) é outro pacote: pode ficar instalado ao lado
  e tem dados próprios. Pode desinstalar quando quiser.

---

## 🔧 Para regenerar o APK/AAB (após editar o app)

O OneDrive corrompe o build do Gradle, então compile numa **cópia fora do OneDrive**
(passo a passo completo em `docs/DOCUMENTACAO.md`, seção 5, e no `README.md`):

```powershell
robocopy "<pasta do projeto>" C:\Users\lrnli\build-cestacerta /MIR /XD build .gradle .git store .claude /XF *.apk *.aab
cd C:\Users\lrnli\build-cestacerta ; npx cap sync android
cd android
$env:JAVA_HOME="C:\Program Files\Eclipse Adoptium\jdk-21.0.11.10-hotspot"
.\gradlew.bat bundleRelease assembleRelease --no-daemon
# AAB (Play Store): android\app\build\outputs\bundle\release\app-release.aab
# APK (instalar):   android\app\build\outputs\apk\release\app-release.apk
```

Antes de gerar: subir `versionCode`/`versionName` em `android/app/build.gradle` e o cache do `sw.js`.
A chave de assinatura fica em `C:\Users\lrnli\keystore-cestacerta\` (fora do projeto).
