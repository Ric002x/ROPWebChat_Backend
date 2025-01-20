# ROPWebChat - Backend

## 📋Sobre

Este projeto é um **BACKEND** para um chat virtual em tempo real, inspirado em aplicativos populares como WhatsApp. Ele foi desenvolvido usando o Django Rest Framework (DRF) e tem como objetivo fornecer uma API REST robusta e escalável para suportar funcionalidades de comunicação em tempo real entre usuários.

Com esta API, é possível gerenciar:

- Criação e autenticação de usuários    
- Envio e recebimento de mensagens
- Suporte para mensagens multimídia, como imagens, áudios e vídeos.
- A arquitetura do projeto prioriza escalabilidade e facilidade de integração com clientes frontend ou aplicativos móveis, como React ou React Native.


## 🖥️Tecnologias

- **Python**: Linguagem de programação utilizada no backend.
- **Django**: Framework web para desenvolvimento rápido e seguro.
- **Django Rest Framework**: Ferramenta para criação de APIs RESTful robustas e escaláveis.


## 🔧Instalação


1. Clone o repositório:

   ```bash
   git clone https://github.com/Ric002x/ROPWebChat_Backend.git
   ```

2. Acesse o diretório do projeto:

   ```bash
   cd ROPWebChat_Backend
   ```

3. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv

   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

4. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```


## 📝Inicialização

1. Execute as migrações do banco de dados:

   ```bash
   python manage.py migrate
   ```

2. Inicie o servidor de desenvolvimento:

   ```bash
   python manage.py runserver
   ```

3. A API estará disponível em:  
   [http://localhost:8000](http://localhost:8000)


## Licença
Este projeto é licenciado sob a licença **MIT**. Consulte o arquivo `LICENSE` para mais informações.
