import os
from pathlib import Path
import subprocess
import click
def create_project_folder(project_name, verbose=False):
    """Cria a pasta do projeto no diretório atual do usuário"""
    # Pega o diretório atual de trabalho (onde o usuário executou o comando)
    current_dir = Path.cwd()
    project_path = current_dir / project_name

    # Cria a pasta
    project_path.mkdir(parents=True, exist_ok=True)

    if verbose:
        print(f"[VERBOSE] Pasta criada em: {project_path}")
    return project_path

def command_git(project_path, verbose=False):
    """Inicializa um repositório Git na pasta do projeto e configura o branch inicial para 'main'."""
    try:
        if verbose:
            click.echo("\n🔧 Iniciando configuração do Git...")
            click.echo(f"📁 Diretório do projeto: {project_path}")

        # Executa git init no diretório do projeto
        git_init_result = subprocess.run(['git', 'init'],
                                         cwd=str(project_path),
                                         capture_output=True,
                                         text=True)

        # Verificação robusta da criação do repositório
        git_dir = project_path / '.git'
        success = git_dir.exists()

        if verbose:
            if success:
                click.echo(f"✅ Repositório Git criado com sucesso em: {git_dir}")
            else:
                click.echo("❌ Falha: Pasta .git não foi criada")

            # Mostra detalhes da execução do init
            click.echo("\n=== SAÍDA DO GIT INIT ===")
            click.echo(git_init_result.stdout or "(Nenhuma saída)")
            if git_init_result.stderr:
                click.echo("\n=== MENSAGENS DE ERRO DO GIT INIT ===")
                click.echo(git_init_result.stderr)

        if success:
            # Tenta configurar o branch inicial para 'main' localmente
            try:
                # Verifica a versão do Git (para evitar erros em versões antigas)
                version_output = subprocess.run(['git', '--version'], capture_output=True, text=True)
                version_str = version_output.stdout.strip().split(' ')[2]
                major, minor, patch = map(int, version_str.split('.'))

                # Configura init.defaultBranch para main se a versão for >= 2.28
                if major >= 3 or (major == 2 and minor >= 28):
                    config_result = subprocess.run(['git', 'config', 'init.defaultBranch', 'main'],
                                                   cwd=str(project_path),
                                                   capture_output=True,
                                                   text=True)
                    if verbose and config_result.returncode == 0:
                        click.echo("🌱 Branch inicial configurado para 'main'.")
                    elif verbose and config_result.stderr:
                        click.echo("\n⚠️ Aviso ao tentar configurar 'init.defaultBranch':")
                        click.echo(config_result.stderr)
                elif verbose:
                    click.echo("ℹ️ Versão do Git é anterior a 2.28, 'init.defaultBranch' não suportado.")

            except Exception as e:
                if verbose:
                    click.echo(f"\n⚠️ Erro ao tentar configurar 'init.defaultBranch': {e}")

            # Verificação adicional do status
            if verbose:
                status_result = subprocess.run(['git', 'status'],
                                                 cwd=str(project_path),
                                                 capture_output=True,
                                                 text=True)
                click.echo("\n=== STATUS DO REPOSITÓRIO ===")
                click.echo(status_result.stdout or "(Nenhuma saída)")
                if status_result.stderr:
                    click.echo("\n=== ERROS NO STATUS ===")
                    click.echo(status_result.stderr)

        return success

    except subprocess.CalledProcessError as e:
        if verbose:
            click.echo("\n❌ ERRO NA EXECUÇÃO DO GIT:")
            click.echo(f"Código: {e.returncode}")
            click.echo(f"Erro: {e.stderr}")
        return False
    except Exception as e:
        if verbose:
            click.echo("\n❌ ERRO INESPERADO:")
            click.echo(f"Tipo: {type(e).__name__}")
            click.echo(f"Detalhes: {str(e)}")
        return False
