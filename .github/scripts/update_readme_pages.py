#!/usr/bin/env python3
"""
Script para atualizar o README.md com links dos GitHub Pages
configurados no arquivo pages-config.yml
"""

import yaml
import requests
import re
import os
from typing import List, Dict, Any

def load_pages_config() -> List[Dict[str, str]]:
    """Carrega a configuração dos repositórios com GitHub Pages"""
    try:
        with open('pages-config.yml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            return config.get('pages_repos', [])
    except FileNotFoundError:
        print("❌ Arquivo pages-config.yml não encontrado")
        return []
    except yaml.YAMLError as e:
        print(f"❌ Erro ao ler pages-config.yml: {e}")
        return []

def verify_pages_status(repos: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Verifica se os sites estão online"""
    active_repos = []
    
    for repo in repos:
        url = repo['url']
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                active_repos.append(repo)
                print(f"✅ {repo['repo']}: Site ativo")
            else:
                print(f"⚠️  {repo['repo']}: Site retornou {response.status_code}")
        except requests.RequestException as e:
            print(f"❌ {repo['repo']}: Erro ao verificar site - {e}")
    
    return active_repos

def generate_pages_section(repos: List[Dict[str, str]]) -> str:
    """Gera a seção dos GitHub Pages para o README"""
    if not repos:
        return ""
    
    section = "## 🌐 GitHub Pages\n"
    
    for repo in repos:
        title = repo.get('title', repo['repo'])
        description = repo.get('description', '')
        url = repo['url']
        
        if description:
            section += f"- **[{title}]({url})** - {description}\n"
        else:
            section += f"- **[{title}]({url})**\n"
    
    section += "\n"
    return section

def update_readme(pages_section: str) -> bool:
    """Atualiza o README.md com a nova seção de GitHub Pages"""
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ README.md não encontrado")
        return False
    
    # Padrão para encontrar a seção existente
    pattern = r'## 🌐 GitHub Pages\n.*?(?=\n## |\n# |\Z)'
    
    if re.search(pattern, content, re.DOTALL):
        # Substitui seção existente
        new_content = re.sub(pattern, pages_section.rstrip(), content, flags=re.DOTALL)
    else:
        # Adiciona nova seção antes da seção "My Public Repositories"
        repo_pattern = r'(## My Public Repositories)'
        if re.search(repo_pattern, content):
            new_content = re.sub(repo_pattern, f'{pages_section}\\1', content)
        else:
            # Adiciona no final se não encontrar seção de repositórios
            new_content = content + '\n' + pages_section
    
    # Só escreve se houve mudança
    if new_content != content:
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ README.md atualizado com sucesso")
        return True
    else:
        print("ℹ️  Nenhuma alteração necessária no README.md")
        return False

def main():
    """Função principal"""
    print("🚀 Iniciando atualização do README com GitHub Pages...")
    
    # Carrega configuração
    repos = load_pages_config()
    if not repos:
        print("ℹ️  Nenhum repositório configurado")
        return
    
    print(f"📋 Encontrados {len(repos)} repositório(s) configurado(s)")
    
    # Verifica status dos sites
    active_repos = verify_pages_status(repos)
    
    if not active_repos:
        print("⚠️  Nenhum site ativo encontrado")
        return
    
    # Gera seção do README
    pages_section = generate_pages_section(active_repos)
    
    # Atualiza README
    update_readme(pages_section)
    
    print("🎉 Processo concluído!")

if __name__ == "__main__":
    main()
