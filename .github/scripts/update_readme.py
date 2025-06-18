# .github/scripts/update_readme.py
import sys
import re

def update_readme(repo_name, repo_url, readme_path='README.md'):
    """
    Adiciona um novo link de repositório à seção 'My Public Repositories'
    no README.md, mantendo a lista em ordem alfabética e evitando duplicatas.
    """
    new_link = f"- [{repo_name}]({repo_url})"
    section_header = "## My Public Repositories"

    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Erro: O arquivo {readme_path} não foi encontrado.")
        sys.exit(1)

    # Encontra o início e o fim da seção de repositórios
    start_index = -1
    end_index = -1
    for i, line in enumerate(lines):
        if line.strip() == section_header:
            start_index = i
        elif start_index != -1 and line.strip().startswith("##"):
            end_index = i
            break

    if start_index == -1:
        print(f"Erro: A seção '{section_header}' não foi encontrada no README.md.")
        sys.exit(1)

    if end_index == -1:
        end_index = len(lines)

    # Extrai a lista atual de repositórios
    repo_list = []
    for i in range(start_index + 1, end_index):
        line = lines[i].strip()
        if line.startswith("- ["):
            repo_list.append(line)

    # Verifica se o link já existe
    if any(repo_url in item for item in repo_list):
        print(f"O link para o repositório '{repo_name}' já existe. Nenhuma alteração necessária.")
        sys.exit(0)

    # Adiciona o novo link e ordena a lista
    repo_list.append(new_link)
    repo_list.sort(key=lambda x: x.lower()) # Ordena alfabeticamente

    # Reconstrói as linhas do README
    new_lines = lines[:start_index + 1]
    new_lines.extend([f"{item}\n" for item in repo_list])

    # Garante que haja uma linha em branco após a lista, se havia antes
    if end_index < len(lines) and lines[end_index].strip() == "":
         new_lines.append("\n")

    new_lines.extend(lines[end_index:])

    # Salva o arquivo README atualizado
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"README.md atualizado com sucesso com o repositório {repo_name}.")

if __name__ == '__main__':
    repo_name = sys.argv[1]
    repo_url = sys.argv[2]
    update_readme(repo_name, repo_url)
