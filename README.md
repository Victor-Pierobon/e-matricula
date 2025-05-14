# E-Matrícula - Sistema de Gestão Escolar

Sistema de gestão escolar desenvolvido para facilitar o processo de matrícula e gerenciamento de turmas no contexto do Novo Ensino Médio.

## Funcionalidades

### Públicas
- Página inicial informativa
- Sistema de login unificado
- Registro de novos usuários (Instituição, Docente, Discente)

### Instituição
- Dashboard com estatísticas gerais
- Gerenciamento de componentes curriculares
  - Adicionar novos componentes
  - Editar componentes existentes
  - Excluir componentes
- Visualização de turmas e alunos

### Docente
- Dashboard personalizado
  - Estatísticas de turmas e alunos
  - Aulas do dia
  - Próximas aulas
  - Lista de turmas ativas
- Gerenciamento de aulas
  - Visualização de horários
  - Edição de aulas
  - Controle de presença

### Discente
- Dashboard do aluno
  - Visualização de matrícula
  - Escolha de itinerários formativos
  - Grade de horários
  - Aulas do dia

## Tecnologias Utilizadas

- Python 3.13
- Django 5.1
- Bootstrap 5
- Font Awesome
- SQLite (desenvolvimento)

## Estrutura do Projeto

```
e-matricula/
├── core/                    # Aplicação principal
│   ├── migrations/         # Migrações do banco de dados
│   ├── templates/          # Templates HTML
│   │   └── html/          # Templates organizados por funcionalidade
│   ├── models.py          # Modelos do banco de dados
│   ├── views.py           # Lógica de negócio
│   └── urls.py            # Configuração de URLs
├── ematricula/            # Configurações do projeto
├── static/                # Arquivos estáticos
│   ├── css/              # Folhas de estilo
│   ├── js/               # Scripts JavaScript
│   └── img/              # Imagens
└── manage.py             # Script de gerenciamento do Django
```

## Modelos de Dados

### Instituição
- Informações básicas da instituição
- Gerenciamento de componentes curriculares

### Docente
- Vinculado à instituição
- Gerenciamento de aulas e turmas

### Discente
- Vinculado à instituição
- Matrícula em turmas
- Escolha de itinerários

### Componente Curricular
- Nome e área do conhecimento
- Tipo (BNCC ou Itinerário)
- Carga horária
- Vinculado à instituição

### Turma
- Vinculada à série
- Nome e turno
- Relacionamento com docentes através de aulas

### Aula
- Componente curricular
- Turma
- Docente responsável
- Dia da semana e horário

### Matrícula
- Discente
- Turma
- Itinerários escolhidos
- Data da matrícula

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/e-matricula.git
cd e-matricula
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute as migrações:
```bash
python manage.py migrate
```

5. Crie um superusuário:
```bash
python manage.py createsuperuser
```

6. Inicie o servidor:
```bash
python manage.py runserver
```

## URLs Principais

### Públicas
- `/` - Página inicial
- `/login/` - Login
- `/register/instituicao/` - Registro de instituição
- `/register/docente/` - Registro de docente
- `/register/discente/` - Registro de discente

### Instituição
- `/painel/instituicao/` - Dashboard
- `/componentes/` - Gerenciamento de componentes
- `/componentes/adicionar/` - Adicionar componente
- `/componentes/editar/<id>/` - Editar componente
- `/componentes/excluir/<id>/` - Excluir componente

### Docente
- `/painel/docente/` - Dashboard
- `/docente/aulas/` - Minhas aulas
- `/docente/turmas/` - Minhas turmas

### Discente
- `/painel/discente/` - Dashboard
- `/matricula/` - Visualizar matrícula
- `/matricula/escolher-itinerarios/` - Escolher itinerários

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 