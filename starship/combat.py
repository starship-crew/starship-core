import random

from multiprocessing import Process
from time import sleep
from starship.data import db_session
from starship.data.action import ActionKind
from starship.data.combat import Combat
from starship.data.crew import Crew
from starship.data.sentence import Sentence
from starship.helpers import get_lang


def determine_first_actor(crew1, crew2):
    """Decide who should move first in a combat after one's creation."""
    (crew2 if crew1.currency > crew2.currency else crew1).active = True


def make_combat(db_sess, crew1, crew2):
    crew1.searching = False
    crew2.searching = False

    combat = Combat()
    combat.crews.append(crew1)
    combat.crews.append(crew2)
    determine_first_actor(crew1, crew2)
    crew1.combat = combat
    crew2.combat = combat

    db_sess.add(combat)
    db_sess.commit()


def combat_connector():
    """Constantly searches for two opportune enemy crews to connect them in a
    combat."""
    db_sess = db_session.create_session()

    while True:
        for crew1 in db_sess.query(Crew).filter(Crew.searching):
            found = False
            for crew2 in db_sess.query(Crew).filter(
                Crew.searching,
                Crew.id != crew1.id,
                Crew.currency.between(crew1.currency * 0.5, crew1.currency * 1.5),
            ):
                if not (crew1.searching and crew2.searching):
                    continue
                make_combat(db_sess, crew1, crew2)
                found = True
                break
            if (
                not found
                and crew1.searching
                and (
                    crew2 := db_sess.query(Crew)
                    .filter(Crew.searching, Crew.id != crew1.id)
                    .first()
                )
            ):
                make_combat(db_sess, crew1, crew2)
        sleep(0.5)


def has_hit(enemy_mobility):
    """Returns whether has hit with the chance constructed from enemy mobility."""
    misfire_chance = enemy_mobility
    hit_chance = 1 - enemy_mobility
    return random.choices([False, True], weights=[misfire_chance, hit_chance])


def apply_action(db_sess, crew, enemy):
    match crew.action.kind:
        case ActionKind.Attack:
            weapon = crew.ship.detail("weapon")

            if has_hit(enemy.ship.mobility):
                if part := crew.action.part:
                    part.health -= weapon.damage
                    part_name = part.name.get(get_lang())
                    crew.action_comment = Sentence(
                        ru=f"{part_name} корабля соперника был(и) повреждены",
                        en=f"{part_name} of the enemy's ship was damaged",
                    )
                else:
                    part = random.choice(enemy.ship.details)
                    part.health -= weapon.damage
                    crew.action_comment = Sentence(
                        ru="Вы нанесли урон кораблю соперника",
                        en="You has damaged the enemy",
                    )

                if part.health < 0:
                    part.health = 0
            else:
                crew.action_comment = Sentence(
                    ru="Вы промахнулись",
                    en="You has misfired",
                )

            enemy.ship.enhanced_mobility = 0.0
        case ActionKind.Dodge:
            crew.ship.enhanced_mobility += 0.2
        case ActionKind.FoolGiveUp:
            raise NotImplementedError
        case ActionKind.SmartGiveUp:
            raise NotImplementedError
        case ActionKind.SelfDestruct:
            raise NotImplementedError
        case ActionKind.Quit:
            crew.combat = None


def combat_action_handler():
    """Constantly handles actions of different crews in a combat."""
    db_sess = db_session.create_session()

    while True:
        for crew in db_sess.query(Crew).filter(Crew.active, Crew.action != None):
            enemy = crew.opponent
            crew.active = False
            enemy.active = True
            apply_action(db_sess, crew, enemy)
            crew.action = None
            db_sess.commit()
        sleep(0.5)


connector = Process(target=combat_connector, name="CombatConnector")
action_handler = Process(target=combat_action_handler, name="CombatActionHandler")


def run_handlers():
    db_session.make_thread_safe()
    connector.start()
    action_handler.start()


def kill_handlers():
    connector.kill()
    action_handler.kill()
