import hd_db
import loggy
from pprintpp import pprint as pp
# from sqlalchemy import delete
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date, timedelta
from pathlib import Path

short_script_name = Path(__file__).stem
logger = loggy.logging.getLogger(short_script_name)
db=hd_db.connect_db()
Session = sessionmaker(bind=db)
session = Session()

## Agents
def get_agents(agents:dict = None, all: bool = False, email:str = None, iid:int = None):
    if all:
        return session.query(hd_db.Agents) \
            .filter(
            hd_db.Agents.ss_id == agents.get('ss_id')
        ).all()
    if email:
        return session.query(hd_db.Agents) \
            .filter(
                hd_db.Agents.email == email,
                hd_db.Agents.ss_id == agents.get('ss_id')
                ).first()
    if iid:
        return session.query(hd_db.Agents) \
        .filter(
            hd_db.Agents.iid == iid
        ).first()  
    return session.query(hd_db.Agents) \
        .filter(
            hd_db.Agents.id == agents['id'],
            hd_db.Agents.ss_id == agents.get('ss_id')
        ).first()
def get_agent_groups(groups:dict = None, all: bool = False,  name:str = None, iid:int = None):
    if all:
        return session.query(hd_db.Agent_Groups) \
            .filter(
                hd_db.Agent_Groups.ss_id == groups.get('ss_id'),    
            ).all()
    if name:
        return session.query(hd_db.Agent_Groups) \
            .filter(
                hd_db.Agent_Groups.name == name,
                hd_db.Agent_Groups.ss_id == groups.get('ss_id')
                ).first()
    if iid:
        return session.query(hd_db.Agent_Groups) \
        .filter(
            hd_db.Agent_Groups.iid == iid
        ).first()
    return session.query(hd_db.Agent_Groups) \
        .filter(
            hd_db.Agent_Groups.id == groups['id'],
            hd_db.Agent_Groups.ss_id == groups.get('ss_id'),
        ).first()
def insert_agents(agents:dict = None):
    if get_agents(agents):
        return
    try:
        add = hd_db.Agents(**agents)
        session.add(add)
        session.commit()
    except Exception as e:
        logger.error(f"Failed to add agent: {e}")
        return False
    return add.iid
def insert_agent_groups(groups:dict = None):
    if get_agent_groups(groups):
        return
    try:
        add = hd_db.Agent_Groups(**groups)
        session.add(add)
        session.commit()
    except Exception as e:
        logger.error(f"Failed to add agent groups: {e}")
        return False
    return add.iid

## Assets
def insert_assets(assets:dict = None):
    if get_assets(assets):
        return
    try:
        add = hd_db.Assets(**assets)
        session.add(add)
        session.commit()
    except Exception as e:
        logger.error(f"Failed to add asset: {e}")
        return False
    return add.iid  
def get_assets(assets:dict = None, all: bool = False, name:str = None, iid:int = None, display_id:int = None):
    if all:
        return session.query(hd_db.Assets) \
            .filter(
                hd_db.Assets.ss_id == assets.get('ss_id')
            ).all()
    if name:
        return session.query(hd_db.Assets) \
        .filter(
            hd_db.Assets.name == name,
            hd_db.Assets.ss_id == assets.get('ss_id')
        ).first()
    if iid:
        return session.query(hd_db.Assets) \
        .filter(
            hd_db.Assets.iid == iid
        ).first()
    if display_id:
        return session.query(hd_db.Assets) \
        .filter(
            hd_db.Assets.display_id == display_id
        ).first()
    return session.query(hd_db.Assets) \
        .filter(
            hd_db.Assets.id == assets['id'],
            hd_db.Assets.ss_id == assets.get('ss_id')
        ).first()

## Custom_Objects
def insert_custom_objects(custom_objects:dict = None):
    if get_custom_objects(custom_objects):
        return
    try:
        add = hd_db.Custom_Objects(**custom_objects)
        session.add(add)
        session.commit()
    except Exception as e:
        logger.error(f"Failed to add custom object: {e}")
        return False
    return add.iid
def insert_custom_object_records(records:dict = None):
    
    try:
        add = hd_db.Custom_Object_Records(**records)
        session.add(add)
        session.commit()
    except Exception as e:
        logger.error(f"Failed to add custom object record: {e}")
        return False
    return add.iid
def get_custom_objects(custom_objects:dict = None, all: bool = False, title:str = None):
    if all:
        return session.query(hd_db.Custom_Objects) \
            .filter(
                hd_db.Custom_Objects.ss_id == custom_objects.get('ss_id')
            ).all()
    if title:
        return session.query(hd_db.Custom_Objects) \
        .filter(
            hd_db.Custom_Objects.title == title,
            hd_db.Custom_Objects.ss_id == custom_objects.get('ss_id')
        ).first()
    return session.query(hd_db.Custom_Objects) \
        .filter(
            hd_db.Custom_Objects.id == custom_objects['id'],
            hd_db.Custom_Objects.ss_id == custom_objects.get('ss_id')
        ).first()
def get_custom_object_records(records:dict = None, all: bool = False, iid:int = None, custom_object_id:int = None):
    if all:
        return session.query(hd_db.Custom_Object_Records) \
            .filter(
                hd_db.Custom_Object_Records.ss_id == records.get('ss_id')
            ).all()
    if custom_object_id:
        return session.query(hd_db.Custom_Object_Records) \
        .filter(
            hd_db.Custom_Object_Records.custom_object_id == custom_object_id,
            hd_db.Custom_Object_Records.ss_id == records.get('ss_id')
        ).all()
    if iid:
        return session.query(hd_db.Custom_Object_Records) \
        .filter(
            hd_db.Custom_Object_Records.iid == iid
        ).first()
    return session.query(hd_db.Custom_Object_Records) \
        .filter(
            hd_db.Custom_Object_Records.custom_object_id == records['custom_object_id'],
            hd_db.Custom_Object_Records.ss_id == records.get('ss_id')
        ).first()
##Departments
def insert_departments(departments:dict = None):
    if get_departments(departments):
        return
    try:
        add = hd_db.Departments(**departments)
        session.add(add)
        session.commit()
    except Exception as e:
        logger.error(f"Failed to add department: {e}")
        return False
    return add.iid
def get_departments(departments:dict = None, all: bool = False, name:str = None, iid:int = None):
    if all:
        return session.query(hd_db.Departments) \
            .filter(
                hd_db.Departments.ss_id == departments.get('ss_id'),
            ).all()
    if name:
        return session.query(hd_db.Departments) \
            .filter(
                hd_db.Departments.name == name,
                hd_db.Departments.ss_id == departments.get('ss_id')
                ).first()
    if iid:
        return session.query(hd_db.Departments) \
        .filter(
            hd_db.Departments.iid == iid
        ).first()
    return session.query(hd_db.Departments) \
        .filter(
            hd_db.Departments.id == departments['id'],
            hd_db.Departments.ss_id == departments.get('ss_id')
        ).first()

##Locations
def insert_locations(locations:dict = None):
    if get_locations(locations):
        return
    try:
        add = hd_db.Locations(**locations)
        session.add(add)
        session.commit()
    except Exception as e:
        logger.error(f"Failed to add location: {e}")
        return False
    return add.iid
def get_locations(locations:dict = None, all: bool = False, iid:int = None):
    if all:
        return session.query(hd_db.Locations) \
            .filter(
                hd_db.Locations.ss_id == locations.get('ss_id'),
            ).all()
    if iid:
        return session.query(hd_db.Locations) \
        .filter(
            hd_db.Locations.iid == iid
        ).first()
    return session.query(hd_db.Locations) \
        .filter(
            hd_db.Locations.id == locations['id'],
            hd_db.Locations.ss_id == locations.get('ss_id')
        ).first()

## Requesters
def insert_requesters(requesters:dict = None):
    if get_requesters(requesters):
        return
    try:
        add = hd_db.Requesters(**requesters)
        session.add(add)
        session.commit()
    except Exception as e:
        logger.error(f"Failed to add requester: {e}")
        return False
    return add.iid
def insert_requester_groups(requester_groups:dict = None):
    if get_requester_groups(requester_groups):
        return
    try:
        add = hd_db.Requester_Groups(**requester_groups)
        session.add(add)
        session.commit()
    except Exception as e:
        logger.error(f"Failed to add requesters group: {e}")
        return False
    return add.iid
def get_requesters(requesters:dict = None, all: bool = False, iid:int = None, primary_email:str = None):
    if all:
        return session.query(hd_db.Requesters) \
            .filter(
                hd_db.Requesters.ss_id == requesters.get('ss_id'),
            ).all()
    if primary_email:
        return session.query(hd_db.Requesters) \
        .filter(
            hd_db.Requesters.primary_email == primary_email,
            hd_db.Requesters.ss_id == requesters.get('ss_id')
        ).first()
    if iid:
        return session.query(hd_db.Requesters) \
        .filter(
            hd_db.Requesters.iid == iid
        ).first()
    return session.query(hd_db.Requesters) \
        .filter(
            hd_db.Requesters.id == requesters['id'],
            hd_db.Requesters.ss_id == requesters.get('ss_id'),
        ).first()
def get_requester_groups(requester_groups:dict = None, all: bool = False, name:str = None, iid:int = None):
    if all:
        return session.query(hd_db.Requester_Groups) \
            .filter(
                hd_db.Requester_Groups.ss_id == requester_groups.get('ss_id')
            ).all()
    if name:
        return session.query(hd_db.Requester_Groups) \
        .filter(
            hd_db.Requester_Groups.name == name,
            hd_db.Requester_Groups.ss_id == requester_groups.get('ss_id')
        ).first()
    if iid:
        return session.query(hd_db.Requester_Groups) \
        .filter(
            hd_db.Requester_Groups.iid == iid
        ).first()
    return session.query(hd_db.Requester_Groups) \
        .filter(hd_db.Requester_Groups.id == requester_groups['id'],
                hd_db.Requester_Groups.ss_id == requester_groups.get('ss_id')
        ).first()

##Tickets
def insert_tickets(tickets:dict = None):
    if get_tickets(tickets):
        return
    try:
        add = hd_db.Tickets(**tickets)
        session.add(add)
        session.commit()
    except Exception as e:
        logger.error(f"Failed to add ticket: {e}")
        return False
    return add.iid
def get_tickets(tickets:dict = None, all: bool = False, subject:str = None, iid:int = None):
    if all:
        return session.query(hd_db.Tickets) \
            .filter(
                hd_db.Tickets.ss_id == tickets.get('ss_id')
            ).all()
    if subject:
        return session.query(hd_db.Tickets) \
            .filter(
                hd_db.Tickets.subject == subject,
                hd_db.Tickets.ss_id == tickets.get('ss_id')
                ).first()
    if iid:
        return session.query(hd_db.Tickets) \
        .filter(
            hd_db.Tickets.iid == iid
        ).first()
    return session.query(hd_db.Tickets) \
        .filter(
            hd_db.Tickets.id == tickets['id'],
            hd_db.Tickets.ss_id == tickets.get('ss_id')
        ).first()

## Vendors
def insert_vendors(vendors:dict = None):
    if get_vendors(vendors):
        return
    try:
        add = hd_db.Vendors(**vendors)
        session.add(add)
        session.commit()
    except Exception as e:
        logger.error(f"Failed to add vendor: {e}")
        return False
    return add.iid
def get_vendors(vendors:dict = None, all: bool = False, name:str = None, iid:int = None):
    if all:
        return session.query(hd_db.Vendors) \
            .filter(
                hd_db.Vendors.ss_id == vendors.get('ss_id')    
            ).all()
    if name:
        return session.query(hd_db.Vendors) \
            .filter(
                hd_db.Vendors.name == name,
                hd_db.Vendors.ss_id == vendors.get('ss_id')
                ).first()
    if iid:
        return session.query(hd_db.Vendors) \
        .filter(
            hd_db.Vendors.iid == iid
        ).first()
    return session.query(hd_db.Vendors) \
        .filter(
            hd_db.Vendors.id == vendors['id'],
            hd_db.Vendors.ss_id == vendors.get('ss_id')
        ).first()

## Service (Note: We can store this data but cannot post/put it)
def insert_service_categories(service_categories:dict = None):
    if get_service_categories(service_categories):
        return
    try:
        add = hd_db.Service_Categories(**service_categories)
        session.add(add)
        session.commit()
    except Exception as e:
        logger.error(f"Failed to add service category: {e}")
        return False
    return add.iid
def insert_service_items(service_items:dict = None):
    if get_service_items(service_items):
        return
    try:
        add = hd_db.Service_Items(**service_items)
        session.add(add)
        session.commit()
    except Exception as e:
        logger.error(f"Failed to add service item: {e}")
        return False
    return add.iid
def get_service_categories(service_categories:dict = None, all: bool = False, name:str = None, iid:int = None):
    if all:
        return session.query(hd_db.Service_Categories) \
            .filter(
                hd_db.Service_Categories.ss_id == service_categories.get('ss_id')
            ).all()
    if name:
        return session.query(hd_db.Service_Categories) \
            .filter(
                hd_db.Service_Categories.name == name,
                hd_db.Service_Categories.ss_id == service_categories.get('ss_id')
                ).first()
    if iid:
        return session.query(hd_db.Service_Categories) \
        .filter(
            hd_db.Service_Categories.iid == iid
        ).first()
    return session.query(hd_db.Service_Categories) \
        .filter(
            hd_db.Service_Categories.id == service_categories['id'],
            hd_db.Service_Categories.ss_id == service_categories.get('ss_id')
        ).first()
def get_service_items(service_items:dict = None, all: bool = False, iid:int = None):
    if all:
        return session.query(hd_db.Service_Items) \
            .filter(
                hd_db.Service_Items.ss_id == service_items.get('ss_id')
            ).all()
    if iid:
        return session.query(hd_db.Service_Items) \
        .filter(
            hd_db.Service_Items.iid == iid
        ).first()
    return session.query(hd_db.Service_Items) \
        .filter(
            hd_db.Service_Items.id == service_items['id'],
            hd_db.Service_Items.ss_id == service_items.get('ss_id')
        ).first()

## Snapshots
def set_snapshot():
    a=hd_db.SnapShots(date=datetime.now())
    session.add(a)
    session.commit()
    return a.id  
def get_snapshots_by(id:int=None):
    if id:
        return session.query(hd_db.SnapShots) \
            .filter(hd_db.SnapShots.id==id
        ).first()
    return session.query(hd_db.SnapShots).all()
def run_retention(days:int):
    ago=date.today()-timedelta(days=days)
    # print(f"Retention period: {ago} days")
    # return 
    remove=session.query(hd_db.SnapShots) \
        .filter(hd_db.SnapShots.date <= ago).all()
    if not remove:
        return None
    for rm in remove:
        session.delete(rm)
    session.commit()
    return remove

## Solutions
def insert_solutions_articles(articles:dict = None):
    if get_solutions_articles(articles):
        return
    try:
        add = hd_db.Solutions_Articles(**articles)
        session.add(add)
        session.commit()
    except Exception as e:
        logger.error(f"Failed to add solution article: {e}")
        return False
    return add.iid
def insert_solutions_categories(categories:dict = None):
    if get_solutions_categories(categories):
        return
    try:
        add = hd_db.Solutions_Categories(**categories)
        session.add(add)
        session.commit()
    except Exception as e:
        logger.error(f"Failed to add solution category: {e}")
        return False
    return add.iid
def insert_solutions_folders(folders:dict = None):
    if get_solutions_folders(folders):
        return
    try:
        add = hd_db.Solutions_Folders(**folders)
        session.add(add)
        session.commit()
    except Exception as e:
        logger.error(f"Failed to add solution folder: {e}")
        return False
    return add.iid
def get_solutions_articles(articles:dict = None, all: bool = False, title:str = None, folder_id:int = None, iid:int = None):
    if all:
        return session.query(hd_db.Solutions_Articles) \
            .filter(
                hd_db.Solutions_Articles.ss_id == articles.get('ss_id')
            ).all()
    if folder_id:
        return session.query(hd_db.Solutions_Articles) \
        .filter(
            hd_db.Solutions_Articles.folder_id == folder_id,
            hd_db.Solutions_Articles.ss_id == articles.get('ss_id')
        ).all()
    if title:
        return session.query(hd_db.Solutions_Articles) \
            .filter(
                hd_db.Solutions_Articles.title == title,
                hd_db.Solutions_Articles.ss_id == articles.get('ss_id')
            ).first()
    if iid:
        return session.query(hd_db.Solutions_Articles) \
        .filter(
            hd_db.Solutions_Articles.iid == iid
        ).first()
    return session.query(hd_db.Solutions_Articles) \
        .filter(
            hd_db.Solutions_Articles.id == articles['id'],
            hd_db.Solutions_Articles.ss_id == articles.get('ss_id')
        ).first()
def get_solutions_categories(categories:dict = None, all: bool = False,  name:str = None, iid:int = None):
    if all:
        return session.query(hd_db.Solutions_Categories) \
            .filter(
                hd_db.Solutions_Categories.ss_id == categories.get('ss_id')
            ).all()
    if name:
        return session.query(hd_db.Solutions_Categories) \
            .filter(
                hd_db.Solutions_Categories.name == name,
                hd_db.Solutions_Categories.ss_id == categories.get('ss_id')
            ).first()
    if iid:
        return session.query(hd_db.Solutions_Categories) \
        .filter(
            hd_db.Solutions_Categories.iid == iid
        ).first()
    return session.query(hd_db.Solutions_Categories) \
        .filter(
            hd_db.Solutions_Categories.id == categories['id'],
            hd_db.Solutions_Categories.ss_id == categories.get('ss_id')
        ).first()
def get_solutions_folders(folders:dict = None, all: bool = False, name:str = None, category_id:int = None, iid:int = None):
    if all:
        return session.query(hd_db.Solutions_Folders) \
            .filter(
                hd_db.Solutions_Folders.ss_id == folders.get('ss_id')
            ).all()
    if category_id:
        return session.query(hd_db.Solutions_Folders) \
        .filter(
            hd_db.Solutions_Folders.category_id == category_id,
            hd_db.Solutions_Folders.ss_id == folders.get('ss_id')
        ).all()
    if name:
        return session.query(hd_db.Solutions_Folders) \
            .filter(
                hd_db.Solutions_Folders.name == name,
                hd_db.Solutions_Folders.ss_id == folders.get('ss_id')
            ).first()
    if iid:
        return session.query(hd_db.Solutions_Folders) \
        .filter(
            hd_db.Solutions_Folders.iid == iid
        ).first()
    return session.query(hd_db.Solutions_Folders) \
        .filter(
            hd_db.Solutions_Folders.id == folders['id'],
            hd_db.Solutions_Folders.ss_id == folders.get('ss_id')
        ).first()

