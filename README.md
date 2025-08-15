# Elephanator (V1.1.0)

Elephanator is a database patching tool designed to streamline the deployment of updates to production environments. It allows developers to apply changes from the main branch directly to a live database, ensuring that new features, fixes, and schema modifications are delivered efficiently. By integrating with automation platforms like Jenkins, Elephanator can automatically deploy committed changes to a production environment, making it ideal for projects where the database structure or data is updated frequently.

## Setup
**Add the database connection string**
Create a file called `appsettings.json` and use the following format for your connection string
```json
{
  "connectionString": "host={Replace This};port=5432;dbname={Replace This};user={Replace This};password={Replace This};"
}
```

**Install Dependencies**
Ensure you have installed all the python dependencies listed in requirements.txt
```bash
pip install -r requirements.txt
```

**Note: The patcher will not work if you skip these steps!**

## Commands
**Add a database patch.**
```bash
python dbtool.py --addpatch --name <patch name>
```

**Execute all database patches.**
```bash
python dbtool.py --execute
```

**Compile all database patches into a .sql file**
Useful for setting up a database for unit tests.
```bash
python dbtool.py --compile
```
