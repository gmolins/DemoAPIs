from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session, select, Relationship
from pydantic import ValidationError, field_validator  # Importar para validaciones

# Definición del modelo Team
class Team(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(..., min_length=1, description="El nombre del equipo no puede estar vacío.")
    headquarters: str
    heroes: list["Hero"] = Relationship(back_populates="team") # Relación inversa con Hero

    @field_validator("name", mode="before")
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("El nombre del equipo no puede estar vacío.")
        return value

# Clase base Person
class Person(SQLModel):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(..., min_length=1, description="El nombre no puede estar vacío.")
    age: Optional[int] = Field(default=None, ge=0, description="La edad debe ser un número positivo.")

    @field_validator("name", mode="before")
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("El nombre no puede estar vacío.")
        return value

    @field_validator("age", mode="before")
    def validate_age(cls, value):
        if value is not None and value < 0:
            raise ValueError("La edad debe ser un número positivo.")
        return value

# Clase Hero que hereda de Person
class Hero(Person, table=True):
    secret_name: str
    team_id: Optional[int] = Field(default=None, foreign_key="team.id") # Clave foránea
    team: Optional["Team"] = Relationship(back_populates="heroes") # Relación con Team

# Conexión a la base de datos
engine = create_engine("sqlite:///heroes.db")

# Creación de las tablas
def create_tables():
    SQLModel.metadata.create_all(engine)

# Inserción de datos
def insert_data():
    try:
        with Session(engine) as session:
            avengers = Team(name="Avengers", headquarters="New York")
            x_men = Team(name="X-Men", headquarters="X-Mansion")
            justice_league = Team(name="Justice League", headquarters="Hall of Justice")
            heroes = [
                Hero(name="Spider-Man", secret_name="Peter Parker", age=18, team=avengers),
                Hero(name="Iron Man", secret_name="Tony Stark", age=45, team=avengers),
                Hero(name="Thor", secret_name="Thor Odinson", age=1500, team=avengers),
                Hero(name="Hulk", secret_name="Bruce Banner", age=40, team=avengers),
                Hero(name="Wolverine", secret_name="Logan", age=200, team=x_men),
                Hero(name="Storm", secret_name="Ororo Munroe", age=30, team=x_men),
                Hero(name="Cyclops", secret_name="Scott Summers", age=35, team=x_men),
                Hero(name="Superman", secret_name="Clark Kent", age=35, team=justice_league),
                Hero(name="Batman", secret_name="Bruce Wayne", age=40, team=justice_league),
                Hero(name="Wonder Woman", secret_name="Diana Prince", age=1000, team=justice_league),
            ]
            session.add_all([avengers, x_men, justice_league] + heroes)
            session.commit()
            print("Datos insertados correctamente.")
    except Exception as e:
        print(f"Error ine9sperado al insertar datos: {e}")

# Consulta de datos con Join
def get_heroes_with_teams():
    try:
        with Session(engine) as session:
            statement = select(Hero, Team).join(Team, Hero.team_id == Team.id)
            results = session.exec(statement).all()
            print("Héroes con sus equipos:")
            for hero, team in results:
                print(f"- {hero.name} pertenece al equipo {team.name} (Sede: {team.headquarters})")
    except Exception as e:
        print(f"Error inesperado al consultar héroes con equipos: {e}")

# Crear un héroe y añadirlo a un equipo
def create_hero(name: str, secret_name: str, age: int, team_name: str):
    try:
        # Validar los datos antes de crear la instancia
        validated_hero = Hero.model_validate({
            "name": name,
            "secret_name": secret_name,
            "age": age
        })

        with Session(engine) as session:
            team = session.exec(select(Team).where(Team.name == team_name)).first()
            if team:
                new_hero = Hero(**validated_hero.model_dump(), team=team)
                session.add(new_hero)
                session.commit()
                print(f"Héroe {name} creado y añadido al equipo {team.name}.")
            else:
                print(f"No se encontró el equipo {team_name}.")
    except ValidationError as err:
        print("Error de validación:")
        print(err.json(indent=4))
    except Exception as e:
        print(f"Error inesperado al crear el héroe: {e}")

# Crear un equipo
def create_team(name: str, headquarters: str):
    try:
        # Validar los datos antes de crear la instancia
        validated_team = Team.model_validate({
            "name": name,
            "headquarters": headquarters
        })

        with Session(engine) as session:
            new_team = Team(**validated_team.model_dump())
            session.add(new_team)
            session.commit()
            print(f"Equipo {name} creado.")
    except ValidationError as err:
        print("Error de validación:")
        print(err.json(indent=4))
    except Exception as e:
        print(f"Error inesperado al crear el equipo: {e}")

# Consulta de todos los teams
def get_teams():
    try:
        with Session(engine) as session:
            teams = session.exec(select(Team)).all()
            print("Lista de equipos:")
            for team in teams:
                print(f"- {team.name} (Sede: {team.headquarters})")
    except Exception as e:
        print(f"Error inesperado al consultar equipos: {e}")

# Consulta de datos
def get_heroes():
    try:
        with Session(engine) as session:
            heroes = session.exec(select(Hero)).all()
            print("Lista de héroes:")
            for hero in heroes:
                print(f"- {hero.name} (Edad: {hero.age})")
    except Exception as e:
        print(f"Error inesperado al consultar héroes: {e}")

# Consulta de héroe por nombre
def get_hero_by_name(name: str):
    try:
        with Session(engine) as session:
            hero = session.exec(select(Hero).where(Hero.name == name)).first()
            if hero:
                print(f"Héroe encontrado: {hero.name} (Edad: {hero.age}, Nombre Secreto: {hero.secret_name})")
            else:
                print(f"No se encontró un héroe con el nombre {name}.")
    except Exception as e:
        print(f"Error inesperado al consultar el héroe por nombre: {e}")

# Actualización de datos
def update_hero_age(name: str, new_age: int):
    
    try:
        with Session(engine) as session:
            hero = session.exec(select(Hero).where(Hero.name == name)).first()
            if hero:
                hero.age = new_age
                validated_hero = Hero.model_validate(hero.model_dump())
                session.commit()
                print(f"Edad actualizada de {hero.name}: {hero.age}")
            else:
                print(f"No se encontró un héroe con el nombre {name}.")
    except Exception as e:
        print(f"Error inesperado al actualizar la edad del héroe: {e}")

# Actualización de edad a todos los héroes por nombre de Team
def update_hero_age_by_team(team_name: str, new_age: int):

    if not isinstance(new_age, int):
        print("La nueva edad debe ser un número entero.")
        return
    try:
        with Session(engine) as session:
            heroes = session.exec(select(Hero).join(Team).where(Team.name == team_name)).all()
            if not heroes:
                print(f"No se encontraron héroes en el equipo {team_name}.")
                return
            
            for hero in heroes:
                hero.age = new_age
            session.commit()
            print(f"Edad actualizada a {new_age} años para todos los héroes del equipo {team_name}.")
    except Exception as e:
        print(f"Error inesperado al actualizar la edad de los héroes por equipo: {e}")

# Eliminación de datos
def delete_hero(name: str):
    try:
        with Session(engine) as session:
            hero = session.exec(select(Hero).where(Hero.name == name)).first()
            if hero:
                session.delete(hero)
                session.commit()
                print(f"{hero.name} ha sido eliminado de la base de datos.")
            else:
                print(f"No se encontró un héroe con el nombre {name}.")
    except Exception as e:
        print(f"Error inesperado al eliminar el héroe: {e}")

# Eliminación de datos por ID
def delete_hero_by_id(hero_id: int):
    try:
        with Session(engine) as session:
            hero = session.get(Hero, hero_id)
            if hero:
                session.delete(hero)
                session.commit()
                print(f"Héroe con ID {hero_id} ha sido eliminado de la base de datos.")
            else:
                print(f"No se encontró un héroe con ID {hero_id}.")
    except Exception as e:
        print(f"Error inesperado al eliminar el héroe por ID: {e}")

    
# Eliminación de héroes por nombre de team
def delete_hero_by_team(team_name: str):
    try:
        with Session(engine) as session:
            heroes = session.exec(select(Hero).join(Team).where(Team.name == team_name)).all()
            for hero in heroes:
                session.delete(hero)
            session.commit()
            print(f"{len(heroes)} héroes del equipo {team_name} han sido eliminados.")
    except Exception as e:
        print(f"Error inesperado al eliminar héroes por equipo: {e}")

# Eliminación de héroes por ID de team
def delete_hero_by_team_id(team_id: int):
    try:
        with Session(engine) as session:
            heroes = session.exec(select(Hero).where(Hero.team_id == team_id)).all()
            for hero in heroes:
                session.delete(hero)
            session.commit()
            print(f"{len(heroes)} héroes del equipo con ID {team_id} han sido eliminados.")
    except Exception as e:
        print(f"Error inesperado al eliminar héroes por ID de equipo: {e}")

# Vaciar los datos de la tabla
def delete_heroes():
    try:
        with Session(engine) as session:
            heroes = session.exec(select(Hero)).all()
            for hero in heroes:
                session.delete(hero)
            session.commit()
            print(f"{len(heroes)} héroes han sido eliminados.")
    except Exception as e:
        print(f"Error inesperado al eliminar héroes: {e}")

def delete_teams():
    try:
        with Session(engine) as session:
            teams = session.exec(select(Team)).all()
            for team in teams:
                session.delete(team)
            session.commit()
            print(f"{len(teams)} equipos han sido eliminados.")
    except Exception as e:
        print(f"Error inesperado al eliminar equipos: {e}")

def delete_team(team_name: str):
    try:
        with Session(engine) as session:
            team = session.exec(select(Team).where(Team.name == team_name)).first()
            if team:
                heroes = session.exec(select(Hero).where(Hero.team_id == team.id)).all()
                if heroes:
                    print(f"No se puede eliminar el equipo '{team.name}' porque tiene héroes asociados.")
                else:
                    session.delete(team)
                    session.commit()
                    print(f"El equipo '{team.name}' ha sido eliminado de la base de datos.")
            else:
                print(f"No se encontró un equipo con el nombre '{team_name}'.")
    except Exception as e:
        print(f"Error inesperado al eliminar el equipo: {e}")

# Borrar la base de datos
def delete_database():
    try:
        import os
        if os.path.exists("heroes.db"):
            os.remove("heroes.db")
            print("Base de datos eliminada.")
        else:
            print("La base de datos no existe.")
    except Exception as e:
        print(f"Error inesperado al eliminar la base de datos: {e}")

# borrar todas las tablas
def delete_all_tables():
    try:
        SQLModel.metadata.drop_all(engine)
        print("Todas las tablas han sido eliminadas.")
    except Exception as e:
        print(f"Error inesperado al eliminar todas las tablas: {e}")

def delete_all():
    delete_heroes()
    delete_teams()
        
# Ejecución del script
if __name__ == "__main__":
    #delete_all_tables()
    #create_tables()
    # insert_data()
    # delete_heroes()
    # delete_teams()
    # delete_all()
    # delete_all_tables()

    # get_heroes_with_teams()
    # get_heroes()
    # get_hero_by_name("Wolverine")
    # get_heroes_with_teams()
    # get_teams()
    update_hero_age("Spider-Man", 19)
    # update_hero_age_by_team("Avengers", 30)
    # delete_hero("Iron Man")
    # delete_hero_by_id(4)
    # delete_hero_by_team_id(1)

    # create_hero("Black Widow", "Natasha Romanoff", 33, "Avengers")
    # create_team("Guardians of the Galaxy", "Space")