from models.manager import Manager
import config.settings as settings
from config.database import session


# ---------------------------------------------------------------------------- #
#                             Auxilliary functions                             #
# ---------------------------------------------------------------------------- #

def is_manager(building_id):
    '''Returns True if user is manager of the building'''
    manager_idp_id =  settings.request_payload["sub"]
    manager = session.query(Manager).filter(Manager.idp_id == manager_idp_id).first()
    building = list(filter(lambda b: b.id == building_id, manager.company.buildings))

    return True if len(building) else False

def is_admin():
    manager_idp_id =  settings.request_payload["sub"]
    manager = session.query(Manager).filter(Manager.idp_id == manager_idp_id).first()

    return True if manager.permissions == 4 else False