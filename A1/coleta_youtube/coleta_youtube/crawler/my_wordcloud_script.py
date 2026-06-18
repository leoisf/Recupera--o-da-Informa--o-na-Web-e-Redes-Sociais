import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

# --- Configurações Iniciais ---
ARQUIVO_CSV = 'files 20260617_185303/comments_info.csv'  # Nome do seu arquivo
COLUNA_TEXTO = 'comment'  # Nome da coluna que contém os comentários


def gerar_nuvem_palavras(arquivo, coluna):
    try:
        # 1. Carregar os dados
        # O encoding='utf-8' é importante para acentos em português
        df = pd.read_csv(arquivo, encoding='utf-8')

        # Verificar se a coluna existe
        if coluna not in df.columns:
            print(f"Erro: A coluna '{coluna}' não foi encontrada no arquivo.")
            print(f"Colunas disponíveis: {list(df.columns)}")
            return

        # 2. Tratamento dos dados
        # Remove valores nulos e converte tudo para string
        comentarios = df[coluna].dropna().astype(str)

        # Junta todos os comentários em uma única string longa
        texto_completo = " ".join(comentario for comentario in comentarios)

        # 3. Configurar Stopwords (Palavras para ignorar)
        # Adicionamos palavras comuns em português que não agregam valor visual
        stopwords = set(STOPWORDS)
        novas_stopwords = ["de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "é", "com", "não", "uma", "os",
                           "no", "se", "na", "por", "mais", "as", "dos", "como", "mas", "foi", "ao", "ele", "das",
                           "tem", "à", "seu", "sua", "ou", "ser", "quando", "muito", "nos", "já", "está", "eu",
                           "também", "só", "pelo", "pela", "até", "isso", "ela", "entre", "era", "depois", "sem",
                           "mesmo", "aos", "ter", "seus", "quem", "nas", "me", "esse", "eles", "estão", "você", "tinha",
                           "foram", "essa", "num", "nem", "suas", "meu", "às", "minha", "têm", "numa", "pelos", "elas",
                           "havia", "seja", "qual", "será", "nós", "tenho", "lhe", "deles", "essas", "esses", "pelas",
                           "este", "fosse", "dele", "tu", "te", "vocês", "vos", "lhes", "meus", "minhas", "teu", "tua",
                           "teus", "tuas", "nosso", "nossa", "nossos", "nossas", "dela", "delas", "uns", "umas",
                           "esteja", "estejamos", "estejam", "estivesse", "estivéssemos", "estivessem", "estiver",
                           "estivermos", "estiverem", "hei", "há", "havemos", "hão", "houve", "houvemos", "houveram",
                           "houvera", "houvéramos", "haja", "hajamos", "hajam", "houvesse", "houvéssemos", "houvessem",
                           "houver", "houvermos", "houverem", "houverei", "houverá", "houveremos", "houverão",
                           "houveria", "houveríamos", "houveriam", "sou", "somos", "são", "era", "éramos", "eram",
                           "fui", "foi", "fomos", "foram", "fora", "fôramos", "seja", "sejamos", "sejam", "fosse",
                           "fôssemos", "fossem", "for", "formos", "forem", "serei", "será", "seremos", "serão", "seria",
                           "seríamos", "seriam", "tenho", "tem", "temos", "tém", "tinha", "tínhamos", "tinham", "tive",
                           "teve", "tivemos", "tiveram", "tivera", "tivéramos", "tenha", "tenhamos", "tenham",
                           "tivesse", "tivéssemos", "tivessem", "tiver", "tivermos", "tiverem", "terei", "terá",
                           "teremos", "terão", "teria", "teríamos", "teriam", 'kkk', "pra", 'vc', 'aí', 'know','q','sei','então',
                           'assim', 'kkkk', 'kkkkk', 'tbm', 'estou', 'ate', 'ainda', "USE", 'tá', 'blaze', 'blazer', 'Silver', 'sonic', 'high', 'S', 'shadow', 'Bro', 'edible', 'one','going', 'nao', 'make','gonna',
                           'Deu', 'think', 'weed', 'edibles','vou','sim', 'say','see', 'Chevrolet','vídeo', 'faz', 'even','much','top',
                           'hedgehog', 'way', 'go', 'super', 'love', 'video', 'aqui', 'back', 'well', 'power', 'desse', 'vai','thing',
                           ]
        stopwords.update(novas_stopwords)

        # 4. Gerar a Nuvem de Palavras
        # background_color: cor de fundo
        # colormap: esquema de cores (ex: 'viridis', 'plasma', 'inferno', 'magma')
        wordcloud = WordCloud(width=800, height=400,
                              background_color='white',
                              stopwords=stopwords,
                              min_font_size=10).generate(texto_completo)

        # 5. Plotar a Imagem
        plt.figure(figsize=(10, 5), facecolor=None)
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")  # Remove os eixos x e y
        plt.tight_layout(pad=0)

        print("Gerando nuvem de palavras...")
        # Salvar a imagem em vez de exibir (para ambientes sem GUI)
        output_path = 'wordcloud.png'
        plt.savefig(output_path, dpi=100, bbox_inches='tight')
        print(f"✓ Nuvem de palavras salva em: {output_path}")
        plt.close()

    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


# Executar a função
if __name__ == "__main__":
    gerar_nuvem_palavras(ARQUIVO_CSV, COLUNA_TEXTO)