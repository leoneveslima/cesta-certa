"""Gera as capturas brutas (412x892 @3x) de todas as telas com dados de exemplo.
Uso:  python tools/gerar-prints.py   e depois   node tools/moldura-prints.cjs
Requer Microsoft Edge instalado. Lê dist/index.html (espelhe o index.html antes de rodar).
Os dados de exemplo ficam no bloco SEED abaixo (não usa a lista real do usuário)."""
import os, subprocess, time, json, tempfile

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # raiz do projeto
SRC = os.path.join(PROJ, 'dist', 'index.html')
RAW = os.path.join(tempfile.gettempdir(), 'cesta-prints')            # capturas brutas (temporárias)
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
os.makedirs(RAW, exist_ok=True)
html = open(SRC, encoding='utf-8').read()
W, H, SC = 412, 892, 3

SEED = r'''
<script>
(function(){
  let n=0; const it=(name,category,qty,price,inCart,extra)=>Object.assign({id:'d'+(n++),name,category,qty,price,inCart,createdAt:1},extra||{});
  const R1='Macarrão com Atum', R2='Pudim de Leite Condensado';
  const DIA=86400000, hoje=Date.now();
  const comp=(store,dias,items)=>({id:'p'+(n++),store,date:hoje-dias*DIA,listName:'Compra do Mês',total:items.reduce((s,i)=>s+i.price*i.qty,0),items});
  const pi=(name,category,qty,price,vol)=>({name,category,qty,price,vol:vol||0,recipe:''});
  state.purchases=[
    comp('Supermercados Guanabara',26,[pi('Macarrão Penne','Grãos e Cereais',1,5.99),pi('Atum em Lata','Enlatados',2,8.49),pi('Molho de Tomate','Enlatados',1,3.29),
      pi('Carne Moída','Açougue',1,19.9,500),pi('Coca-Cola','Bebidas',12,4.19,269),pi('Leite Condensado MOÇA®','Laticínios',1,7.49),pi('Cebola','Hortifrúti',2,3.2)]),
    comp('Supermercados Mundial',48,[pi('Macarrão Penne','Grãos e Cereais',1,6.29),pi('Atum em Lata','Enlatados',2,8.99),pi('Carne Moída','Açougue',1,21.5,500),pi('Coca-Cola','Bebidas',12,3.99,269)])];
  state.stores=['Supermercados Guanabara','Supermercados Mundial'];
  state.lists=[
   {id:'a',name:'Compra do Mês',budget:750,store:'Supermercados Mundial',
    funds:[{label:'Vale-alimentação',amount:600,foodOnly:true},{label:'Saldo em conta',amount:150,foodOnly:false}],createdAt:1,items:[
     it('Macarrão Penne','Grãos e Cereais',1,6.49,true,{recipe:R1}),
     it('Atum em Lata','Enlatados',2,8.99,true,{recipe:R1}),
     it('Molho de Tomate','Enlatados',1,3.49,false,{recipe:R1}),
     it('Cebola','Hortifrúti',2,0,false,{recipe:R1}),
     it('Alho — 2 dentes','Hortifrúti',1,0,false,{recipe:R1}),
     it('Leite Condensado MOÇA®','Laticínios',1,7.99,true,{recipe:R2}),
     it('Leite Líquido NINHO® — 2 medidas','Laticínios',1,0,false,{recipe:R2}),
     it('Ovos','Laticínios',3,0,false,{recipe:R2}),
     it('Açúcar — 1 xícara (chá)','Grãos e Cereais',1,0,false,{recipe:R2}),
     it('Carne Moída','Açougue',1,21.9,true,{vol:500}),
     it('Coca-Cola','Bebidas',12,3.89,true,{vol:269}),
     it('Maçã','Hortifrúti',8,24,true,{priceMode:'total'}),
     it('Sabão em Pó','Limpeza',1,32.9,true),
     it('Papel Higiênico','Higiene',1,0,false)]},
   {id:'b',name:'Churrasco',budget:0,createdAt:2,items:[]}];
  state.currentListId='a'; state.groupMode=window.__GROUP||'recipe'; state.theme=window.__THEME||'dark'; applyTheme();
  state.collapsed={};
  if(window.__COLLAPSE){ state.collapsed.a={}; window.__COLLAPSE.forEach(k=>state.collapsed.a[k]=1); }
  currentView=window.__VIEW||'list'; renderView();
  if(window.__RECIPE_TEXT){ document.getElementById('recipe-text').value=window.__RECIPE_TEXT; }
  if(window.__CHURRAS){ const c=window.__CHURRAS; document.getElementById('churras-pessoas').value=c[0]; document.getElementById('churras-bebedores').value=c[1]; document.getElementById('churras-criancas').value=c[2]; calcularChurrasco();
     const el=document.getElementById('churras-pessoas'); window.scrollTo(0, el.getBoundingClientRect().top+window.scrollY-190); }
  if(window.__PREVIEW){ state.lists[0].items=[]; document.getElementById('recipe-text').value=window.__PREVIEW; lerReceita(); }
  if(window.__OPEN==='finish'){ abrirFinalizar(); }
  if(window.__OPEN==='budget'){ abrirOrcamento(); }
  if(window.__OPEN==='add'){ openModal('addModal'); }
  if(window.__OPEN==='newlist'){ openModal('newListModal'); }
  if(window.__ONLY==='precos'){
    state.lists[0].funds=[]; state.lists[0].budget=300;
    state.lists[0].items=[ it('Maçã','Hortifrúti',8,24,true,{priceMode:'total'}), it('Banana','Hortifrúti',6,7.9,true,{priceMode:'kg',vol:900}),
      it('Coca-Cola','Bebidas',2,9.5,true,{vol:2000}), it('Arroz','Grãos e Cereais',3,5.99,true) ];
    currentView='cart'; state.groupMode='cat'; renderView();
  }
  if(window.__SCROLL){ window.scrollTo(0, window.__SCROLL); }
  document.querySelectorAll('.modal-sheet').forEach(m=>m.style.transition='none');
})();
</script>
'''


def shot(name, **cfg):
    pre = '<script>' + ''.join(f"window.__{k.upper()}={json.dumps(v, ensure_ascii=False)};" for k, v in cfg.items()) + '</script>'
    f = os.path.join(RAW, f'page_{name}.html')
    open(f, 'w', encoding='utf-8').write(html.replace('</body>', pre + SEED + '</body>'))
    wf = os.path.join(RAW, f'wrap_{name}.html')
    open(wf, 'w', encoding='utf-8').write(
        f'<body style="margin:0;background:#888"><iframe src="page_{name}.html" style="border:0;width:{W}px;height:{H}px;display:block"></iframe></body>')
    out = os.path.join(RAW, f'{name}.png')
    if os.path.exists(out):
        os.remove(out)
    subprocess.run([EDGE, '--headless', '--disable-gpu', '--no-sandbox', '--user-data-dir=' + os.path.join(RAW, 'prof_' + name),
                    '--hide-scrollbars', f'--force-device-scale-factor={SC}', f'--window-size=700,{H}',
                    '--virtual-time-budget=4000', f'--screenshot={out}', 'file:///' + wf.replace(chr(92), '/')],
                   capture_output=True, text=True, timeout=120)
    for _ in range(60):            # o Edge grava o PNG depois que o processo termina
        if os.path.exists(out) and os.path.getsize(out) > 5000:
            break
        time.sleep(0.5)
    print(name, os.path.exists(out))


PUDIM_URL = 'https://www.receitasnestle.com.br/receitas/pudim-de-leite-moca'
ESCONDIDINHO = '''Escondidinho de carne moída com abóbora
Ingredientes
400 gramas de carne moída
1 colher de sopa de azeite
3 dentes de alho
800 gramas de abóbora-cabotiá
2 colheres de sopa de manteiga
1 colher de sopa de requeijão
1/2 colher de chá de sal
1 cebola média picada
Modo de preparo
x'''

shot('01-lista-por-receita', view='list', group='recipe', collapse=['l:r:Pudim de Leite Condensado'])
shot('02-lista-por-categoria', view='list', group='cat', collapse=['l:c:Grãos e Cereais', 'l:c:Enlatados', 'l:c:Hortifrúti'])
shot('03-carrinho', view='cart', group='cat')
shot('04-receita-por-link', view='tools', recipe_text=PUDIM_URL)
shot('05-previa-da-receita', view='tools', preview=ESCONDIDINHO)
shot('06-calculadora-de-churrasco', view='tools', churras=[8, 5, 2])
shot('07-historico-e-comparacao', view='history')
shot('08-configuracoes', view='settings')
shot('09-tema-claro', view='list', group='recipe', theme='light', collapse=['l:r:Pudim de Leite Condensado'])
shot('10-finalizar-compra', view='cart', group='cat', open='finish')
shot('11-orcamento-por-fonte', view='settings', open='budget')
shot('12-adicionar-item', view='list', group='recipe', open='add')
shot('13-nova-lista', view='list', group='recipe', open='newlist')
shot('14-modos-de-preco', view='cart', only='precos')
