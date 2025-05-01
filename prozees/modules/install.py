from pathlib import Path

def create_default_requirements(project_path, project_type):
    """Cria um requirements.txt padrão baseado no tipo de projeto"""
    requirements = {
        'web-flask': """flask==2.3.2
python-dotenv==1.0.0
pytest==7.4.0""",

        'web-fastapi': """fastapi==0.95.2
uvicorn==0.22.0
python-dotenv==1.0.0
pytest==7.4.0""",

        # Adicione outros templates conforme necessário
    }

    default_content = requirements.get(project_type, """# Dependências básicas
python-dotenv==1.0.0
pytest==7.4.0""")

    (project_path / 'requirements.txt').write_text(default_content)
