"""Gera o PDF de apresentação do produto a partir de docs/apresentacao/apresentacao.html.
Uso:  python tools/gerar-apresentacao.py            -> docs/apresentacao/Cesta-Certa-Apresentacao.pdf
      python tools/gerar-apresentacao.py --paginas  -> também salva um PNG por página em %TEMP%/cesta-apresentacao (para conferir o layout)
Requer Microsoft Edge. As imagens vêm de docs/prints/ (regerar com tools/gerar-prints.py + tools/moldura-prints.cjs)."""
import os, subprocess, sys, tempfile, time

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(PROJ, 'docs', 'apresentacao', 'apresentacao.html')
PDF = os.path.join(PROJ, 'docs', 'apresentacao', 'Cesta-Certa-Apresentacao.pdf')
TMP = os.path.join(tempfile.gettempdir(), 'cesta-apresentacao')
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
os.makedirs(TMP, exist_ok=True)
URL = 'file:///' + HTML.replace(chr(92), '/')


def esperar(caminho, minimo=2000, tentativas=80):
    for _ in range(tentativas):                      # o Edge grava o arquivo depois que o processo termina
        if os.path.exists(caminho) and os.path.getsize(caminho) > minimo:
            time.sleep(0.5)
            return True
        time.sleep(0.5)
    return False


def pdf():
    if os.path.exists(PDF):
        os.remove(PDF)
    subprocess.run([EDGE, '--headless', '--disable-gpu', '--no-sandbox', '--user-data-dir=' + os.path.join(TMP, 'prof_pdf'),
                    '--no-pdf-header-footer', '--print-to-pdf=' + PDF, URL], capture_output=True, text=True, timeout=180)
    print('PDF', esperar(PDF, 20000), os.path.getsize(PDF) if os.path.exists(PDF) else 0)


def paginas(n=11):
    base = 'file:///' + os.path.dirname(HTML).replace(chr(92), '/') + '/'
    html = open(HTML, encoding='utf-8').read()
    for i in range(1, n + 1):
        # página isolada (as demais ficam ocultas) para conferir o layout; <base> mantém os caminhos das imagens
        css = f'<base href="{base}"><style>.page{{display:none!important}}#p{i}{{display:block!important;page-break-after:auto!important}}</style>'
        tmp = os.path.join(TMP, f'pag_{i}.html')
        open(tmp, 'w', encoding='utf-8').write(html.replace('</head>', css + '</head>'))
        out = os.path.join(TMP, f'pagina-{i:02d}.png')
        if os.path.exists(out):
            os.remove(out)
        subprocess.run([EDGE, '--headless', '--disable-gpu', '--no-sandbox', '--user-data-dir=' + os.path.join(TMP, f'prof_{i}'),
                        '--hide-scrollbars', '--force-device-scale-factor=1.5', '--window-size=794,1123',
                        '--virtual-time-budget=4000', f'--screenshot={out}', 'file:///' + tmp.replace(chr(92), '/')],
                       capture_output=True, text=True, timeout=120)
        print(f'pagina {i}', esperar(out, 3000))


if __name__ == '__main__':
    pdf()
    if '--paginas' in sys.argv:
        paginas()
