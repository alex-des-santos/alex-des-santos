# .github/scripts/update_readme.py
import os
import requests
import re

def get_public_repos(github_user):
    """Busca todos os repositórios públicos de um usuário via API do GitHub."""
    repos = []
    page = 1
    while True:
        # Usamos a API pública, não precisa de token para esta parte
        url = f"https://api.github.com/users/{github_user}/repos?type=owner&sort=updated&per_page=100&page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Erro ao buscar repositórios: {response.status_code} - {response.text}")
            break
        
        data = response.json()
        if not data:
            break
            
        for repo in data:
            # Filtramos para pegar apenas repositórios que não são forks
            if not repo['fork']:
                repos.append({'name': repo['name'], 'url': repo['html_url']})
        page += 1
        
    return repos

def update_readme(github_user, readme_path='README.md'):
    """Atualiza o README com a lista de repositórios públicos."""
    section_header = "## My Public Repositories"
    
    public_repos = get_public_repos(github_user)
    repo_links = sorted([f"- [{repo['name']}]({repo['url']})" for repo in public_repos], key=str.lower)
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Erro: O arquivo {readme_path} não foi encontrado.")
        return

    start_index = -1
    end_index = -1
    for i, line in enumerate(lines):
        if line.strip() == section_header:
            start_index = i
        elif start_index != -1 and line.strip().startswith("##"):
            end_index = i
            break
            
    if start_index == -1:
        print(f"A seção '{section_header}' não foi encontrada. Adicionando ao final do arquivo.")
        lines.append(f"\n{section_header}\n")
        lines.extend([f"{link}\n" for link in repo_links])
    else:
        if end_index == -1:
            end_index = len(lines)
            
        # Constrói o novo conteúdo do README
        new_lines = lines[:start_index + 1]
        new_lines.extend([f"{link}\n" for link in repo_links])
        # Adiciona uma linha em branco para separação, se necessário
        if end_index < len(lines) and lines[end_index].strip() != "":
             new_lines.append("\n")
        new_lines.extend(lines[end_index:])
        lines = new_lines

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
        
    print("README.md atualizado com sucesso!")

if __name__ == '__main__':
    github_user = os.getenv('GITHUB_USER', 'alex-des-santos')
    update_readme(github_user)
