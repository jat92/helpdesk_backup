from auth import db_connection_str
from sqlalchemy import Column
# from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import BigInteger
from sqlalchemy.orm import declarative_base
# from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists

if "sqlite" in db_connection_str:
    from sqlalchemy.dialects.sqlite import JSON
elif "postgres" in db_connection_str:
    from sqlalchemy.dialects.postgresql import JSON

Base = declarative_base()

def connect_db():
    if not database_exists(db_connection_str):
        create_database(db_connection_str)
    db = create_engine(
        db_connection_str,
        echo=False,
        future = True,
    )
    return db

class SnapShots(Base):
    __tablename__ = 'snapshots'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=func.now, index=True)

class Agents(Base):
    __tablename__ = "agents"
    iid = Column(Integer, primary_key=True)
    id = Column(BigInteger, nullable=False, index=True)
    ss_id = Column(Integer, ForeignKey('snapshots.id', ondelete='CASCADE'), nullable=False, index=True)
    active = Column(Boolean)
    address = Column(String)
    auto_assign_status_changed_at = Column(String)
    auto_assign_tickets = Column(Boolean)
    background_information = Column(String)
    can_see_all_tickets_from_associated_departments = Column(Boolean)
    created_at = Column(String)
    custom_fields = Column(JSON)
    department_ids = Column(JSON)
    department_names = Column(JSON)
    email = Column(String)
    external_id = Column(String, nullable=True)
    first_name = Column(String)
    group_ids = Column(JSON)
    has_logged_in = Column(Boolean)
    job_title = Column(String)
    language = Column(String)
    last_active_at = Column(String)
    last_login_at = Column(String)
    last_name = Column(String)
    location_name = Column(JSON)
    location_id = Column(BigInteger, nullable=True)
    member_of = Column(JSON)
    member_of_pending_approval = Column(JSON)
    mobile_phone_number = Column(String)
    observer_of = Column(JSON)
    observer_of_pending_approval = Column(JSON)
    occasional = Column(Boolean)
    reporting_manager_id = Column(BigInteger)
    role_ids = Column(JSON)
    roles = Column(JSON)
    scopes = Column(JSON)
    scoreboard_level_id = Column(BigInteger, nullable=True)
    scoreboard_points = Column(Integer, nullable=True)
    signature = Column(String)
    time_format = Column(String)
    time_zone = Column(String)
    updated_at = Column(String)
    vip_user = Column(String)
    work_phone_number = Column(String, nullable=True)

class Agent_Groups(Base):
    __tablename__ = "groups"
    iid = Column(Integer, primary_key=True)
    id = Column(BigInteger, nullable=False, index=True)
    ss_id = Column(Integer, ForeignKey('snapshots.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String)
    description = Column(String)
    business_hours_id = Column(String)
    escalate_to = Column(String)
    unassigned_for = Column(String)
    agent_ids = Column(JSON)
    created_at = Column(JSON)
    updated_at = Column(JSON)
    auto_ticket_assign = Column(Boolean)
    approval_required = Column(Boolean)
    leaders = Column(JSON)
    leaders_pending_approval = Column(JSON)
    members = Column(JSON)
    members_pending_approval = Column(JSON)
    observers = Column(JSON)
    observers_pending_approval = Column(JSON)
    ocs_schedule_id = Column(JSON)
    restricted = Column(Boolean)

class Assets(Base):
    __tablename__ = "assets"
    iid = Column(Integer, primary_key=True)
    id = Column(BigInteger, nullable=False, index=True)
    ss_id = Column(Integer, ForeignKey('snapshots.id', ondelete='CASCADE'), nullable=False, index=True)
    display_id = Column(BigInteger)
    name = Column(String)
    description = Column(String)
    asset_type_id = Column(BigInteger)
    impact = Column(String)
    group_id = Column(BigInteger)
    author_type = Column(String)
    usage_type = Column(String)
    asset_tag = Column(String)
    user_id = Column(BigInteger)
    location_id = Column(BigInteger)
    department_id = Column(BigInteger)
    agent_id = Column(BigInteger)
    assigned_on = Column(JSON)
    created_at = Column(JSON)
    updated_at = Column(JSON)
    end_of_life = Column(String)

class Custom_Objects(Base):
    __tablename__ = "custom_objects"
    iid = Column(Integer, primary_key=True)
    id = Column(BigInteger, index=True)
    ss_id = Column(Integer, ForeignKey('snapshots.id', ondelete='CASCADE'), nullable=False, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String)
    updated_at = Column(JSON)
    last_updated_by = Column(JSON)
    meta = Column(JSON)

class Custom_Object_Records(Base):
    __tablename__ = "records"
    iid = Column(Integer, primary_key=True)
    custom_object_id = Column(BigInteger,nullable=False, index=True)
    ss_id = Column(Integer, ForeignKey('snapshots.id', ondelete='CASCADE'), nullable=False, index=True)
    data = Column(JSON)
    record_item = Column(JSON)
    bo_display_id = Column(BigInteger)
    
class Departments(Base):
    __tablename__ = "departments"
    iid = Column(Integer, primary_key=True)
    id = Column(BigInteger, nullable=False, index=True)
    ss_id = Column(Integer, ForeignKey('snapshots.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String)
    description = Column(String)
    head_user_id = Column(JSON)
    prime_user_id = Column(BigInteger)
    domains = Column(JSON)
    custom_fields = Column(JSON)
    created_at = Column(JSON)
    updated_at = Column(JSON)

class Locations(Base):
    __tablename__ = "locations"
    iid = Column(Integer, primary_key=True)
    id = Column(BigInteger, nullable=False, index=True)
    ss_id = Column(Integer, ForeignKey('snapshots.id', ondelete='CASCADE'), nullable=False, index=True)
    address = Column(JSON)
    contact_name = Column(String)
    created_at = Column(JSON)
    email = Column(String)
    name = Column(String)
    parent_location_id = Column(BigInteger)
    phone = Column(String)
    primary_contact_id = Column(BigInteger)
    updated_at = Column(JSON)

class Requesters(Base):
    __tablename__ = "requesters"
    iid = Column(Integer, primary_key=True)
    id = Column(BigInteger, nullable=False, index=True)
    ss_id = Column(Integer, ForeignKey('snapshots.id', ondelete='CASCADE'), nullable=False, index=True)
    is_agent = Column(Boolean)
    first_name = Column(String)
    last_name = Column(String)
    job_title = Column(String)
    primary_email = Column(String)
    secondary_emails = Column(JSON)
    work_phone_number = Column(String)
    mobile_phone_number = Column(String)
    department_ids = Column(JSON)
    department_names = Column(JSON)
    can_see_all_tickets_from_associated_departments = Column(Boolean)
    can_see_all_changes_from_associated_departments = Column(Boolean)
    reporting_manager_id = Column(BigInteger)
    address = Column(String)
    time_zone = Column(JSON)
    time_format = Column(JSON)
    language = Column(String)
    location_id = Column(BigInteger)
    location_name = Column(JSON)
    background_information = Column(String)
    custom_fields = Column(JSON)
    active = Column(Boolean)
    has_logged_in = Column(Boolean)
    created_at = Column(JSON)
    updated_at = Column(JSON)
    external_id = Column(JSON)
    vip_user = Column(JSON)

class Requester_Groups(Base):
    __tablename__ = "requester_groups"
    iid = Column(Integer, primary_key=True)
    id = Column(BigInteger, nullable=False, index=True)
    ss_id = Column(Integer, ForeignKey('snapshots.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String)
    description = Column(String)
    type = Column(String)

class Service_Categories(Base):
    __tablename__ = "service_categories"
    iid = Column(Integer, primary_key=True)
    id = Column(BigInteger, nullable=False, index=True)
    ss_id = Column(Integer, ForeignKey('snapshots.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = Column(JSON)
    description = Column(String)
    name = Column(String)
    position = Column(Integer)
    updated_at = Column(JSON)

class Service_Items(Base):
    __tablename__ = "service_items"
    iid = Column(Integer, primary_key=True)
    id = Column(BigInteger, nullable=False, index=True)
    ss_id = Column(Integer, ForeignKey('snapshots.id', ondelete='CASCADE'), nullable=False, index=True)
    agent_group_visibility = Column(Integer)
    allow_attachments = Column(Boolean)
    allow_quantity = Column(Boolean)
    botified = Column(Boolean)
    category_id = Column(BigInteger)
    ci_type_id = Column(BigInteger)
    configs = Column(JSON)
    cost_visibility = Column(Boolean)
    create_child = Column(Boolean)
    created_at = Column(JSON)
    deleted = Column(Boolean)
    delivery_time = Column(String)
    delivery_time_visibility = Column(Boolean)
    display_id = Column(BigInteger)
    group_visibility = Column(Integer)
    icon_name = Column(String)
    is_bundle = Column(Boolean)
    item_type = Column(Integer)
    name = Column(String)
    product_id = Column(BigInteger)
    quantity = Column(Integer)
    updated_at = Column(JSON)
    visibility = Column(Integer)

class Solutions_Articles(Base):
    __tablename__ = "articles"
    iid = Column(Integer, primary_key=True)
    id = Column(BigInteger, nullable=False, index=True)
    ss_id = Column(Integer, ForeignKey('snapshots.id', ondelete='CASCADE'), nullable=False, index=True)
    description = Column(String)
    created_at = Column(JSON)
    updated_at = Column(JSON)
    title = Column(String, nullable=False, index=True)
    status = Column(Integer)
    approval_status = Column(String)
    position = Column(Integer)
    folder_department_ids = Column(JSON)
    folder_visibility = Column(Integer)
    group_folder_department_ids = Column(JSON)
    group_folder_group_ids = Column(JSON)
    group_folder_requester_group_ids = Column(JSON)
    inserted_into_tickets = Column(Integer)
    folder_id = Column(BigInteger)
    category_id = Column(BigInteger)
    thumbs_up = Column(Integer)
    thumbs_down = Column(Integer)
    modified_by = Column(BigInteger)
    modified_at = Column(JSON)
    url = Column(String)
    article_type = Column(Integer)
    user_id = Column(BigInteger)
    views = Column(Integer)
    description_text = Column(String)
    keywords = Column(JSON)
    review_date = Column(String)
    attachments = Column(JSON)
    approvals = Column(String)

class Solutions_Categories(Base):
    __tablename__ = "categories"
    iid = Column(Integer, primary_key=True)
    id = Column(BigInteger, nullable=False, index=True)
    ss_id = Column(Integer, ForeignKey('snapshots.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = Column(String)
    updated_at = Column(String)
    name = Column(String,nullable=False, index=True)
    description = Column(String)
    default_category = Column(Boolean)
    position = Column(Integer)
    translations = Column(JSON)

class Solutions_Folders(Base):
    __tablename__ = "folders"
    iid = Column(Integer, primary_key=True)
    id = Column(BigInteger, nullable=False, index=True)
    ss_id = Column(Integer, ForeignKey('snapshots.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String,nullable=False, index=True)
    group_ids = Column(JSON)
    description = Column(String)
    created_at = Column(JSON)
    updated_at = Column(JSON)
    category_id = Column(BigInteger)
    position = Column(Integer)
    visibility = Column(Integer)
    approval_settings = Column(String)
    default_folder = Column(Boolean)
    manage_by_group_ids = Column(JSON)

class Tickets(Base):
    __tablename__ = "tickets"
    iid = Column(Integer, primary_key=True)
    id = Column(BigInteger, nullable=False, index=True)
    ss_id = Column(Integer, ForeignKey('snapshots.id', ondelete='CASCADE'), nullable=False, index=True)
    cc_emails = Column(JSON)
    fwd_emails = Column(JSON)
    reply_cc_emails = Column(JSON)
    fr_escalated = Column(Boolean)
    spam = Column(Boolean)
    email_config_id = Column(JSON)
    group_id = Column(BigInteger)
    priority = Column(Integer)
    requester_id = Column(BigInteger)
    requested_for_id = Column(BigInteger)
    responder_id = Column(BigInteger)
    source = Column(Integer) 
    status = Column(Integer)
    subject = Column(String, index=True)
    to_emails = Column(JSON)
    department_id = Column(BigInteger)
    type = Column(String)
    due_by = Column(String)
    fr_due_by = Column(JSON)
    is_escalated = Column(Boolean)
    description = Column(String)
    description_text = Column(String)
    category = Column(String)
    sub_category = Column(String)
    item_category = Column(String)
    custom_fields = Column(JSON)
    created_at = Column(JSON)
    updated_at = Column(JSON)
    deleted = Column(Boolean)

class Vendors(Base):
    __tablename__ = "vendors"
    iid = Column(Integer, primary_key=True)
    id = Column(BigInteger, nullable=False, index=True)
    ss_id = Column(Integer, ForeignKey('snapshots.id', ondelete='CASCADE'), nullable=False, index=True)
    contact_name = Column(String)
    custom_fields = Column(JSON)
    email = Column(String)
    mobile = Column(String)
    phone = Column(String)
    name = Column(String, index=True)
    description = Column(String)
    primary_contact_id = Column(BigInteger)
    address = Column(JSON)
    created_at = Column(String)
    updated_at = Column(String)

engine = connect_db()
Base.metadata.create_all(engine)