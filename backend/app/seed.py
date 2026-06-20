"""
Script simples para popular o banco com uma cidade e alguns cruzamentos do Grande
Recife. Para executar: `python -m app.seed`.  
Isso utiliza as funções CRUD e modelos definidos na aplicação para criar
registros. Em um ambiente de produção, recomenda-se usar arquivos de migração e
script de seed controlado pelo Alembic ou ferramentas similares.
"""

from sqlalchemy.orm import Session

from .core.database import SessionLocal
from . import crud, schemas


def run():
    db: Session = SessionLocal()

    # Cria a cidade Recife se ainda não existir
    existing_cities = crud.get_cities(db)
    recife = next((c for c in existing_cities if c.name.lower() == "recife"), None)
    if not recife:
        recife = crud.create_city(db, schemas.CityCreate(name="Recife", state="PE"))

    # Lista de cruzamentos com nomes e descrições
    intersections_data = [
        {
            "name": "Av. Abdias de Carvalho x Av. do Forte",
            "description": "Cruzamento movimentado na zona oeste, próximo ao bairro da Várzea.",
        },
        {
            "name": "Av. Beberibe x Rua São Bento",
            "description": "Ponto crítico próximo ao bairro de Beberibe, na zona norte.",
        },
        {
            "name": "Av. Norte x Cruz Cabugá",
            "description": "Cruzamento importante que liga áreas centrais e norte do Recife.",
        },
        {
            "name": "Antonio Falcão x Domingos Ferreira",
            "description": "Interseção na Zona Sul próxima a Boa Viagem e imediações do Shopping Center Recife.",
        },
    ]

    # Cria cruzamentos e câmeras básicas
    for item in intersections_data:
        intersection = crud.create_intersection(
            db,
            schemas.IntersectionCreate(
                name=item["name"],
                description=item.get("description"),
                city_id=recife.id,
            ),
        )
        # Cria uma câmera associada (RTSP fictícia apenas para exemplo)
        crud.create_camera(
            db,
            schemas.CameraCreate(
                name=f"Camera principal - {item['name']}",
                rtsp_url=f"rtsp://exemplo/{item['name'].replace(' ', '').lower()}",
                intersection_id=intersection.id,
            ),
        )

    print("Seed executado com sucesso!")


if __name__ == "__main__":
    run()