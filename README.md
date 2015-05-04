# IRC Bots
Various bots written in ruby using cinch.

###OR

Various bots written in python using sockets.

##Requirements
- cinch==2.2.4
- python==2.7
- postgresql==9.3
- postgresql-contrib==9.3
- pip==1.5.4
 - peewee==2.4.6
 - psycopg2==2.6

## Setting Up Postgresql on Linux
Since this can be a giant pain in the dick:

- Install requirements above
- `sudo -u postgres psql`
- CREATE ROLE \<the username\> WITH LOGIN PASSWORD '\<the password\>' CREATEDB;
- CREATE DATABASE \<some dbname\> OWNER \<the username\>;
- \c \<some dbname\>
- CREATE EXTENSION hstore;
- quit postgres
- `useradd <the username>`
- `sudo vim /etc/postgresql/9.3/main/pg_hba.conf`
 - Change `peer` to `md5`
 - `sudo service postgresql restart`
- `sudo -u <the username> psql`
 - Enter \<the password\>

If this doesn't work: let Brian know he fucked up the instructions.

