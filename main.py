from sqlmodel import SQLModel
from sqlmodel.pool import StaticPool

from settings import Settings
from orm.database import create_sqlmodel_engine, sqlmodel_session_maker
from service_layer.uow import UnitOfWork
from schemas import Hero, Team


settings = Settings()
engine = create_sqlmodel_engine(settings=settings, poolclass=StaticPool)
SQLModel.metadata.create_all(engine)
session_maker = sqlmodel_session_maker(engine)


def print_team_members(team: Team):
    for member in team.heroes:
        print(f"Name {member.name}, Secret name {member.secret_name}")


with UnitOfWork(session_factory=session_maker) as uow:
    team = Team(name="Dream Team")
    team = uow.teams.add(team)

    uow.heroes.add(Hero(name="Toni Stark", secret_name="Iron Man", team_id=team.id))
    uow.heroes.add(Hero(name="Bruce Banner", secret_name="Hulk", team_id=team.id))
    uow.heroes.add(Hero(name="Steve Rogers", secret_name="Captain America", team_id=team.id))
    uow.heroes.add(Hero(name="John Wick", secret_name="John Wick", team_id=team.id))

    print("-------------------------- Print dream team ----------------------------------")
    print_team_members(team)

    hero_hulk = uow.heroes.list(name="Bruce Banner", secret_name="Hulk")[0]
    hero_hulk.secret_name = "Incredible Hulk"
    hero_hulk = uow.heroes.update(hero_hulk)

    print("-------------------------- Print updated dream team ----------------------------------")
    print_team_members(team)

    hero_john = uow.heroes.list(name="John Wick")[0]
    hero_john.team_id = None
    uow.heroes.update(hero_john)

    print("-------------------------- Remove member from dream team ----------------------------------")
    uow.heroes.delete(hero_john.id)
    hero_john = uow.heroes.get_by_id(hero_john.id)
    if hero_john is None:
        print("Deleted John Wick")
    uow.commit()
    print_team_members(team)
