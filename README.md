# Freshservice Backup
# Setup
### local dev
Create a secrets json file
```json
{
    "FS_API_KEY": "",
    "DB_USER": "",
    "DB_PPASSWORD": ""
}
```
Then set the ENV var
If you omit the DB_* keys it will default to a sqlite3 database, otherwise it a postgresql connection

```sh
export SECERTS_FILE=/path/to/secrets.file
```
Set another ENV var for logging
```sh
export LOG_CONFIG_FILE=logger.yaml.example
```
This defaults to logger.yaml



### Production
The secrets file is genertated from GCP Secrets Manager in a Init Container and store in /var/tmp/secrets/secrets.json

Set the FS API URL in the k8s manifest
```yaml
env:
- name: FS_API_URL
  value: ""
```
Defaults to the sandbox account "https://{name}-fs-sandbox.freshservice.com/api/v2/"

# Running
To start the backup
```sh
./get-fs.py
```
To prune backups older then 60 days
```sh
./manage-hd.py snap --prune 60
```
To restore a entry
```sh
./manage-hd.py snap -l 
```
Grab the snapshot ID which will be used on subsequent runs.
```sh
./manage-hd.py agents -s <snap_id> -l
```
Grap the restore ID
```sh
./manage-hd.py agents -s <snap_id> -r <restore_id>
```


##### How each lib works

### requirements.txt will list adittional dependencies needed for the hd_backup to run.

### loggy.py and logger.yaml are used for logging. Checking the logs will be esential if you run into any issues.

### auth.py is using GCP/AWS secrets manger to handle credentials and authentication.

### hd_db.py is where the database tables and columns are defined that will be used in the backup.
### Sqlalchemy allows you to map databases with python.
### Regardless of which helpdesk management tool you're using, refer to it's api documentation
### to confirm data type and if the api supports POST/PUT for whichever record you're looking to restore.

### http_func.py is where the http api commands are defined that will be used to backup the data and then to restore the data.

### backup-hd.py contains the functions that actually use the GET call to retrieve the data and then store it in the database.
### it also contains snapshot class which is used to track each backup at a specific time.

### db_func.py is used to build the functions that allow the database to be queried.

### manage-hd.py is the CLI portion of the program, that calls db_func to query and hd_restore, to restore.

### hd_restore.py calls http_func to check to see if the data exists. If it does it ask the user if they would like to
### overwite the existing data or cancel. If it does not exist, it ask the user if they would like to create a new record.