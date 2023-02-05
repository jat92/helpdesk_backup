from difflib import restore
from tabnanny import check
import re
import fnmatch
import fs_db
import json
import http_func
import db_func
import sys
import loggy
from pathlib import Path
from pprintpp import pprint as pp
from rich.prompt import Confirm

short_script_name = Path(__file__).stem
logger = loggy.logging.getLogger(short_script_name)

# confirm_action() prompts the user with the date of the snapshot and gives the option to continue or cancel restore.
def confirm_action(date_id:int, message:str):
    verify_date = db_func.get_snapshots_by(id = date_id)
    return Confirm.ask(f"Snapshot date: {verify_date.date}. {message}")

def restore_agents(row:dict = None):
    db_ag_keys = ['role_ids', 'first_name','last_name', 'email', 'job_title','department_ids','scoreboard_level_id','observer_of','reporting_manager_id']
    agent_id = db_func.get_agents({"id": row.id, "ss_id": row.ss_id})
    if not agent_id:
        logger.error("Agent id not found in backup.")
        return
    restore_dict={key:getattr(row,key) for key in db_ag_keys}
    check_agent = http_func.get_freshservice(f"agents/{row.id}", no_page=True)
    logger.debug(f"Agent: {row.id} http result is {check_agent.status_code}")
    if not check_agent.results:
        if confirm_action(row.ss_id,"Continuing will create a new agent."):
            ag_post = http_func.post_freshservice("agents", data=restore_dict)
            logger.debug(f"Agent status code: {ag_post.status_code}")
            if ag_post.status_code < 300:
                result=ag_post.json()['agent']
                logger.info(f"Added agent id {row.id}, new id is {result['id']}")
                return True
            else:
                logger.error(f"{row.iid} failed to add agent id {row.id} to Freshservice :: {ag_post.status_code}:{ag_post.content}")
                return False
        return False

    is_active = False
    if 'agent' in check_agent.results[0] and not check_agent.results[0]['agent']['active']:
         if confirm_action(row.ss_id,"Continuing will activate the agent then overwrite it."):
            ag_put = http_func.put_freshservice(f"agents/{row.id}/reactivate")
            logger.debug(f"Agent status code: {ag_put.status_code}")
            if ag_put.status_code < 300:
                is_active = True
                logger.info(f"Reactivated agent: {row.id}")
            else:
                logger.error(f"{row.iid} failed to reactivate agent: {row.id} :: {ag_put.status_code}:{ag_put.content}")
                return False

    if 'agent' in check_agent.results[0] and (is_active or check_agent.results[0]['agent']['active']):
        if confirm_action(row.ss_id,"Continuing will overwrite the agent."):
            ag_put = http_func.put_freshservice(f"agents/{row.id}", data=restore_dict)
            logger.debug(f"Agent status code: {ag_put.status_code}")
            if ag_put.status_code < 300:
                logger.info(f"Updated agent id {row.id}")
                return True
            else:
                logger.error(f"{row.iid} failed to update agent id {row.id} :: {ag_put.status_code}:{ag_put.content}")
                return False
        return False

def restore_agent_groups(row:dict = None):
    db_agg_keys = ['name','description', 'members','agent_ids']
    agent_group_id = db_func.get_agent_groups({"id": row.id, "ss_id": row.ss_id})
    if not agent_group_id:
        logger.error("Agent group id not found in backup.")
        return
    restore_dict={key:getattr(row,key) for key in db_agg_keys}
    check_agent_group = http_func.get_freshservice(f"groups/{row.id}", no_page=True)
    logger.debug(f"Agent Groups: {row.id} http result is {check_agent_group.status_code} :: {check_agent_group.results}")
    
    if not check_agent_group.results:
        if confirm_action(row.ss_id,"Continuing will create a new agent group."):
            agg_post = http_func.post_freshservice("groups", data=restore_dict)
            logger.debug(f"Agent group status code: {agg_post.status_code}")
            if agg_post.status_code < 300:
                result=agg_post.json()['group']
                logger.info(f"Added agent group id {row.id}, new id is {result['id']}")
                return True
            else:
                logger.error(f"{row.iid} failed to add agent group id {row.id} to Freshservice :: {agg_post.status_code}:{agg_post.content}")
                return False
        return False

    if 'group' in check_agent_group.results[0]:
         if confirm_action(row.ss_id,"Continuing will overwrite the agent group."):
            agg_put = http_func.put_freshservice(f"groups/{row.id}", data=restore_dict)
            logger.debug(f"Agent group status code: {agg_put.status_code}")
            if agg_put < 300:
                result=agg_put.json()
                logger.info(f"Updated agent group id {row.id}")
                return True
            else:
                logger.error(f"{row.iid} failed to update agent group id {row.id} to Freshservice :: {agg_put.status_code}:{agg_put.content}")
                return False

def restore_assets(row:dict = None):
    db_se_keys = ['name','description', 'asset_type_id','asset_tag','impact','usage_type','user_id','assigned_on','group_id','agent_id','department_id','location_id']
    display_id = row.display_id
    if not display_id:
        logger.error("Asset id not found in backup.")
        return
    restore_dict={key:getattr(row,key) for key in db_se_keys}
    check_asset = http_func.get_freshservice(f"assets/{display_id}", no_page=True)
    logger.debug(f"Asset: {display_id} http result is {check_asset.status_code}")
    if not check_asset.results:
        as_put = http_func.put_freshservice(f"assets/{display_id}/restore")
        if as_put.status_code == 204:
            logger.info(f"Restored asset: {row.id}")
        else:
            logger.error(f"{row.iid} failed to restore asset: {row.id} :: {as_put.status_code}:{as_put.content}")
            if confirm_action(row.ss_id,"Continuing will create a new asset."):
                as_post = http_func.post_freshservice("assets", data=restore_dict)
                if as_post.status_code < 300:
                    result=as_post.json()['asset']
                    logger.info(f"Added asset id {display_id}, new id is {result['id']}")
                    return True
                else:
                    logger.error(f"{row.iid} failed to add asset id {display_id} to Freshservice :: {as_post.status_code}:{as_post.content}")
                    return False
        return False

    if 'asset' in check_asset.results[0]:
        if confirm_action(row.ss_id,"Continuing will overwrite the asset."):
            as_put = http_func.put_freshservice(f"assets/{display_id}", data=restore_dict)
            if as_put.status_code < 300:
                logger.info(f"Updated asset id {display_id}")
                return True
            else:
                logger.error(f"{row.iid} failed to update asset id {display_id} :: {as_put.status_code}:{as_put.content}")
                return False
        return False

def restore_custom_object_records(row:dict = None):
    restore_dict = {}
    regex_matches = re.compile("^bo_+").match
    cor_data = row.data
    restore_dict['data']= {k:v for k,v in cor_data.items()
        if not regex_matches(k)}
    record_id = row.bo_display_id
    object_id = row.custom_object_id
    if not record_id and not object_id:
        logger.error("Record not found in backup.")
        return
    check_record = http_func.get_freshservice(f"objects/{object_id}/records", params={'bo_display_id': row.bo_display_id}, no_page=True) 
    logger.debug(f"Record: {row.custom_object_id}|{row.bo_display_id} http result is {check_record.status_code}")
    if not check_record.results:
        if confirm_action(row.ss_id,"Continuing will create a new record."):
            rec_post = http_func.post_freshservice(f"objects/{object_id}/records", data=restore_dict)
            logger.debug(f"Custom object record status code: {rec_post.status_code}")
            if rec_post.status_code < 300:
                result=rec_post.json()['records']
                logger.info(f"Added record id {row.bo_display_id} for custom object {row.custom_object_id}, new id is {result['data']['id']}")
                return True
            else:
                logger.error(f"{row.iid} failed to add record id {row.bo_display_id} for custom object {row.custom_object_id} to Freshservice :: {rec_post.status_code}:{rec_post.content}")
                return False
        return False

    if 'records' in check_record.results[0]:
        if confirm_action(row.ss_id,"Continuing will overwrite the record."):
            rec_put = http_func.put_freshservice(f"objects/{object_id}/records/{record_id}", data=restore_dict)
            logger.debug(f"Custom object record status code: {rec_put.status_code}")
            if rec_put.status_code < 300:
                logger.info(f"Updated record id {row.bo_display_id} for custom object {row.custom_object_id}")
                return True
            else:
                logger.error(f"{row.iid} failed to update record id {row.bo_display_id} for custom object {row.custom_object_id} :: {rec_put.status_code}:{rec_put.content}")
                return False
        return False

def restore_departments(row:dict = None):
    db_dep_keys = ['name','custom_fields', 'prime_user_id', 'head_user_id','domains']
    departments_id = row.id
    if not departments_id:
        logger.error("Department id not found in backup.")
        return
    restore_dict={key:getattr(row,key) for key in db_dep_keys}
    check_department = http_func.get_freshservice(f"departments/{departments_id}", no_page=True)
    logger.debug(f"Department: {departments_id} http result is {check_department.status_code} :: {check_department.results}")
    print(check_department.results)
    if not check_department.results:
        if confirm_action(row.ss_id,"Continuing will create a new department."):
            dep_post = http_func.post_freshservice("departments", data=restore_dict)
            logger.debug(f"department status code: {dep_post.status_code}")
            if dep_post.status_code < 300:
                result=dep_post.json()['department']
                logger.info(f"Added department id {departments_id}, new id is {result['id']}")
                return True
            else:
                logger.error(f"{row.iid} failed to add department id {departments_id} to Freshservice :: {dep_post.status_code}:{dep_post.content}")
                return False
        return False

    if 'department' in check_department.results[0]:
        if confirm_action(row.ss_id,"Continuing will overwrite the department."):
            dep_put = http_func.put_freshservice(f"departments/{row.id}", data=restore_dict)
            logger.debug(f"Department status code: {dep_put.status_code}")
            if dep_put.status_code < 300:
                logger.info(f"Updated department id {departments_id}")
                return True
            else:
                logger.error(f"{row.iid} failed to update department id {departments_id} :: {dep_put.status_code}:{dep_put.content}")
                return False
        return False

def restore_requesters(row:dict = None):
    db_re_keys = ['first_name','last_name', 'primary_email', 'job_title','department_ids','reporting_manager_id']
    requester_id = db_func.get_requesters({"id": row.id, "ss_id": row.ss_id})
    if not requester_id:
        logger.error("Requester id not found in backup.")
        return
    restore_dict={key:getattr(row,key) for key in db_re_keys}
    check_requester = http_func.get_freshservice(f"requesters/{row.id}", no_page=True)
    logger.debug(f"Requester: {row.id} http result is {check_requester.status_code}")
    
    if not check_requester.results:
        if confirm_action(row.ss_id,"Continuing will create a new requester."):
            re_post = http_func.post_freshservice("requesters", data=restore_dict)
            logger.debug(f"Requester status code: {re_post.status_code}")
            if re_post.status_code < 300:
                result=re_post.json()['requester']
                logger.info(f"Added requester id {row.id}, new id is {result['id']}")
                return True
            else:
                logger.error(f"{row.iid} failed to add requester id {row.id} to Freshservice :: {re_post.status_code}:{re_post.content}")
                return False
        return False
    
    is_active = False
    if 'requester' in check_requester.results[0] and not check_requester.results[0]['requester']['active']:
        if confirm_action(row.ss_id,"Continuing will activate the requester then overwrite it."):
            re_put = http_func.put_freshservice(f"requesters/{row.id}/reactivate")
            logger.debug(f"Requester status code: {re_put.status_code}")
            if re_put.status_code < 300:
                is_active = True
                logger.info(f"Reactivated requester: {row.id}")
            else:
                logger.error(f"{row.iid} failed to reactivate requester: {row.id} :: {re_put.status_code}:{re_put.content}")
                return False
 
    if 'requester' in check_requester.results[0] and (is_active or check_requester.results[0]['requester']['active']):
        if confirm_action(row.ss_id,"Continuing will overwrite the requester."):
            re_put = http_func.put_freshservice(f"requesters/{row.id}", data=restore_dict)
            logger.debug(f"Requester status code: {re_put.status_code}")
            if re_put.status_code < 300:
                logger.info(f"Updated requester id {row.id}")
                return True
            else:
                logger.error(f"{row.iid} failed to update requester id {row.id} :: {re_put.status_code}:{re_put.content}")
                return False
        return False

def restore_requester_groups(row:dict = None):
    db_reg_keys = ['name', 'description', 'type']
    requester_group_id = db_func.get_requester_groups({"id": row.id, "ss_id": row.ss_id})
    if not requester_group_id:
        logger.error("Requester group id not found in backup.")
        return
    restore_dict={key:getattr(row,key) for key in db_reg_keys}
    check_requester_group = http_func.get_freshservice(f"requester_groups/{row.id}", no_page=True)
    logger.debug(f"Requester group: {row.id} http result is {check_requester_group.status_code}")
    
    if not check_requester_group.results:
        if confirm_action(row.ss_id,"Continuing will create a new requester."):
            reg_post = http_func.post_freshservice("requester_groups", data=restore_dict)
            logger.debug(f"Requester group status code: {reg_post.status_code}")
            if reg_post.status_code < 300:
                result=reg_post.json()['requester_group']
                logger.info(f"Added requester group id {row.id}, new id is {result['id']}")
                return True
            else:
                logger.error(f"{row.iid} failed to add requester group id {row.id} to Freshservice :: {reg_post.status_code}:{reg_post.content}")
                return False
        return False

    if 'requester_group' in check_requester_group.results[0]:
        if confirm_action(row.ss_id,"Continuing will overwrite the requester group."):
            reg_put = http_func.put_freshservice(f"requester_groups/{row.id}", data=restore_dict)
            logger.debug(f"Requester group status code: {reg_put.status_code}")
            if reg_put.status_code < 300:
                logger.info(f"Updated requester id {row.id}")
                return True
            else:
                logger.error(f"{row.iid} failed to update requester group id {row.id} :: {reg_put.status_code}:{reg_put.content}")
                return False
        return False

def restore_solutions_articles(row:dict = None):
    db_sa_keys = ['title', 'description', 'article_type', 'folder_id', 'status', 'keywords']
    
    category_id = db_func.get_solutions_categories({"id": row.category_id, "ss_id": row.ss_id})
    if not category_id:
        logger.error("Category id not found in backup.")
        return
    check_category = http_func.get_freshservice(f"solutions/categories/{row.category_id}", no_page=True)
    logger.debug(f"Category: {row.category_id} http result is {check_category.status_code}")
    if check_category.status_code != 200:
        print("Category id not found in Freshservice, verify that category exists.")
        return False
    
    folder_id = db_func.get_solutions_folders({"id": row.folder_id, "ss_id": row.ss_id})
    if not folder_id:
        logger.error("Folder_id not found in backup.")
        return
    check_folder = http_func.get_freshservice(f"solutions/folders/{row.folder_id}", no_page=True)
    logger.debug(f"Folder: {row.folder_id} http result is {check_folder.status_code} :: {check_folder.results}")
    if check_folder.status_code != 200:
        print("Folder id not found in Freshservice, verify that folder exists.")
        return False

    restore_dict={key:getattr(row,key) for key in db_sa_keys}
    check_article = http_func.get_freshservice(f"solutions/articles/{row.id}", no_page=True)
    logger.debug(f"Article: {row.id} http result is {check_article.status_code}")

    if not check_article.results:
        if confirm_action(row.ss_id, "Continuing will create a new article."):
            sa_post = http_func.post_freshservice("solutions/articles", data=restore_dict)
            logger.debug(f"Solutions article status code: {sa_post.status_code}")
            if sa_post.status_code < 300:
                result=sa_post.json()['article']
                logger.info(f"Added article id {row.id}, new id is {result['id']}")
                return True
            else:
                logger.error(f"{row.iid} failed to add article id {row.id} to Freshservice :: {sa_post.status_code}:{sa_post.content}")
                return False
        return False
            
    if 'article' in check_article.results[0]:
        if confirm_action(row.ss_id,"Continuing will overwrite the article."):
                sa_put=http_func.put_freshservice(f"solutions/articles/{row.id}", data=restore_dict)
                logger.debug(f"Solutions article status code: {sa_put.status_code}")
                if sa_put.status_code < 300:
                    result=sa_put.json()
                    logger.info(f"Updated article id {row.id}")
                    return True
                else:
                    logger.error(f"{row.iid} failed to update article id {row.id} :: {sa_put.status_code}:{sa_put.content}")
                    return False
        return False
        
def restore_solutions_folders(row:dict = None):
    db_sf_keys = ['name', 'description', 'category_id', 'visibility','manage_by_group_ids']
    category_id = row.category_id
    if not category_id:
        logger.error("Category id not found in backup.")
        return
    check_category = http_func.get_freshservice(f"solutions/categories/{category_id}", no_page=True)
    logger.debug(f"Category: {category_id} http result is {check_category.status_code}")
    if check_category.status_code != 200:
        print("Category id not found in Freshservice, verify that folder exists.")
        return False
    folder_id = row.id
    if not folder_id:
        logger.error("Folder id not found in backup.")
        return
    restore_dict={key:getattr(row,key) for key in db_sf_keys}
    check_folder = http_func.get_freshservice(f"solutions/folders/{folder_id}", no_page=True)

    if not check_folder.results:
        if confirm_action(row.ss_id,"Continuing will create a new folder."):
            sf_post = http_func.post_freshservice("solutions/folders", data=restore_dict)
            logger.debug(f"Solutions folder status code: {sf_post.status_code}")
            if sf_post.status_code < 300:
                result=sf_post.json()['folder']
                logger.info(f"Added folder id {folder_id}, new id is {result['id']}")
                return True
            else:
                logger.error(f"{row.iid} failed to add folder id {folder_id} to Freshservice :: {sf_post.status_code}:{sf_post.content}")
                return False
        return False

    if 'folder' in check_folder.results[0]:
        if confirm_action(row.ss_id,"Continuing will overwrite the folder."):
            sf_put = http_func.put_freshservice(f"solutions/folders/{folder_id}", data=restore_dict)
            logger.debug(f"Solutions folder status code: {sf_put.status_code}")
            if sf_put.status_code < 300:
                logger.info(f"Updated folder id {folder_id}")
                return True
            else:
                logger.error(f"{row.iid} failed to update folder id {folder_id} :: {sf_put.status_code}:{sf_put.content}")
                return False
        return False
    logger.critical(f"Unable to figure out how to resotore solutions folder")
    return False

def restore_solutions_categories(row:dict = None):
    db_sc_keys = ['name', 'description']
    category_id = row.id
    if not category_id:
        logger.error("Category_id not found in backup.")
        return
    restore_dict={key:getattr(row,key) for key in db_sc_keys}
    check_category = http_func.get_freshservice(f"solutions/categories/{category_id}", no_page=True)
    logger.debug(f"Category: {category_id} http result is {check_category.status_code}")
    if not check_category.results:
        if confirm_action(row.ss_id,"Continuing will create a new category."):
            sc_post = http_func.post_freshservice("solutions/categories", data=restore_dict)
            logger.debug(f"Solutions category status code: {sc_post.status_code}")
            if sc_post.status_code < 300:
                result=sc_post.json()['category']
                logger.info(f"Added category id {category_id}, new id is {result['id']}")
                return True
            else:
                logger.error(f"{row.iid} failed to add category id {category_id} to Freshservice :: {sc_post.status_code}:{sc_post.content}")
                return False
        return False

    if 'category' in check_category.results[0]:
        if confirm_action(row.ss_id,"Continuing will overwrite the folder."):
            sc_put = http_func.put_freshservice(f"solutions/categories/{category_id}", data=restore_dict)
            logger.debug(f"Solutions category status code: {sc_put.status_code}")
            if sc_put.status_code < 300:
                logger.info(f"Updated category id {category_id}")
                return True
            else:
                logger.error(f"{row.iid} failed to update category id {category_id} :: {sc_put.status_code}:{sc_put.content}")
                return False
        return False
       
def restore_tickets(row:dict = None):
    db_t_keys = ['requester_id','subject','type','source','description','responder_id','custom_fields','status','priority','category','sub_category','due_by']
    ticket_id = row.id
    if not ticket_id:
        logger.error("Ticket id not found in backup.")
        return
    restore_dict={key:getattr(row,key) for key in db_t_keys}
    check_ticket = http_func.get_freshservice(f"tickets/{ticket_id}", no_page=True)
    logger.debug(f"Ticket: {ticket_id} http result is {check_ticket.status_code} :: {check_ticket.results}")
    if check_ticket.status_code > 399:
        logger.error(f"API Failure: {check_ticket.status_code}:{check_ticket.results}")
        return

    if not check_ticket.results:
        t_put = http_func.put_freshservice(f"tickets/{ticket_id}/restore")
        if t_put.status_code == 204:
            logger.info(f"Restored asset: {row.id}")
        else:
            if confirm_action(row.ss_id,"Continuing will create a new ticket."):
                t_post = http_func.post_freshservice("tickets", data=restore_dict)
                logger.debug(f"Ticket status code: {t_post.status_code}")
                if t_post.status_code == 201:
                    result=t_post.json()['ticket']
                    logger.info(f"Added ticket id {ticket_id}, new id is {result['id']}")
                    return True
                else:
                    logger.error(f"{row.iid} failed to add ticket id {ticket_id} to Freshservice :: {t_post.status_code}:{t_post.content}")
                    return False
        return False

    if 'ticket' in check_ticket.results[0]:
        if confirm_action(row.ss_id,"Continuing will overwrite the ticket."):
            t_put = http_func.put_freshservice(f"tickets/{ticket_id}", data=restore_dict)
            logger.debug(f"Ticket status code: {t_put.status_code}")
            if t_put.status_code < 300:
                logger.info(f"Updated ticket id {ticket_id}")
                return True
            else:
                logger.error(f"{row.iid} failed to update ticket id {ticket_id} :: {t_put.status_code}:{t_put.content}")
                return False
        return False

def restore_vendors(row:dict = None):
    db_v_keys = ['name','id','description','primary_contact_id','address']
    vendor_id = row.id
    if not vendor_id:
        logger.error("Vendor id not found in backup.")
        return
    restore_dict={key:getattr(row,key) for key in db_v_keys}
    check_vendor = http_func.get_freshservice(f"vendors/{vendor_id}", no_page=True)
    logger.debug(f"Vendor: {vendor_id} http result is {check_vendor.status_code}: {check_vendor.results}")

    if not check_vendor.results:
        if confirm_action(row.ss_id,"Continuing will create a new vendor."):
            v_post = http_func.post_freshservice("vendors", data=restore_dict)
            logger.debug(f"Vendor status code: {v_post.status_code}")
            if v_post.status_code < 300:
                result=v_post.json()['vendor']
                logger.info(f"Added vendor id {vendor_id}, new id is {result['id']}")
                return True
            else:
                logger.error(f"{row.iid} failed to add vendor id {vendor_id} to Freshservice :: {v_post.status_code}:{v_post.content}")
                return False
        return False

    if 'vendor' in check_vendor.results[0]:
        if confirm_action(row.ss_id,"Continuing will overwrite the vendor."):
            v_put = http_func.put_freshservice(f"vendors/{vendor_id}", data=restore_dict)
            logger.debug(f"Vendor status code: {v_put.status_code}")
            if v_put.status_code < 300:
                result=v_put.json()
                logger.info(f"Updated vendor id {vendor_id}")
                return True
            else:
                logger.error(f"{row.iid} failed to update vendor id {vendor_id} :: {v_put.status_code}:{v_put.content}")
                return False
        return False
