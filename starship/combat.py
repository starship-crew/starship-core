from multiprocessing import Process
from starship.data import db_session


def combat_connector():
    """Constantly searches for two opportune enemy crews to connect them in a
    combat."""
    pass


def combat_action_handler():
    """Constantly handles actions of different crews in a combat."""
    pass


connector = Process(target=combat_connector, name="CombatConnector")
action_handler = Process(target=combat_connector, name="CombatActionHandler")


def run_handlers():
    db_session.global_init()
    connector.start()
    action_handler.start()


def kill_handlers():
    connector.kill()
    action_handler.kill()
