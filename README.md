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
Defaults to the sandbox account "https://color-fs-sandbox.freshservice.com/api/v2/"

# Running
To start the backup
```sh
./get-fs.py
```
To prune backups older then 60 days
```sh
./fs_argparse.py snap --prune 60
```
To restore a entry
```sh
./fs_argparse.py snap -l 
```
Grab the snapshot ID which will be used on subsequent runs.
```sh
./fs_argparse.py agents -s <snap_id> -l
```
Grap the restore ID
```sh
./fs_argparse.py agents -s <snap_id> -r <restore_id>
```
