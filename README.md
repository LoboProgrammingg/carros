# Sistema de Gerenciamento de Carros

Este projeto é um sistema de gerenciamento de carros que utiliza tecnologias front-end e back-end para fornecer uma interface responsiva e funcional. O objetivo é gerenciar informações relacionadas a carros de forma prática e eficiente.

---

## 🚀 Status do Projeto
- **Situação**: Em desenvolvimento
- **Última Atualização**: Abril de 2025

---

## 🛠️ Tecnologias Utilizadas
- **Front-End**:
  - **JavaScript**: Para manipulação da lógica do cliente.
  - **CSS**: Para estilização e design responsivo.
  - **HTML**: Para estruturação das páginas.
- **Back-End**:
  - **Python**: Para lógica do servidor e processamento de dados.

---

## 📋 Funcionalidades
- Interface responsiva para gerenciar informações de carros.
- Integração entre o front-end e o back-end.
- Lógica de negócios implementada no lado do servidor.
- Estilização moderna com CSS.

---

## 📂 Estrutura do Projeto
A estrutura do projeto é organizada da seguinte maneira:
```
carros/
├── accounts/               # Gerenciamento de contas e usuários
├── app/                    # Aplicação principal do sistema
├── cars/                   # Módulo para gerenciamento de carros
├── openai_api/             # Integrações com a API da OpenAI
├── static/images/          # Imagens utilizadas no sistema
├── staticfiles/            # Arquivos estáticos para produção
├── .gitignore              # Arquivo para ignorar arquivos e diretórios no Git
├── carros_uwsgi.ini        # Configuração do servidor uWSGI
├── manage.py               # Script de gerenciamento do Django
├── requirements.txt        # Dependências do projeto
└── uwsgi_params            # Configurações adicionais para o uWSGI
```

---

## 🧩 Como Usar

### 1. **Clone este repositório**
```bash
git clone https://github.com/LoboProgrammingg/carros.git
cd carros
```

### 2. **Configuração do Back-End**
- Certifique-se de que o Python esteja instalado em sua máquina.
- Crie e ative um ambiente virtual:
  ```bash
  python -m venv venv
  source venv/bin/activate  # No Windows: venv\Scripts\activate
  ```
- Instale as dependências necessárias:
  ```bash
  pip install -r requirements.txt
  ```

### 3. **Execute o Back-End**
- Inicie o servidor Django:
  ```bash
  python manage.py runserver
  ```

### 4. **Acesse a Página Inicial**
- Acesse o sistema no navegador em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📜 Próximos Passos
- [ ] Adicionar funcionalidades de busca e filtros para gerenciar carros.
- [ ] Implementar autenticação de usuários.
- [ ] Criar relatórios em PDF para exportação de dados.
- [ ] Melhorar a integração entre front-end e back-end.

---

## 👨‍💻 Contribuindo
Contribuições são bem-vindas! Siga as etapas abaixo:
1. Faça um fork do projeto.
2. Crie uma branch para suas alterações:
   ```bash
   git checkout -b minha-feature
   ```
3. Faça suas alterações e um commit:
   ```bash
   git commit -m "Minha nova feature"
   ```
4. Envie suas alterações para o repositório remoto:
   ```bash
   git push origin minha-feature
   ```
5. Abra um Pull Request.

---

Criado por **Matheus Lobo Camara**.
