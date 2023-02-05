#!/usr/bin/env python3
from pathlib import Path
import sys
import argparse
import db_func
import fs_restore
from pprintpp import pprint as pp
import loggy
from rich.console import Console
from rich.table import Table
import json

console = Console()

short_script_name = Path(__file__).stem
logger = loggy.logging.getLogger(short_script_name)
script_name = Path(__file__).name
left_just= 15

table = Table(show_header=True, header_style="bold magenta",show_lines=True)

def agents(args):
    if not args.snap:
        print("--snap is required")
        return 1
    snap={"ss_id": args.snap}
    
    ag_get_agents=None

    if args.list:
        ag_table=table
        ag_table.add_column('ID', width=15)
        ag_table.add_column('First Name', width=15)
        ag_table.add_column('Last Name', width=15)
        ag_table.add_column('Email', width=15)
        ag_table.add_column('Group ID', width=15)
        ag_table.add_column('Restore ID', width=15)
        if args.agents and args.agents.isnumeric():
            agents = db_func.get_agents({"id": args.agents, **snap})
        elif args.agents:
            agents = db_func.get_agents(agents=snap, email=args.agents)
        else:
            for agents in db_func.get_agents(agents=snap, all=True):
                ag_table.add_row(str(agents.id), agents.first_name, agents.last_name, agents.email, str(agents.group_ids), str(agents.iid))
            console.print(ag_table)
            return 0
        if not requesters:
            print("No Agents found")
            return 1
        ag_table.add_row(str(agents.id), agents.first_name, agents.last_name, agents.email, str(agents.group_ids), str(agents.iid))
        console.print(ag_table)
        return 0

    if args.restore:
        ag_get_agents = db_func.get_agents(snap, iid = args.restore)
        if not ag_get_agents:
            print("No agents were found in the database")
            return 1
        ag_restore_agents = fs_restore.restore_agents(ag_get_agents)
        if not ag_restore_agents:
            return 1

def agent_groups(args):
    if not args.snap:
        print("--snap is required")
        return 1
    snap={"ss_id": args.snap}
    
    agent_groups=None

    if args.list:
        agg_table=table
        agg_table.add_column('ID', width=15)
        agg_table.add_column('Name', width=15)
        agg_table.add_column('description', width=15)
        agg_table.add_column('member IDS', width=15)
        agg_table.add_column('Restore ID', width=15)
        if args.agent_groups and args.agent_groups.isnumeric():
            agent_groups = db_func.get_agent_groups({"id": args.agent_groups, **snap})
        elif args.agent_groups:
            agent_groups = db_func.get_agent_groups(groups=snap, name=args.agent_groups)
        else:
            for agent_groups in db_func.get_agent_groups(groups=snap, all=True):
                agg_table.add_row(str(agent_groups.id), agent_groups.name, agent_groups.description, str(agent_groups.members), str(agent_groups.iid))
            console.print(agg_table)
            return 0
        if not agent_groups:
            print("No Agent Groups found")
            return 1
        agg_table.add_row(str(agent_groups.id), agent_groups.name, agent_groups.description, str(agent_groups.members), str(agent_groups.iid))
        console.print(agg_table)
        return 0

    if args.restore:
        agg_get_agent_groups = db_func.get_agent_groups(snap, iid = args.restore)
        if not agg_get_agent_groups:
            print("No agent groups were found in the database")
            return 1
        agg_restore_agent_groups = fs_restore.restore_agent_groups(agg_get_agent_groups)
        if not agg_restore_agent_groups:
            return 1

def assets(args):
    if not args.snap:
        print("--snap is required")
        return 1
    snap={"ss_id": args.snap}
    
    as_get_assets=None

    if args.list:
        assets=None
        as_table=table
        as_table.add_column('ID', width=15)
        as_table.add_column('Display ID', width=15)
        as_table.add_column('Name', width=15)
        as_table.add_column('Asset Tag', width=15)
        as_table.add_column('User ID', width=15)
        as_table.add_column('Restore ID', width=15)
        if args.assets and args.assets.isnumeric():
            assets = db_func.get_assets({"id": args.assets, **snap})
        elif args.assets:
            assets = db_func.get_assets(assets = snap, name = args.assets)
        else:
            for assets in db_func.get_assets(assets=snap, all=True):
                as_table.add_row(str(assets.id), str(assets.display_id), assets.name, assets.asset_tag, assets.user_id, str(assets.iid))
            console.print(as_table)
            return 0
        if not assets:
            print("No Assets found")
            return 1
        as_table.add_row(str(assets.id), str(assets.display_id), assets.name, assets.asset_tag, assets.user_id, str(assets.iid))
        console.print(as_table)
        return 0

    if args.restore:
        as_get_assets = db_func.get_assets(snap, iid = args.restore)
        if not as_get_assets:
            print("No assets were found in the database")
            return 1
        as_restore_assets = fs_restore.restore_assets(as_get_assets)
        if not as_restore_assets:
            return 1

def custom_objects(args):
    if not args.snap:
        print("--snap is required")
        return 1
    snap={"ss_id": args.snap}
    custom_objects = None

    if args.list:
        co_table=table
        co_table.add_column('Custom Object ID', width=15)
        co_table.add_column('Custom Object Title', width=15)
        co_table.add_column('Description', width=55)
        if args.custom_objects and args.custom_objects.isnumeric():
            custom_objects = db_func.get_custom_objects({"id": args.custom_objects, **snap})
        elif args.custom_objects:
            custom_objects = db_func.get_custom_objects(custom_objects=snap, title = args.custom_objects)
        else:
            for custom_objects in db_func.get_custom_objects(custom_objects=snap, all = True):
                co_table.add_row(str(custom_objects.id), custom_objects.title, str(custom_objects.description))
            console.print(co_table)
            return 0
        if not custom_objects:
            print("No custom objects")
            return 1
        co_table.add_row(str(custom_objects.id), custom_objects.title, str(custom_objects.description))
        console.print(co_table)
        return 0

def custom_object_records(args):
    if not args.snap:
        print("--snap is required")
        return 1
    snap={"ss_id": args.snap}
    co_get_custom_objects = None

    if args.custom_objects:
        if args.custom_objects.isnumeric():
            co_get_custom_objects = db_func.get_custom_objects({"id": args.custom_objects, **snap})
        else:
            co_get_custom_objects = db_func.get_custom_objects(custom_objects=snap, title = args.custom_objects)
        if not co_get_custom_objects:
            print("No custom objects")
            return 1
       
    
    if args.list:
        cor_table=table
        if co_get_custom_objects:
            records = db_func.get_custom_object_records(snap, custom_object_id = co_get_custom_objects.id)
        else:
            records = db_func.get_custom_object_records(snap, all = True)
        if not records:
            print("No custom object records found")
            return 1
        cor_table.add_column('Custom Object ID', width=15)
        cor_table.add_column('Custom Object Title', width=15)
        cor_table.add_column('Record ID', width=15)
        cor_table.add_column('Data', width=55)
        cor_table.add_column('Restore ID', width=15)
        for record in records:
            if co_get_custom_objects:
                t_obj=co_get_custom_objects
            else:
                t_obj=db_func.get_custom_objects({"id": record.custom_object_id, **snap})
            cor_table.add_row(str(record.custom_object_id), t_obj.title, str(record.bo_display_id), str(record.data), str(record.iid))
        console.print(cor_table)
        return 0

    if args.restore:
        cor_get_records = db_func.get_custom_object_records(snap, iid = args.restore)
        if not cor_get_records:
            print("No records were found in the database")
            return 1
        cor_restore_records = fs_restore.restore_custom_object_records(cor_get_records)
        if not cor_restore_records:
            return 1

def departments(args):
    if not args.snap:
        print("--snap is required")
        return 1
    snap={"ss_id": args.snap}
    
    dep_get_departments=None

    if args.list:
        departments=None
        dep_table=table
        dep_table.add_column('ID', width=15)
        dep_table.add_column('Name', width=15)
        dep_table.add_column('Restore ID', width=15)
        if args.departments and args.departments.isnumeric():
            departments = db_func.get_departments({"id": args.departments, **snap})
        elif args.departments:
            departments = db_func.get_departments(departments = snap, name = args.departments)
        else:
            for departments in db_func.get_departments(departments=snap, all=True):
                dep_table.add_row(str(departments.id), departments.name, str(departments.iid))
            console.print(dep_table)
            return 0
        if not departments:
            print("No Departments found")
            return 1
        dep_table.add_row(str(departments.id), departments.name, departments.description, str(departments.iid))
        console.print(dep_table)
        return 0

    if args.restore:
        dep_get_departments = db_func.get_departments(snap, iid = args.restore)
        if not dep_get_departments:
            print("No departments were found in the database")
            return 1
        dep_restore_departments = fs_restore.restore_departments(dep_get_departments)
        if not dep_restore_departments:
            return 1

def requesters(args):
    if not args.snap:
        print("--snap is required")
        return 1
    snap={"ss_id": args.snap}
    
    requesters=None

    if args.list:
        re_table=table
        re_table.add_column('ID', width=15)
        re_table.add_column('First Name', width=15)
        re_table.add_column('Last Name', width=15)
        re_table.add_column('Primary Email', width=35)
        re_table.add_column('Department ID', width=15)
        re_table.add_column('Restore ID', width=15)
        if args.requesters and args.requesters.isnumeric():
            requesters = db_func.get_requesters({"id": args.requesters, **snap})
        elif args.requesters:
            requesters = db_func.get_requesters(requesters=snap, primary_email=args.requesters)
        else:
            for requesters in db_func.get_requesters(requesters=snap, all=True):
                re_table.add_row(str(requesters.id), requesters.first_name, requesters.last_name, str(requesters.primary_email), str(requesters.department_ids), str(requesters.iid))
            console.print(re_table)
            return 0
        if not requesters:
            print("No Requesters found")
            return 1
        re_table.add_row(str(requesters.id), requesters.first_name, requesters.last_name, str(requesters.primary_email), str(requesters.department_ids), str(requesters.iid))
        console.print(re_table)
        return 0

    if args.restore:
        re_get_requesters = db_func.get_requesters(snap, iid = args.restore)
        if not re_get_requesters:
            print("No requesters were found in the database")
            return 1
        re_restore_requesters = fs_restore.restore_requesters(re_get_requesters)
        if not re_restore_requesters:
            return 1

def requester_groups(args):
    if not args.snap:
        print("--snap is required")
        return 1
    snap={"ss_id": args.snap}
    
    requester_groups=None

    if args.list:
        reg_table=table
        reg_table.add_column('ID', width=15)
        reg_table.add_column('Name', width=15)
        reg_table.add_column('Description', width=15)
        reg_table.add_column('Restore ID', width=15)
        if args.requester_groups and args.requester_groups.isnumeric():
            requester_groups = db_func.get_requester_groups({"id": args.requester_groups, **snap})
        elif args.requester_groups:
            requester_groups = db_func.get_requester_groups(requester_groups=snap, name=args.requester_groups)
        else:
            for requester_groups in db_func.get_requester_groups(requester_groups=snap, all=True):
                reg_table.add_row(str(requester_groups.id), requester_groups.name, requester_groups.description, str(requester_groups.iid))
            console.print(reg_table)
            return 0
        if not requester_groups:
            print("No Requester Groups found")
            return 1
        reg_table.add_row(str(requester_groups.id), requester_groups.name, requester_groups.description, str(requester_groups.iid))
        console.print(reg_table)
        return 0

    if args.restore:
        reg_get_requester_groups = db_func.get_requester_groups(snap, iid = args.restore)
        if not reg_get_requester_groups:
            print("No requester groups were found in the database")
            return 1
        reg_restore_requester_groups = fs_restore.restore_requester_groups(reg_get_requester_groups)
        if not reg_restore_requester_groups:
            return 1

def snapshots(args):
    if args.prune:
        removed=db_func.run_retention(args.prune)
        if removed:
            for rm in removed:
                logger.info(f"Removed snapshot {rm.id}:{rm.date}")
            logger.info("Removed %s snapshots from the database" % len(removed))
        else:
            logger.info(f"No snapshots found older then {args.prune} days")
        return 0
    
    if args.list:
        snaps=db_func.get_snapshots_by()
        if not snaps:
            logger.error("No snapshots found")
            return 1
        
        snap_table=table
        snap_table.add_column('ID', width=15)
        snap_table.add_column('Date', width=35)
        for snap in snaps:
            snap_table.add_row(str(snap.id), str(snap.date))
        console.print(snap_table)
        return 0

    row = None
    if args.id:
        row=db_func.get_snapshots_by(id = args.id)
        if not row:
            logger.error("Snapshot ID not found")
            return 1
        
        snap_table=table
        snap_table.add_column('ID', width=15)
        snap_table.add_column('Date', width=35)
        snap_table.add_row(str(row.id), str(row.date))
        console.print(snap_table)
        return 0

def service_categories(args):
    if not args.snap:
        print("--snap is required")
        return 1
    snap={"ss_id": args.snap}
    
    service_categories=None

    if args.list:
        svc_table=table
        svc_table.add_column('ID', width=15)
        svc_table.add_column('Name', width=15)
        svc_table.add_column('Description', width=15)
        svc_table.add_column('Position', width=15)
        svc_table.add_column('Restore ID', width=15)
        if args.service_categories and args.service_categories.isnumeric():
            service_categories = db_func.get_service_categories({"id": args.service_categories, **snap})
        elif args.service_categories:
            service_categories = db_func.get_service_categories(service_categories = snap, name = args.service_categories)
        else:
            for service_categories in db_func.get_service_categories(service_categories=snap, all=True):
                svc_table.add_row(str(service_categories.id), service_categories.name, service_categories.description, str(service_categories.position), str(service_categories.iid))
            console.print(svc_table)
            return 0
        if not service_categories:
            print("No service categories found")
            return 1
        svc_table.add_row(str(service_categories.id), service_categories.name, service_categories.description, str(service_categories.position), str(service_categories.iid))
        console.print(svc_table)
        return 0

    if args.restore:
        svc_get_svc = db_func.get_service_categories(snap, iid = args.restore)
        if not svc_get_svc:
            print("No assets were found in the database")
            return 1
        svc_restore_svc = fs_restore.restore_service_categories(svc_get_svc)
        if not svc_restore_svc:
            return 1

def solutions_articles(args):
    if not args.snap:
        print("--snap is required")
        return 1
    snap={"ss_id": args.snap}
    
    sa_get_folders=None

    if args.folder:
        if args.folder.isnumeric():
            sa_get_folders = db_func.get_solutions_folders({"id": args.folder, **snap})
        else:
            sa_get_folders = db_func.get_solutions_folders(snap, name=args.folder)
        if not sa_get_folders:
            print("You need folders, go to staples")
            return 1
        
    if args.list:
        articles = None
        art_table=table
        art_table.add_column('ID', width=15)
        art_table.add_column('Category', width=15)
        art_table.add_column('Folder', width=15)
        art_table.add_column('Title', width=15)
        art_table.add_column('Restore ID', width=15)
        if args.details:
            art_table.add_column('Details', width=55)
        if sa_get_folders:
            articles=db_func.get_solutions_articles(snap, folder_id = sa_get_folders.id)
        elif args.solutions_articles and args.solutions_articles.isnumeric():
            articles = db_func.get_solutions_articles({"id": args.solutions_articles, **snap})
        elif args.solutions_articles:
            articles = db_func.get_solutions_articles(articles=snap, title=args.solutions_articles)
        else:
            for articles in db_func.get_solutions_articles(articles=snap, all=True):
                t_cat=db_func.get_solutions_categories({"id": articles.category_id, **snap})
                t_folder=db_func.get_solutions_folders({"id": articles.folder_id, **snap})
                details=None
                if args.details:
                    del articles._sa_instance_state
                    details=str(articles.__dict__)
                art_table.add_row(str(articles.id), t_cat.name, t_folder.name, articles.title, str(articles.iid), details)
            console.print(art_table)
            return 0
        if not articles:
            print("No Articles found")
            return 1
        t_cat=db_func.get_solutions_categories({"id": articles.category_id, **snap})
        t_folder=db_func.get_solutions_folders({"id": articles.folder_id, **snap})
        details=None
        if args.details:
            del articles._sa_instance_state
            details=str(articles.__dict__)
        art_table.add_row(str(articles.id), t_cat.name, t_folder.name, articles.title, str(articles.iid), details)
        console.print(art_table)
        return 0

    if args.restore:
        sa_get_articles = db_func.get_solutions_articles(snap, iid = args.restore)
        if not sa_get_articles:
            print("No articles were found in the database")
            return 1
        sa_restore_articles = fs_restore.restore_solutions_articles(sa_get_articles)
        if not sa_restore_articles:
            return 1

def solutions_categories(args):
    if not args.snap:
        print("--snap is required")
        return 1
    snap={"ss_id": args.snap}
    categories = None

    if args.list:
        cat_table=table
        cat_table.add_column('ID', width=15)
        cat_table.add_column('Category', width=55)
        cat_table.add_column('Restore ID', width=15)
        if args.solutions_categories and args.solutions_categories.isnumeric():
            categories = db_func.get_solutions_categories({"id": args.solutions_categories, **snap})
        elif args.solutions_categories:
            categories = db_func.get_solutions_categories(categories = snap, name = args.solutions_categories)
        else:
            for categories in db_func.get_solutions_categories(categories=snap,all=True):
                cat_table.add_row(str(categories.id), categories.name, str(categories.iid))
            console.print(cat_table)
            return 0
        if not categories:
            print("No Categories found")
            return 1
        cat_table.add_row(str(categories.id), categories.name, str(categories.iid))
        console.print(cat_table)
        return 0

    if args.restore:
        sc_get_categories = db_func.get_solutions_categories(snap, iid = args.restore)
        if not sc_get_categories:
            print("No categories were found in the database")
            return 1
        sc_restore_categories = fs_restore.restore_solutions_categories(sc_get_categories)
        if not sc_restore_categories:
            return 1

def solutions_folders(args):
    if not args.snap:
        print("--snap is required")
        return 1
    snap={"ss_id": args.snap}
    sf_get_categories=None
    if args.category:
        if args.category.isnumeric():
            sf_get_categories = db_func.get_solutions_categories({"id": args.category, **snap})
        else:
            sf_get_categories = db_func.get_solutions_categories(categories = snap, name = args.category)
        if not sf_get_categories:
            print("No solutions categories")
            return 1
        
    if args.list:
        folders = None
        fold_table = table
        fold_table.add_column('ID', width=15)
        fold_table.add_column('Category', width=35)
        fold_table.add_column('Folder', width=35)
        fold_table.add_column('Restore ID', width=15)
        if sf_get_categories:
            folders = db_func.get_solutions_folders(snap, category_id = sf_get_categories.id)
        elif args.solutions_folders and args.solutions_folders.isnumeric():
            folders = db_func.get_solutions_folders({"id": args.solutions_folders, **snap})
        elif args.solutions_folders:
            folders = db_func.get_solutions_folders(folders = snap, name = args.solutions_folders)
        else:
            for folder in db_func.get_solutions_folders(folders=snap,all=True):
                if sf_get_categories:
                    t_cat = sf_get_categories
                else:
                    t_cat=db_func.get_solutions_categories({"id": folder.category_id, **snap})
                fold_table.add_row(str(folder.id), t_cat.name, folder.name, str(folder.iid))
            console.print(fold_table)
            return 0
        if not folders:
            print("No folders found.")
            return 1
        t_cat=db_func.get_solutions_categories({"id": folders.category_id, **snap})
        fold_table.add_row(str(folders.id), t_cat.name, folders.name, str(folders.iid))
        console.print(fold_table)
        return 0

    if args.restore:
        sf_get_folders = db_func.get_solutions_folders(snap, iid = args.restore)
        if not sf_get_folders:
            print("No folders were found in the database")
            return 1
        sf_restore_folders = fs_restore.restore_solutions_folders(sf_get_folders)
        if not sf_restore_folders:
            return 1
        
def tickets(args):
    if not args.snap:
        print("--snap is required")
        return 1
    snap={"ss_id": args.snap}
    
    tickets=None

    if args.list:
        t_table=table
        t_table.add_column('Requester ID', width=15)
        t_table.add_column('Subject', width=15)
        t_table.add_column('Emails', width=15)
        t_table.add_column('Responder ID', width=15)
        t_table.add_column('Restore ID', width=15)
        if args.tickets and args.tickets.isnumeric():
            tickets = db_func.get_tickets({"id": args.tickets, **snap})
        elif args.tickets:
            tickets = db_func.get_tickets(tickets = snap, subject = args.tickets)
        else:
            for tickets in db_func.get_tickets(tickets=snap, all=True):
                t_table.add_row(str(tickets.requester_id), tickets.subject, str(tickets.to_emails), str(tickets.responder_id), str(tickets.iid))
            console.print(t_table)
            return 0
        if not tickets:
            print("No Tickets found")
            return 1
        t_table.add_row(str(tickets.requester_id), tickets.subject, str(tickets.to_emails), str(tickets.responder_id), str(tickets.iid))
        console.print(t_table)
        return 0

    if args.restore:
        t_get_tickets = db_func.get_tickets(snap, iid = args.restore)
        if not t_get_tickets:
            print("No tickets were found in the database")
            return 1
        t_restore_tickets = fs_restore.restore_tickets(t_get_tickets)
        if not t_restore_tickets:
            return 1

def vendors(args):
    if not args.snap:
        print("--snap is required")
        return 1
    snap={"ss_id": args.snap}
    
    vendors=None

    if args.list:
        v_table=table
        v_table.add_column('ID', width=15)
        v_table.add_column('Name', width=15)
        v_table.add_column('Primary Contact ID', width=15)
        v_table.add_column('Address', width=15)
        v_table.add_column('Restore ID', width=15)
        if args.vendors and args.vendors.isnumeric():
            vendors = db_func.get_vendors({"id": args.vendors, **snap})
        elif args.vendors:
            vendors = db_func.get_vendors(vendors = snap, name = args.vendors)
        else:
            for vendors in db_func.get_vendors(vendors=snap,all=True):
                v_table.add_row(str(vendors.id), vendors.name, str(vendors.primary_contact_id), str(vendors.address), str(vendors.iid))
            console.print(v_table)
            return 0
        if not vendors:
            print("No Vendors found")
            return 1
        v_table.add_row(str(vendors.id), vendors.name, str(vendors.primary_contact_id), str(vendors.address), str(vendors.iid))
        console.print(v_table)
        return 0

    if args.restore:
        v_get_vendors = db_func.get_vendors(snap, iid = args.restore)
        if not v_get_vendors:
            print("No vendors were found in the database")
            return 1
        v_restore_vendors = fs_restore.restore_vendors(v_get_vendors)
        if not v_restore_vendors:
            return 1


parser = argparse.ArgumentParser(prog=script_name)
subparsers = parser.add_subparsers(dest="context")

ag = subparsers.add_parser(
    "agents",
    aliases=['ag'],
    help = "Work with Agents",
)
ag.set_defaults(func=agents)
ag.add_argument(
    "-l",
    "--list",
    action=argparse.BooleanOptionalAction,
    help="List all agents",
    required=False
)
ag.add_argument(
  "-r",
  "--restore",
  help="Restore an agent",
  required=False,
)
ag.add_argument(
  "-ag",
  "--agents",
  help="Filter by agents name or ID",
  required=False,
)
ag.add_argument(
  "-s",
  "--snap",
  help="Snapshot ID",
  type=int,
  required=True,
)

agg = subparsers.add_parser(
    "agent_groups",
    aliases=['agg'],
    help = "Work with Agent Groups",
)
agg.set_defaults(func=agent_groups)
agg.add_argument(
    "-l",
    "--list",
    action=argparse.BooleanOptionalAction,
    help="List all agent groups",
    required=False
)
agg.add_argument(
  "-r",
  "--restore",
  help="Restore an agent group",
  required=False,
)
agg.add_argument(
  "-agg",
  "--agent_groups",
  help="Filter by agent groups name or ID",
  required=False,
)
agg.add_argument(
  "-s",
  "--snap",
  help="Snapshot ID",
  type=int,
  required=True,
)


se = subparsers.add_parser(
    "assets",
    aliases=['se'],
    help = "Work with assets",
)
se.set_defaults(func=assets)
se.add_argument(
    "-l",
    "--list",
    action=argparse.BooleanOptionalAction,
    help="List all assets",
    required=False
)
se.add_argument(
  "-r",
  "--restore",
  help="Restore an asset",
  required=False,
)
se.add_argument(
  "-se",
  "--assets",
  help="Filter by assets name or ID",
  required=False,
)
se.add_argument(
  "-s",
  "--snap",
  help="Snapshot ID",
  type=int,
  required=True,
)

co = subparsers.add_parser(
  "custom_objects", 
  aliases=['co'],
  help="Work with custom objects"
)
co.set_defaults(func=custom_objects)
co.add_argument(
  "-co",
  "--custom_objects",
  help="Filter custom objects by title name or ID",
  required=False,
)
co.add_argument(
  "-l",
  "--list",
  help="List all custom objects",
  required=False,
  action=argparse.BooleanOptionalAction
)
co.add_argument(
  "-s",
  "--snap",
  help="Snapshot ID",
  type=int,
  required=True,
)

cor = subparsers.add_parser(
  "custom_object_records", 
  aliases=['cor'],
  help="Work with custom object records"
)
cor.set_defaults(func=custom_object_records)
cor.add_argument(
  "-l",
  "--list",
  help="List all custom object records",
  required=False,
  action=argparse.BooleanOptionalAction
)
cor.add_argument(
  "-co",
  "--custom_objects",
  help="Filter by custom objects title or ID",
  required=False,
)
cor.add_argument(
  "-r",
  "--restore",
  help="Restore an single record",
  type=int,
  required=False,
)
cor.add_argument(
  "-s",
  "--snap",
  help="Snapshot ID",
  type=int,
  required=True,
)

dep = subparsers.add_parser(
    "departments",
    aliases=['dep'],
    help = "Work with Departments",
)
dep.set_defaults(func=departments)
dep.add_argument(
    "-l",
    "--list",
    action=argparse.BooleanOptionalAction,
    help="List all departments",
    required=False
)
dep.add_argument(
  "-r",
  "--restore",
  help="Restore an agent",
  required=False,
)
dep.add_argument(
  "-dep",
  "--departments",
  help="Filter by departments name or ID",
  required=False,
)
dep.add_argument(
  "-s",
  "--snap",
  help="Snapshot ID",
  type=int,
  required=True,
)

re = subparsers.add_parser(
  "requesters", 
  aliases=['re'],
  help="Work with requesters"
)
re.set_defaults(func=requesters)
re.add_argument(
  "-l",
  "--list",
  action=argparse.BooleanOptionalAction,
  help="List all requesters",
  required=False,
)
re.add_argument(
  "-r",
  "--restore",
  help="Restore a requester",
  required=False,
)
re.add_argument(
  "-re",
  "--requesters",
  help="Filter by requesters name or ID",
  required=False,
)
re.add_argument(
  "-s",
  "--snap",
  help="Snapshot ID",
  type=int,
  required=True,
)

reg = subparsers.add_parser(
  "requester_groups", 
  aliases=['reg'],
  help="Work with requester groups"
)
reg.set_defaults(func=requester_groups)
reg.add_argument(
  "-l",
  "--list",
  action=argparse.BooleanOptionalAction,
  help="List all requester groups",
  required=False,
)
reg.add_argument(
  "-r",
  "--restore",
  help="Restore a requester group",
  required=False,
)
reg.add_argument(
  "-reg",
  "--requester_groups",
  help="Filter by requester groups name or ID",
  required=False,
)
reg.add_argument(
  "-s",
  "--snap",
  help="Snapshot ID",
  type=int,
  required=True,
)

sa = subparsers.add_parser(
  "solutions_articles", 
  aliases=['sa'],
  help="Work with solutions articles"
)
sa.set_defaults(func=solutions_articles)
sa.add_argument(
  "-d",
  "--details",
  action=argparse.BooleanOptionalAction,
  help="Show DB details of the articles in the list",
  type=int,
  required=False,
)
sa.add_argument(
  "-f",
  "--folder",
  help="Filter the solutions articles using this folder",
  required=False,
)
sa.add_argument(
  "-l",
  "--list",
  action=argparse.BooleanOptionalAction,
  help="List all solutions_articles",
  required=False,
)
sa.add_argument(
  "-r",
  "--restore",
  help="Restore an article to a folder",
  required=False,
)
sa.add_argument(
  "-sa",
  "--solutions_articles",
  help="Filter by solutions articles name or ID",
  required=False,
)
sa.add_argument(
  "-s",
  "--snap",
  help="Snapshot ID",
  type=int,
  required=True,
)

sc = subparsers.add_parser(
  "solutions_categories", 
  aliases=['sc'],
  help="With with solutions categories"
)
sc.set_defaults(func=solutions_categories)
sc.add_argument(
  "-l",
  "--list",
  action=argparse.BooleanOptionalAction,
  help="List all solutions_categories",
  required=False,
)
sc.add_argument(
  "-r",
  "--restore",
  help="Restore a solutions category",
  required=False,
)
sc.add_argument(
  "-sc",
  "--solutions_categories",
  help="Filter by solutions categories Name or ID",
  required=False,
)
sc.add_argument(
  "-s",
  "--snap",
  help="Snapshot ID",
  type=int,
  required=True,
)

sf = subparsers.add_parser(
  "solutions_folders", 
  aliases=['sf'],
  help="Work with solutions folders"
)
sf.set_defaults(func=solutions_folders)
sf.add_argument(
  "-c",
  "--category",
  help="Filter solutions folders using this category Name or ID",
  required=False,
)
sf.add_argument(
  "-l",
  "--list",
  action=argparse.BooleanOptionalAction,
  help="List all solutions folders",
  required=False,
)
sf.add_argument(
  "-r",
  "--restore",
  help="Restore a folder to a category",
  required=False,
)
sf.add_argument(
  "-sf",
  "--solutions_folders",
  help="Filter by solutions folders Name or ID",
  required=False,
)
sf.add_argument(
  "-s",
  "--snap",
  help="Snapshot ID",
  type=int,
  required=True,
)

ss = subparsers.add_parser(
  "snap_shots", 
  aliases=['snap'],
  help="Manage snapshots"
)
ss.set_defaults(func=snapshots)
ss.add_argument(
  "-l",
  "--list",
  help="List all snapshots",
  required=False,
  action=argparse.BooleanOptionalAction
)
ss.add_argument(
    "-i",
    "--id",
    help="Find a Snapshot by ID",
    type=int,
    required=False,
)
ss.add_argument(
    "-p",
    "--prune",
    help="Remove snapshots older then the specified number of days",
    type=int,
    required=False,
)

svc = subparsers.add_parser(
    "service_categories",
    aliases=['svc'],
    help = "Work with service categories",
)
svc.set_defaults(func=service_categories)
svc.add_argument(
    "-l",
    "--list",
    action=argparse.BooleanOptionalAction,
    help="List all service categories",
    required=False
)
svc.add_argument(
  "-r",
  "--restore",
  help="Restore a service category",
  required=False,
)
svc.add_argument(
  "-svc",
  "--service_categories",
  help="Filter by service categories name or ID",
  required=False,
)
svc.add_argument(
  "-s",
  "--snap",
  help="Snapshot ID",
  type=int,
  required=True,
)

t = subparsers.add_parser(
    "tickets",
    aliases=['t'],
    help = "Work with tickets",
)
t.set_defaults(func=tickets)
t.add_argument(
    "-l",
    "--list",
    action=argparse.BooleanOptionalAction,
    help="List all tickets",
    required=False
)
t.add_argument(
  "-r",
  "--restore",
  help="Restore a ticket",
  required=False,
)
t.add_argument(
  "-s",
  "--snap",
  help="Snapshot ID",
  type=int,
  required=True,
)
t.add_argument(
  "-t",
  "--tickets",
  help="Filter by ticket Subject or ID",
  required=False,
)

v = subparsers.add_parser(
    "vendors",
    aliases=['v'],
    help = "Work with a vendor",
)
v.set_defaults(func=vendors)
v.add_argument(
    "-l",
    "--list",
    action=argparse.BooleanOptionalAction,
    help="List all vendors",
    required=False
)
v.add_argument(
  "-r",
  "--restore",
  help="Restore a vendor",
  required=False,
)
v.add_argument(
  "-s",
  "--snap",
  help="Snapshot ID",
  type=int,
  required=True,
)
v.add_argument(
  "-v",
  "--vendors",
  help="Filter vendors by Name or ID",
  required=False,
)

args=parser.parse_args()
if not args.context:
  parser.print_help()
  sys.exit(1)

#return a exit code from the function
sys.exit(args.func(args))
