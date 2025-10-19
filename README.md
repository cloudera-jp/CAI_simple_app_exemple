# CAI_simple_app_exemple
Very simple &amp; small web app example for CAI Workbench Application

This small exmple shows how CAI apps interact with external tables on its datalake using SparkSQL.

## Prerequisites

1. **Create IDBroker mapping**
 - In SparkSQL, the app is needed to access the storage on its datalake directly.
 - For that, IDBroker mapping setting on the CDP environment is required.
 - Reffer to the following document to create IDBroker mapping
   - https://docs.cloudera.com/cdf-datahub/7.3.1/nifi-hive-ingest/topics/cdf-datahub-hive-ingest-idbroker-mapping.html

2. **Check the SparkSQL connection setting on your project on CAI**
 - Confirm the path where the external warehouse directory points.
 - You need to create the external table located under the path.

3. **Create the external table**
 - This app expects "simple_external" as the table name that has 3 columns named col1, col2 and col3.
 - To create "simple_external", refer to the following.
```sql
  CREATE EXTERNAL TABLE default.simple_external
  (
    col1 bigint ,
    col2 bigint ,
    col3 bigint
  ) 
  ROW FORMAT   DELIMITED
  FIELDS TERMINATED BY ','
  COLLECTION ITEMS TERMINATED BY '\002'
  MAP KEYS TERMINATED BY '\003'
  STORED AS TextFile
  LOCATION 's3a://YOUR-BUCKET/data/warehouse/tablespace/external/hive/simple_external'
  TBLPROPERTIES('transactional'='false');
```
 - Put the csv file like this to load initial data to "simple_external"
```
100,200,300
400,500,600
700,800,900
```