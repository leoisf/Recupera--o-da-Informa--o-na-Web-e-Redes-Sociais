"""
Gera Leonardo_Flores_A5.pdf a partir do resolucao_exercicios.ipynb.
"""
import json, base64, subprocess, os, textwrap, re, html as _html

NB_PATH   = 'resolucao_exercicios.ipynb'
HTML_PATH = '_tmp_a5.html'
PDF_PATH  = 'Leonardo_Flores_A5.pdf'
CHROME    = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

with open(NB_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Células que contêm APENAS definições de funções auxiliares — omitir do PDF
# (o leitor vê só a chamada e o resultado, como num relatório)
SKIP_CODE_CELLS = {4, 9}   # buscar_focus, buscar_ptax

# ── markdown → HTML simples ───────────────────────────────────────────────────
def md2html(text):
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)

    lines = text.split('\n')
    out, in_table, in_list = [], False, False

    for line in lines:
        s = line.strip()

        m = re.match(r'^(#{1,4})\s+(.*)', s)
        if m:
            if in_list:  out.append('</ul>'); in_list = False
            if in_table: out.append('</table>'); in_table = False
            lvl = len(m.group(1))
            out.append(f'<h{lvl}>{m.group(2)}</h{lvl}>')
            continue

        if s in ('---', '***', '___'):
            if in_list:  out.append('</ul>'); in_list = False
            if in_table: out.append('</table>'); in_table = False
            out.append('<hr>')
            continue

        if s.startswith('|'):
            if in_list: out.append('</ul>'); in_list = False
            cells = [c.strip() for c in s.strip('|').split('|')]
            if all(re.match(r'^[-:]+$', c.replace(' ', '')) for c in cells):
                continue
            if not in_table:
                out.append('<table>')
                in_table = True
                out.append('<tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr>')
            else:
                out.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
            continue
        else:
            if in_table: out.append('</table>'); in_table = False

        if s.startswith(('● ', '* ', '- ')):
            if not in_list: out.append('<ul>'); in_list = True
            out.append(f'<li>{s[2:].strip()}</li>')
            continue
        else:
            if in_list: out.append('</ul>'); in_list = False

        if not s:
            out.append('<br>')
            continue

        out.append(f'<p>{s}</p>')

    if in_list:  out.append('</ul>')
    if in_table: out.append('</table>')
    return '\n'.join(out)


# ── montar corpo HTML ─────────────────────────────────────────────────────────
parts = []

for idx, cell in enumerate(nb['cells']):
    ctype = cell['cell_type']
    # source é sempre lista de strings no nbformat 4
    src = ''.join(cell.get('source', []))

    if ctype == 'markdown':
        # Ocultar células puramente de infraestrutura ("## Imports")
        if src.strip() in ('## Imports',):
            continue
        parts.append(f'<div class="md">{md2html(src)}</div>')

    elif ctype == 'code':
        if idx in SKIP_CODE_CELLS:
            # Pula exibição do código da função, mas ainda renderiza os outputs
            pass
        else:
            # Não mostrar células de import ou setup
            skip_kw = ['import requests', 'import urllib3',
                       'plt.rcParams', 'print(\'ok\')', 'print("ok")']
            if not any(k in src for k in skip_kw):
                escaped = _html.escape(src)
                parts.append(f'<pre><code>{escaped}</code></pre>')

        # Outputs (sempre renderizar independente de mostrar o código)
        for out in cell.get('outputs', []):
            otype = out.get('output_type', '')

            if otype == 'stream':
                text = ''.join(out.get('text', []))
                parts.append(f'<pre class="output">{_html.escape(text)}</pre>')

            elif otype in ('display_data', 'execute_result'):
                data = out.get('data', {})

                if 'image/png' in data:
                    b64 = data['image/png'].replace('\n', '')
                    parts.append(
                        '<div class="img-wrap">'
                        f'<img src="data:image/png;base64,{b64}" alt="grafico">'
                        '</div>'
                    )
                elif 'text/html' in data:
                    # DataFrame HTML — limpar estilos inline que atrapalham
                    raw = data['text/html']
                    df_html = ''.join(raw) if isinstance(raw, list) else raw
                    # remover bloco <style> embutido do pandas
                    df_html = re.sub(r'<style[^>]*>.*?</style>', '',
                                     df_html, flags=re.DOTALL)
                    parts.append(f'<div class="df">{df_html}</div>')
                # text/plain ignorado — evita o lixo \n', ' do repr de lista

            elif otype == 'error':
                tb = '\n'.join(out.get('traceback', []))
                tb = re.sub(r'\x1b\[[0-9;]*m', '', tb)
                parts.append(f'<pre class="error">{_html.escape(tb)}</pre>')

body_html = '\n'.join(parts)

# ── CSS ───────────────────────────────────────────────────────────────────────
css = textwrap.dedent("""
    @page { size: A4; margin: 18mm 16mm 18mm 16mm; }
    * { box-sizing: border-box; }
    body {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 10.5pt;
        color: #1a1a1a;
        line-height: 1.55;
    }
    h1 { font-size: 16pt; margin: 0 0 6pt; }
    h2 { font-size: 13pt; margin: 18pt 0 4pt;
         border-bottom: 1px solid #ccc; padding-bottom: 3pt; }
    h3 { font-size: 11pt; margin: 12pt 0 3pt; color: #333; }
    h4 { font-size: 10.5pt; margin: 8pt 0 2pt; }
    p  { margin: 3pt 0; }
    hr { border: none; border-top: 1px solid #ddd; margin: 10pt 0; }
    ul { margin: 4pt 0 4pt 18pt; padding: 0; }
    li { margin-bottom: 3pt; }
    code {
        font-family: "Consolas", "Courier New", monospace;
        font-size: 9pt;
        background: #f4f4f4;
        padding: 1px 4px;
        border-radius: 3px;
    }
    pre {
        font-family: "Consolas", "Courier New", monospace;
        font-size: 8.5pt;
        background: #f6f6f6;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 8pt 10pt;
        margin: 6pt 0;
        white-space: pre-wrap;
        word-break: break-word;
        page-break-inside: avoid;
    }
    pre.output {
        background: #fafffe;
        border-color: #c8e6c9;
        color: #1b5e20;
    }
    pre.error {
        background: #fff3f3;
        border-color: #ffcdd2;
        color: #b71c1c;
    }
    .img-wrap {
        text-align: center;
        margin: 10pt 0;
        page-break-inside: avoid;
    }
    .img-wrap img {
        max-width: 100%;
        height: auto;
        display: block;
        margin: 0 auto;
    }
    .df { margin: 6pt 0; page-break-inside: avoid; }
    .df table {
        border-collapse: collapse;
        font-size: 8.5pt;
        width: auto;
    }
    .df th, .df td {
        border: 1px solid #ddd;
        padding: 3pt 7pt;
        text-align: right;
    }
    .df th {
        background: #f0f0f0;
        font-weight: 600;
        text-align: center;
    }
    table {
        border-collapse: collapse;
        font-size: 9.5pt;
        margin: 6pt 0;
        width: 100%;
    }
    th, td { border: 1px solid #ccc; padding: 4pt 8pt; }
    th { background: #f0f4f8; font-weight: 600; }
    .md { margin-bottom: 2pt; }
    strong { color: #000; }
""")

html_full = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
{css}
</style>
</head>
<body>
{body_html}
</body>
</html>"""

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html_full)

print(f'HTML: {os.path.getsize(HTML_PATH):,} bytes')

# ── Chrome headless → PDF ─────────────────────────────────────────────────────
pdf_abs  = os.path.abspath(PDF_PATH)
html_abs = os.path.abspath(HTML_PATH)

result = subprocess.run([
    CHROME,
    '--headless',
    '--disable-gpu',
    '--no-sandbox',
    '--run-all-compositor-stages-before-draw',
    '--virtual-time-budget=5000',
    f'--print-to-pdf={pdf_abs}',
    '--print-to-pdf-no-header',
    f'file:///{html_abs}'
], capture_output=True, text=True, timeout=90)

os.remove(HTML_PATH)

if os.path.exists(pdf_abs):
    print(f'PDF: {pdf_abs}  ({os.path.getsize(pdf_abs):,} bytes)')
else:
    print('ERRO — PDF não gerado')
    print(result.stderr[-600:])
