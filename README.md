# Elephanator (V1.0.0)

Elephanator is a software tool designed for the development process of applications that require database deployment. It enables developers to effortlessly deploy a system’s database and make updates as changes occur, making it particularly useful in scenarios where the database may undergo frequent modifications.

Additionally, Elephanator is compatible with the production server, allowing developers to apply patches when they are committed to a master (production) branch using a tool like GitHub Actions.

## Commands
**Initialise the database with a connection string.**
```
python dbtool.py --init --connectionstring "<connection string>"
```
_This command must be executed before you use the software_

**Add a database patch.**
```
python dbtool.py --addpatch --name <patch name>
```

**Compile all patches into one single `.sql` file**
```
python dbtool.py --compile
```
_This command should be used to assist with unit testing._

**Execute all database patches.**
```
python dbtool.py --execute
```
