# GitHub Pages Auto-Update

Sistema automatizado para manter os links dos GitHub Pages atualizados no README.md do perfil.

## 📁 Estrutura

```text
.github/
├── workflows/
│   └── update-readme.yml      # GitHub Action
└── scripts/
    └── update_readme_pages.py # Script Python
pages-config.yml               # Configuração dos repos
```

## 🚀 Como usar

### 1. Configurar repositórios

Edite `pages-config.yml` para adicionar novos sites:

```yaml
pages_repos:
  - repo: nome-do-repositorio
    url: https://alex-des-santos.github.io/nome-do-repositorio/
    title: "Título do Projeto"
    description: "Descrição breve do projeto"
```

### 2. Executar automaticamente

A Action roda automaticamente quando:

- ✅ Você faz push no arquivo `pages-config.yml`
- ✅ Você faz push na própria Action
- ✅ Segunda-feira às 6h UTC (verificação semanal)

### 3. Executar manualmente

No GitHub: **Actions** → **Update README with GitHub Pages** → **Run workflow**

## 🔧 O que o sistema faz

1. **Lê** o arquivo `pages-config.yml`
2. **Verifica** se cada site está online (HTTP 200)
3. **Atualiza** o README.md com a seção "🌐 GitHub Pages"
4. **Faz commit** automaticamente se houver mudanças

## 📋 Exemplo de saída no README

```markdown
## 🌐 GitHub Pages
- **[Data Science Guide](https://alex-des-santos.github.io/datascients-guide/)** - Guia completo de Data Science
- **[CSV Insights Tool](https://alex-des-santos.github.io/csv-insights-tool/)** - Ferramenta para análise de arquivos CSV
```

## ⚠️ Considerações

- Sites offline não aparecem no README
- Verificação de status pode falhar por timeout de rede
- A Action só faz commit se há mudanças reais no README
