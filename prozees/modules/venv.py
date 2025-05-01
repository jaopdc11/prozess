import os
import subprocess
import sys
from pathlib import Path
import click

def encontrar_python(versao=None):
    """Encontra o executável do Python na versão especificada ou usa o atual."""
    if not versao:
        return sys.executable

    versoes_testar = [f"python{versao}", f"python{versao.replace('.', '')}", f"python{versao.split('.')[0]}"]

    for py in versoes_testar:
        try:
            caminho = subprocess.check_output(["which", py], stderr=subprocess.PIPE, text=True).strip()
            if caminho:
                return caminho
        except subprocess.CalledProcessError:
            continue
    return None

def criar_venv(caminho_projeto, versao_python=None, verbose=False):
    """Cria um ambiente virtual Python."""
    venv_path = caminho_projeto / 'venv'

    if verbose:
        click.echo(f"\n🐍 Criando ambiente virtual em {venv_path}")

    if venv_path.exists():
        if verbose:
            click.echo("ℹ️ Ambiente virtual já existe")
        return True

    python_exec = encontrar_python(versao_python)
    if not python_exec:
        try:
            versoes_disponiveis = subprocess.check_output(["ls", "/usr/bin/python*"], text=True).strip()
        except subprocess.CalledProcessError:
            versoes_disponiveis = "Não foi possível listar as versões disponíveis."
        raise FileNotFoundError(
            f"Python versão {versao_python} não encontrado.\n"
            f"Versões disponíveis:\n{versoes_disponiveis}"
        )

    if verbose:
        click.echo(f"🔍 Usando Python: {python_exec}")

    resultado = subprocess.run(
        [python_exec, "-m", "venv", str(venv_path)],
        capture_output=True,
        text=True
    )

    if resultado.returncode != 0:
        erro = resultado.stderr or "Erro desconhecido ao criar venv"
        raise RuntimeError(f"Falha ao criar venv: {erro}")

    if verbose:
        click.echo("✅ Ambiente virtual criado com sucesso")
        pip_exec = venv_path / 'bin' / 'pip' if os.name != 'nt' else venv_path / 'Scripts' / 'pip.exe'
        versao_pip = subprocess.run([str(pip_exec), "--version"], capture_output=True, text=True)
        click.echo(versao_pip.stdout)

    return True

def instalar_dependencias(caminho_projeto, caminho_requirements=None, verbose=False):
    """Instala as dependências do projeto a partir do arquivo requirements.txt."""
    venv_path = caminho_projeto / 'venv'
    if not venv_path.exists():
        raise FileNotFoundError("Ambiente virtual não encontrado.")

    arquivo_req = Path(caminho_requirements) if caminho_requirements else caminho_projeto / 'requirements.txt'
    if not arquivo_req.exists():
        raise FileNotFoundError(f"Arquivo de requirements não encontrado: {arquivo_req}")

    if verbose:
        click.echo(f"\n📦 Instalando dependências de {arquivo_req}")

    pip_exec = venv_path / 'bin' / 'pip' if os.name != 'nt' else venv_path / 'Scripts' / 'pip.exe'

    resultado = subprocess.run(
        [str(pip_exec), "install", "-r", str(arquivo_req)],
        capture_output=True,
        text=True
    )

    if verbose:
        if resultado.returncode == 0:
            click.echo("✅ Dependências instaladas com sucesso")
            click.echo(resultado.stdout)
        else:
            click.echo(f"❌ Erro ao instalar dependências: {resultado.stderr}")

    return resultado.returncode == 0

def configurar_ambiente_projeto(caminho_projeto, versao_python=None, caminho_requirements=None, verbose=False):
    """Função principal para configurar o ambiente do projeto."""
    venv_criado = criar_venv(caminho_projeto, versao_python, verbose)
    if not venv_criado:
        return False

    if caminho_requirements or (caminho_projeto / 'requirements.txt').exists():
        return instalar_dependencias(caminho_projeto, caminho_requirements, verbose)

    return True
