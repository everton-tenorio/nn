import requests
import sys
from datetime import datetime
import json

# Configuração
NOTION_TOKEN = ""
DATABASE_ID = ""

def verificar_colunas():
    """Mostra as colunas disponíveis no database"""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        props = response.json()['properties']
        print("\n=== Colunas disponíveis no seu database ===")
        for nome, info in props.items():
            print(f"  • '{nome}' (tipo: {info['type']})")
        print("\nUse esses nomes exatos no script!\n")
    else:
        print(f"Erro ao buscar database: {response.status_code}")
        print(response.json())

def adicionar_nota(titulo, conteudo):
    """Adiciona uma nota no Notion"""
    url = "https://api.notion.com/v1/pages"
    
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Estrutura da página
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Nome": {  # Coluna de título do database
                "title": [
                    {
                        "text": {
                            "content": titulo
                        }
                    }
                ]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": conteudo
                            }
                        }
                    ]
                }
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("✓ Nota adicionada com sucesso!")
    else:
        print(f"✗ Erro: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    # Se usar --check, mostra as colunas
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        verificar_colunas()
        sys.exit(0)
    
    if len(sys.argv) < 3:
        print("Uso: python notion_note.py 'Título' 'Conteúdo'")
        print("Ou:   python notion_note.py 'Título' -f arquivo.txt")
        print("Ou:   python notion_note.py --check  (para ver colunas)")
        sys.exit(1)
    
    titulo = sys.argv[1]
    
    # Se usar -f, lê de arquivo
    if sys.argv[2] == "-f" and len(sys.argv) >= 4:
        try:
            with open(sys.argv[3], 'r', encoding='utf-8') as f:
                conteudo = f.read()
        except FileNotFoundError:
            print(f"✗ Arquivo '{sys.argv[3]}' não encontrado")
            sys.exit(1)
    else:
        conteudo = sys.argv[2]
    
    adicionar_nota(titulo, conteudo)
