import click
from pathlib import Path
from modules.dirs import create_project_folder, command_git
from modules.venv import criar_venv, instalar_dependencias
from modules.install  import create_default_requirements

@click.command()
@click.argument('architecture', type=click.Choice(['mvc', 'mvvm', 'clean', 'microservices', 'layered']))
@click.argument('project_name')
@click.option(
    '-t', '--type',
    type=click.Choice(['web-flask', 'web-fastapi', 'web-rest', 'web-grpc', 'cli', 'data-science', 'microservice'],
                     case_sensitive=False),
    required=True,
    help='Tipo de projeto a ser criado'
)
@click.option('-v', '--verbose', is_flag=True, help='Modo detalhado')
@click.option('--no-docker', is_flag=True, help='Pular configuração do Docker')
@click.option(
    '-r', '--requirements',
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help='Arquivo requirements.txt customizado'
)
@click.option('--git', is_flag=True, help='Inicializar repositório Git')
@click.option(
    '-l', '--license',
    type=click.Choice(['mit', 'apache', 'gpl', 'none'], case_sensitive=False),
    default='none',
    help='Tipo de licença'
)
@click.option('--venv', is_flag=True, help='Criar ambiente virtual')
@click.option(
    '--python-version',
    type=str,
    default=None,
    help='Versão do Python para o venv (ex: 3.9)'
)
@click.option('--install-deps', is_flag=True, help='Instalar dependências automaticamente')
def new(architecture, project_name, type, verbose, no_docker, requirements, git, license, venv, python_version, install_deps):
    """Cria um novo projeto Python com arquitetura específica

    ARCHITECTURE: Arquitetura do projeto (mvc, mvvm, clean, etc.)
    PROJECT_NAME: Nome do diretório do projeto
    """
    try:
        # Cria pasta do projeto
        project_path = create_project_folder(project_name, verbose)
        click.echo(f"🚀 Criando projeto {type} com arquitetura {architecture.upper()}: {project_name}")

        # Configura estrutura baseada na arquitetura
        if verbose:
            click.echo(f"⚙️  Configurando estrutura {architecture}...")
            # Adicionar lógica específica de arquitetura aqui

        # Configuração específica para projetos web
        if type.startswith('web-'):
            web_type = type.split('-')[1]
            if verbose:
                click.echo(f"🕸️  Configurando projeto {web_type}...")
            # Adicionar lógica específica para web aqui

        # Configurações comuns
        if verbose:
            click.echo("🔍 Modo detalhado ativado")

        # Configuração do Docker
        if not no_docker:
            if verbose:
                click.echo("🐳 Configurando Docker...")
            # setup_docker(project_path, type, architecture, verbose)

        # Configuração do ambiente virtual
        if venv:
            if verbose:
                click.echo("\n🐍 Configuração do ambiente virtual:")

            venv_success = criar_venv(project_path, python_version, verbose)

            if venv_success and install_deps:
                # Cria requirements.txt padrão se não existir
                if not requirements and not (project_path / 'requirements.txt').exists():
                    create_default_requirements(project_path, type)
                    if verbose:
                        click.echo("ℹ️ Arquivo requirements.txt padrão criado")

                # Instala dependências
                req_file = requirements if requirements else 'requirements.txt'
                if (project_path / req_file).exists():
                    install_success = instalar_dependencias(project_path, req_file, verbose)
                    if not install_success:
                        click.echo("⚠️ Falha ao instalar dependências")
                elif verbose:
                    click.echo("ℹ️ Nenhum arquivo de dependências encontrado")

        # Inicialização do Git
        if git:
            if verbose:
                click.echo("\n🔧 Configurando repositório Git:")
            git_success = command_git(project_path, verbose)
            if not git_success and verbose:
                click.echo("❌ Falha ao inicializar repositório Git")

        # Configuração de licença
        if license != 'none':
            if verbose:
                click.echo(f"\n📜 Aplicando licença {license}...")
            # apply_license(project_path, license, verbose)

        # Mensagem final
        click.echo(f"\n🎉 Projeto criado com sucesso em: {project_path}")
        click.echo(f"Arquitetura: {architecture.upper()} | Tipo: {type}")

        if venv:
            click.echo("\nPara ativar o ambiente virtual:")
            click.echo(f"source {project_path}/venv/bin/activate  # Linux/Mac")
            click.echo(f"{project_path}\\venv\\Scripts\\activate  # Windows")

    except Exception as e:
        click.echo(f"\n❌ Erro ao criar projeto: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    import sys
    new()
