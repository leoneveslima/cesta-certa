// Corta as capturas brutas, aplica moldura de celular e gera docs/prints/*.png + imagem-resumo.
// Uso: node tools/moldura-prints.cjs   (depois de python tools/gerar-prints.py)
const sharp = require('sharp'), fs = require('fs'), os = require('os'), path = require('path');
const RAW = path.join(os.tmpdir(), 'cesta-prints');
const OUT = path.join(__dirname, '..', 'docs', 'prints');
const W = 1236, H = 2676, B = 36;                       // tela e espessura da moldura
fs.mkdirSync(path.join(OUT, 'sem-moldura'), { recursive: true });
const nomes = fs.readdirSync(RAW).filter(f => /^\d\d-.*\.png$/.test(f)).sort();

async function moldura(file) {
  const tela = await sharp(path.join(RAW, file)).extract({ left: 0, top: 0, width: W, height: H }).png().toBuffer();
  await fs.promises.writeFile(path.join(OUT, 'sem-moldura', file), tela);
  const mask = Buffer.from(`<svg width="${W}" height="${H}"><rect width="${W}" height="${H}" rx="86" fill="#fff"/></svg>`);
  const arred = await sharp(tela).composite([{ input: mask, blend: 'dest-in' }]).png().toBuffer();
  const FW = W + 2 * B, FH = H + 2 * B;
  const corpo = Buffer.from(`<svg width="${FW}" height="${FH}"><rect x="2" y="2" width="${FW - 4}" height="${FH - 4}" rx="122" fill="#0b0f14" stroke="#2c3442" stroke-width="4"/></svg>`);
  const out = await sharp(corpo).composite([{ input: arred, left: B, top: B }]).png().toBuffer();
  await fs.promises.writeFile(path.join(OUT, file), out);
  return out;
}
(async () => {
  const feitos = {};
  for (const f of nomes) feitos[f] = await moldura(f);
  // imagem-resumo: 4 telas lado a lado
  const escolha = [['01-lista-por-receita.png', 'Lista por receita'], ['07-historico-e-comparacao.png', 'Comparar mercados'],
                   ['05-previa-da-receita.png', 'Prévia dos ingredientes'], ['11-orcamento-por-fonte.png', 'Orçamento por fonte']];
  const ph = 1500, scale = ph / (H + 2 * B), pw = Math.round((W + 2 * B) * scale), gap = 70, topo = 150, base = 90;
  const CW = escolha.length * pw + (escolha.length + 1) * gap, CH = topo + ph + base;
  const fundo = Buffer.from(`<svg width="${CW}" height="${CH}"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F8FAFC"/><stop offset="1" stop-color="#E2E8F0"/></linearGradient></defs>
    <rect width="${CW}" height="${CH}" fill="url(#g)"/>
    <text x="${CW / 2}" y="92" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="56" font-weight="800" fill="#1E293B">Cesta Certa: Lista de Compras</text>
    ${escolha.map(([, t], i) => `<text x="${gap + i * (pw + gap) + pw / 2}" y="${topo + ph + 62}" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="34" font-weight="600" fill="#475569">${t}</text>`).join('')}</svg>`);
  const comps = [];
  for (let i = 0; i < escolha.length; i++) {
    const img = await sharp(feitos[escolha[i][0]]).resize({ height: ph }).png().toBuffer();
    comps.push({ input: img, left: gap + i * (pw + gap), top: topo });
  }
  await sharp(fundo).composite(comps).png().toFile(path.join(OUT, '00-visao-geral.png'));
  console.log('ok:', ['00-visao-geral.png', ...nomes].join(', '));
})();
