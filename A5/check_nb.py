import json
nb = json.load(open('resolucao_exercicios.ipynb', encoding='utf-8'))
code_cells = [c for c in nb['cells'] if c['cell_type'] == 'code']
for i, c in enumerate(code_cells):
    outs = c.get('outputs', [])
    for o in outs[:2]:
        otype = o.get('output_type', '')
        if otype == 'stream':
            txt = ''.join(o.get('text', []))[:200]
            print(f'[{i+1}] STDOUT: {txt}')
        elif otype == 'error':
            msg = str(o.get('evalue', ''))[:100]
            print(f'[{i+1}] ERRO: {o.get("ename")}: {msg}')
