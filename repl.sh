

mysqldump --opt nova > nova.sql
mysqldump --opt neutron > neutron.sql

mysqlimport -u root -p nova nova.sql
mysqlimport -u root -p neutron neutron.sql
