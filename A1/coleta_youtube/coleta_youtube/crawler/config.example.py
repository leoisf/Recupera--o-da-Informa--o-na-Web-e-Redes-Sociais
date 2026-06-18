config = {
  # Configuração da região da coleta -> Formato: ISO 3166-1 alpha-2
  "region_code": "BR",         

  # Configuração da linguagem da coleta -> Formato: ISO 639-1   
  "relevance_language": "pt",     

  # A coleta ocorre da data final para a data inicial -> [ano, mês, dia]
  "start_date": [2026, 1, 1],
  "end_date": [2026, 6, 16],

  # API que receberá uma requisição PATCH com payload de um JSON contendo informações acerca da coleta
  # Mantenha uma string vazia "" Caso não tenha configurado
  "api_endpoint": "",
  # Intervalo, em segundos, entre cada envio de dados para a API
  "api_cooldown": 60,                                                   

  # Intervalo, em segundos, entre cada tentativa de requisição para a API apos falha
  "try_again_timeout": 60,                                              

  # Palavras que serão utilizadas para filtrar os títulos dos vídeos
  "key_words": [
    "data science", "machine learning", "artificial intelligence"
  ], 

  # KEYs da API v3 do YouTube
  "youtube_keys": [
    'key1',
    'key2',
    'key3'    
  ],

  # Queries que serão utilizadas na pesquisa
  "queries": [
    "LLM", "generative AI", "Kiro", "MCP", "Hook", "RAG"
  ]
}