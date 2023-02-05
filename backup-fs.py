#!/usr/bin/env python3
# import os
import sys
# from base64 import b64encode
import fs_db
from sqlalchemy.orm import sessionmaker
import http_func
import db_func
import loggy
from pathlib import Path
from pprintpp import pprint as pp
from inspect import stack

script_name = Path(__file__).stem
logger = loggy.logging.getLogger(script_name)

fake_err_num = 100000000
db=fs_db.connect_db()
Session = sessionmaker(bind=db)
session = Session()

snapshot_id=db_func.set_snapshot()
if not snapshot_id:
    logger.critical("No snapshot_id was created")
    sys.exit(1)

def make_err_str(response):
    err="Unknown"
    if response.results:
        err=response.results
    return f"http_code: {response.status_code}, http_error: {err}, Failed: {fake_err_num}"

## Agents
def process_agents():
    logger.info(f"Starting {stack()[0][3]}")
    try:
        agent_results = http_func.get_freshservice('agents')
    except:
        logger.critical("get_freshservice('agents') Failed")
    if agent_results.status_code > 299:
        logger.error(make_err_str(agent_results))
        return
    agent_added=0
    agent_failed=0
    for agent in agent_results.results:
        for results in agent['agents']:
            results['ss_id']= snapshot_id
            if db_func.insert_agents(results):
                agent_added+=1
            else:
                agent_failed+=1
    logger.info(f"Agents, Added: {agent_added}, Failed: {agent_failed}")
    
    agent_groups_results = http_func.get_freshservice('groups')
    if agent_groups_results.status_code > 299:
        logger.error(make_err_str(agent_groups_results))
        return
    groups_added=0
    groups_failed=0
    for group in agent_groups_results.results:
        for results in group['groups']:
            results['ss_id'] = snapshot_id
            if db_func.insert_agent_groups(results):
                groups_added+=1
            else:
                groups_failed+=1
    logger.info(f"Agent Groups, Added: {groups_added}, Failed: {groups_failed}")
    return True

## Assests
def process_assets():
    logger.info(f"Starting {stack()[0][3]}")
    assets_results = http_func.get_freshservice('assets')
    if assets_results.status_code > 299:
        logger.error(make_err_str(assets_results))
        return
    asset_added = 0
    asset_failed = 0
    for asset in assets_results.results:
        for results in asset['assets']:
            results['ss_id'] = snapshot_id
            if db_func.insert_assets(results):
                asset_added+=1
            else:
                asset_failed+=1
    logger.info(f"Assests, Added: {asset_added}, Failed: {asset_failed}")
    return True

## Custom_Objects
def process_custom_objects():
    logger.info(f"Starting {stack()[0][3]}")
    def get_custom_object_records_id(custom_object_list):
        cor_results = []
        for record_id in custom_object_list:
            custom_object_records_results = http_func.get_freshservice(f'objects/{record_id}/records', no_page=True)
            if custom_object_records_results.status_code > 299:
                logger.error(make_err_str(custom_object_records_results))
                continue
            
            # The cor[] below is creating the rows for the objects we specify. 
            # We don't need to do this for "data" because it already exists
            #and will be created further in the program.
            for results in custom_object_records_results.results:
                for cor in results['records']:
                    cor["custom_object_id"] = record_id
                    cor["ss_id"] = snapshot_id
                    cor["bo_display_id"] = cor["data"]["bo_display_id"]
                    cor_results.append(cor)
        return cor_results

    custom_objects_results = http_func.get_freshservice('objects')
    if custom_objects_results.status_code > 299:
        logger.error(make_err_str(custom_objects_results))
        return
    custom_objects_list = []
    co_added = 0
    co_failed = 0
    for objects in custom_objects_results.results:
        for results in objects['custom_objects']:
            results['ss_id'] = snapshot_id
            if db_func.insert_custom_objects(results):
                co_added += 1
            else:
                co_failed += 1
            custom_objects_list.extend([results[key] for key in results if key == "id"])
    logger.info(f"Custom_Objects, Added: {co_added}, Failed: {co_failed}")
    
    insert_results = get_custom_object_records_id(custom_objects_list)
    
    cor_added = 0
    cor_failed = 0
    for record in insert_results:
        # record['ss_id'] = snapshot_id
        # record['data']['id'] =record['data']['workplace_agent_group']['id']
        if db_func.insert_custom_object_records(record):
            cor_added += 1
        else:
            cor_failed += 1
    logger.info(f"Custom_Objects Reocrds, Added: {cor_added}, Failed: {cor_failed}")
    return True

##Departments
def process_departments():
    logger.info(f"Starting {stack()[0][3]}")
    departments_results = http_func.get_freshservice('departments')
    if departments_results.status_code > 299:
        logger.error(make_err_str(departments_results))
        return
    departments_added = 0
    departments_failed = 0
    for departments in departments_results.results:
        for results in departments['departments']:
            results['ss_id'] = snapshot_id
            if db_func.insert_departments(results):
                departments_added+=1
            else:
                departments_failed+=1
    logger.info(f"Departments, Added: {departments_added}, Failed: {departments_failed}")
    return True

## Locations
def process_location():
    logger.info(f"Starting {stack()[0][3]}")
    locations_results = http_func.get_freshservice('locations')
    if locations_results.status_code > 299:
        logger.error(make_err_str(locations_results))
        return
    loc_added=0
    loc_failed=0
    for location in locations_results.results:
        for results in location['locations']:
            results['ss_id'] = snapshot_id
            if db_func.insert_locations(results):
                loc_added+=1
            else:
                loc_failed+=1
    logger.info(f"Location, Added: {loc_added}, Failed: {loc_failed}")
    return True

##Requests
def process_requesters():
    logger.info(f"Starting {stack()[0][3]}")
    requesters_results = http_func.get_freshservice('requesters')
    if requesters_results.status_code > 299:
        logger.error(make_err_str(requesters_results))
        return
    req_added = 0
    req_failed = 0
    for requesters in requesters_results.results:
        for results in requesters['requesters']:
            results['ss_id'] = snapshot_id
            if db_func.insert_requesters(results):
                req_added += 1
            else:
                req_failed += 1
    logger.info(f"Requesters, Added: {req_added}, Failed: {req_failed}")

    requester_groups_results = http_func.get_freshservice('requester_groups')
    if requester_groups_results.status_code > 299:
        logger.error(make_err_str(requester_groups_results))
        return
    rg_added = 0
    rg_failed = 0
    for r_group in requester_groups_results.results:
        for results in r_group['requester_groups']:
            results['ss_id'] = snapshot_id
            if db_func.insert_requester_groups(results):
                rg_added += 1
            else:
                rg_failed += 1
    logger.info(f"Requester Groups, Added: {rg_added}, Failed: {rg_failed}")
    return True
            
## Service Category
def process_service_category():
    logger.info(f"Starting {stack()[0][3]}")
    service_categories_results = http_func.get_freshservice('service_catalog/categories')
    if service_categories_results.status_code > 299:
        print(make_err_str(service_categories_results))
        return
    sc_added = 0
    sc_failed = 0
    for s_categories in service_categories_results.results:
        for results in s_categories['service_categories']:
            results['ss_id'] = snapshot_id
            if db_func.insert_service_categories(results):
                sc_added += 1
            else:
                sc_failed += 1
    logger.info(f"Service category, Added: {sc_added}, Failed: {sc_failed}")

## Service Items
def process_service_items():
    logger.info(f"Starting {stack()[0][3]}")
    service_items_results = http_func.get_freshservice('service_catalog/items')
    if service_items_results.status_code > 299:
        logger.error(make_err_str(service_items_results))
        return
    si_added = 0
    si_failed = 0
    for s_items in service_items_results.results:
        for results in s_items['service_items']:
            results['ss_id'] = snapshot_id
            if db_func.insert_service_items(results):
                si_added += 1
            else:
                si_failed += 1
    logger.info(f"Service items, Added: {si_added}, Failed: {si_failed}")

## Solutions
def process_solutions():
    logger.info(f"Starting {stack()[0][3]}")
    def get_solutions_categories():
        solutions_category_id_list = []
        solutions_categories_results = http_func.get_freshservice('solutions/categories')
        if solutions_categories_results.status_code > 299:
            logger.error(make_err_str(solutions_categories_results))
            return
        cat_add = 0
        cat_failed = 0
        for category in solutions_categories_results.results:
            for results in category['categories']:
                results['ss_id'] = snapshot_id
                if db_func.insert_solutions_categories(results):
                    cat_add += 1
                    solutions_category_id_list.extend([results[key] for key in results if key == 'id'])
                else:
                        cat_failed += 1
        logger.info(f"Solution category, Added: {cat_add}, Failed: {cat_failed}")
        return solutions_category_id_list

    def get_solutions_folders(solutions_category_id_list = list):
        solutions_folder_results = None
        solutions_folder_id_list = []
        folder_added = 0
        folder_failed = 0
        if not solutions_category_id_list:
            logger.error("Empty list of solutions category ids")
            folder_failed=fake_err_num
        else:
            for category_id in solutions_category_id_list:
                solutions_folder_results = http_func.get_freshservice(f'solutions/folders?category_id={category_id}')
                if solutions_folder_results.status_code > 299:
                    logger.error(make_err_str(solutions_folder_results))
                    continue

                for folder in solutions_folder_results.results:
                    for results in folder['folders']:
                        results['ss_id'] = snapshot_id
                        if db_func.insert_solutions_folders(results):
                            folder_added += 1
                            solutions_folder_id_list.extend([results[key] for key in results if key == 'id'])
                        else:
                            folder_failed += 1
        logger.info(f"Folders, Added: {folder_added}, Failed: {folder_failed}")
        return solutions_folder_id_list

    def get_solutions_articles(solutions_folder_id_list = list):
        solutions_articles_results = None
        sa_added = 0
        sa_failed = 0
        if not solutions_folder_id_list:
            logger.error("No solutions folder ids found")
            sa_failed = fake_err_num
        else:
            for folder_id in solutions_folder_id_list:
                solutions_articles_results =  http_func.get_freshservice(f'solutions/articles?folder_id={folder_id}')
                
                if solutions_articles_results.status_code > 299:
                    logger.error(make_err_str(solutions_articles_results))
                    continue

                for article in solutions_articles_results.results:
                    for results in article['articles']:
                        results['ss_id'] = snapshot_id
                        if db_func.insert_solutions_articles(results):
                            sa_added += 1
                        else:
                            sa_failed += 1
        logger.info(f"Solution Article, Added: {sa_added}, Failed: {sa_failed}")
        return solutions_articles_results
    
    solutions_categories_results = get_solutions_categories()
    solutions_folder_results = get_solutions_folders(solutions_categories_results)
    get_solutions_articles(solutions_folder_results)
    return True

## Vendors
def process_vendors():
    logger.info(f"Starting {stack()[0][3]}")
    vendor_results = http_func.get_freshservice('vendors')
    if vendor_results.status_code > 299:
        logger.error(make_err_str(vendor_results))
        return False
    ven_add = 0
    ven_failed = 0
    for vendor in vendor_results.results:
        for results in vendor['vendors']:
            results['ss_id'] = snapshot_id
            if db_func.insert_vendors(results):
                ven_add += 1
            else:
                ven_failed += 1
    logger.info(f"Vendors, Add: {ven_add}, Failed: {ven_failed}")
    return True

## Tickets
def process_tickets():
    logger.info(f"Starting {stack()[0][3]}")
    tickets_results = http_func.get_freshservice('tickets')
    if tickets_results.status_code > 299:
        logger.error(make_err_str(tickets_results))
        return
    ticket_added = 0
    ticket_failed = 0
    for ticket in tickets_results.results:
        for results in ticket['tickets']:
            results['ss_id'] = snapshot_id
            if db_func.insert_tickets(results):
                ticket_added += 1
            else:
                ticket_failed += 1
    logger.info(f"Tickets, Added: {ticket_added}, Failed: {ticket_failed}")


###############################
if process_agents():
    logger.info("Finished processing agents.")

if process_assets():
    logger.info("Finished processing assets.")  

if process_custom_objects():
    logger.info("Finished processing agents.")

if process_departments():
    logger.info("Finished processing departments.")
 
if process_location():
    logger.info("Finished processing locations.")

if process_requesters():
    logger.info("Finished processing requesters.")

if process_service_category():
    logger.info("Finished processing service category.")

if process_service_items():
    logger.info("Finished processing service items.")

if process_solutions():
    logger.info("Finished processing solutions.")

if process_tickets():
    logger.info("Finished processing tickets.")

if process_vendors():
    logger.info("Finished processing vendors.")
