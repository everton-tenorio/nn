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

def listar_paginas():
    """Lista as últimas páginas do database com seus IDs"""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    data = {
        "page_size": 20,
        "sorts": [{"timestamp": "created_time", "direction": "descending"}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        results = response.json()['results']
        print("\n=== Últimas páginas ===")
        for page in results:
            page_id = page['id']
            # Pega o título da página
            titulo_prop = page['properties'].get('Nome', {})
            if titulo_prop.get('title'):
                titulo = titulo_prop['title'][0]['text']['content']
            else:
                titulo = "(sem título)"
            print(f"  • {titulo}")
            print(f"    ID: {page_id}\n")
    else:
        print(f"Erro ao listar páginas: {response.status_code}")
        print(response.json())

def adicionar_conteudo_pagina(page_id, conteudo):
    """Adiciona conteúdo (bloco) em uma página existente"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Divide conteúdo em parágrafos se tiver quebras de linha
    paragrafos = conteudo.split('\n')
    blocos = []
    
    for para in paragrafos:
        if para.strip():  # Ignora linhas vazias
            blocos.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": para}
                    }]
                }
            })
    
    data = {"children": blocos}
    
    response = requests.patch(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("✓ Conteúdo adicionado à página existente!")
    else:
        print(f"✗ Erro: {response.status_code}")
        print(response.json())

def adicionar_nota(titulo, conteudo):
    """Cria uma nova página no database"""
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
            "Nome": {
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
        page_id = response.json()['id']
        print(f"  Page ID: {page_id}")
    else:
        print(f"✗ Erro: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    # Comandos especiais
    if len(sys.argv) > 1:
        if sys.argv[1] == "--check":
            verificar_colunas()
            sys.exit(0)
        elif sys.argv[1] == "--list" or sys.argv[1] == "-l":
            listar_paginas()
            sys.exit(0)
    
    # Adicionar conteúdo em página existente
    if len(sys.argv) >= 4 and sys.argv[1] == "-p":
        page_id = sys.argv[2]
        
        # Se usar -f, lê de arquivo
        if sys.argv[3] == "-f" and len(sys.argv) >= 5:
            try:
                with open(sys.argv[4], 'r', encoding='utf-8') as f:
                    conteudo = f.read()
            except FileNotFoundError:
                print(f"✗ Arquivo '{sys.argv[4]}' não encontrado")
                sys.exit(1)
        else:
            conteudo = sys.argv[3]
        
        adicionar_conteudo_pagina(page_id, conteudo)
        sys.exit(0)
    
    # Criar nova página
    if len(sys.argv) < 3:
        print("nn - terminal notes to notion")
        print("\nUso:")
        print("  nn 'Título' 'Conteúdo'           # cria nova página")
        print("  nn 'Título' -f arquivo.txt       # cria nova página do arquivo")
        print("  nn -p PAGE_ID 'Conteúdo'         # adiciona em página existente")
        print("  nn -p PAGE_ID -f arquivo.txt     # adiciona arquivo em página")
        print("  nn --list ou -l                  # lista páginas e IDs")
        print("  nn --check                       # mostra colunas do database")
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
