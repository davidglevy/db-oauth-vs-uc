# Databricks notebook source
# MAGIC %md
# MAGIC 
# MAGIC ## Create ADLS Mounts and Tables
# MAGIC Before we got here, we created a container called "autoloader-dh" in storage account "dlevyadlsmountsdb".

# COMMAND ----------

dbutils.widgets.text("1_scope-name", "oauth-demo", "Scope Name")
dbutils.widgets.text("2_storage-account", "dlevy0oauth0vs0uc", "Storage Account")
dbutils.widgets.text("3_container", "oauth-example", "Container")

# COMMAND ----------

scope = dbutils.widgets.get("1_scope-name")
storage_account = dbutils.widgets.get("2_storage-account")
container = dbutils.widgets.get("3_container")

# COMMAND ----------

keyValue = dbutils.secrets.get(scope=scope, key="keyValue")
applicationId = dbutils.secrets.get(scope=scope, key="applicationId")
directoryId = dbutils.secrets.get(scope=scope, key="directoryId")

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id": applicationId,
          "fs.azure.account.oauth2.client.secret": keyValue,
          "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{directoryId}/oauth2/token"}

# COMMAND ----------

spark.conf.set("fs.azure.account.auth.type", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id", applicationId)
spark.conf.set("fs.azure.account.oauth2.client.secret", keyValue)
spark.conf.set("fs.azure.account.oauth2.client.endpoint", f"https://login.microsoftonline.com/{directoryId}/oauth2/token")


# COMMAND ----------

path = f"abfss://{container}@{storage_account}.dfs.core.windows.net/"
print(path)
dbutils.fs.ls(path + "/test")

# COMMAND ----------

dbutils.fs.mount(source = f"abfss://{container}@{storage_account}.dfs.core.windows.net/",
  mount_point = f"/mnt/{container}",
  extra_configs = configs
)

# COMMAND ----------

dbutils.fs.ls("/mnt/oauth-example/")

# COMMAND ----------

#containerName = "autoloader-dh"

#dbutils.fs.mkdirs(f"/mnt/{containerName}")

#dbutils.fs.unmount(f"/mnt/{containerName}")

#dbutils.fs.mount(
#  source = f"abfss://{containerName}@dlevyadlsmountsdb.dfs.core.windows.net/",
#  mount_point = f"/mnt/{containerName}",
# extra_configs = configs)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE IF NOT EXISTS adha_demo;
# MAGIC USE adha_demo;

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS people_bronze;
# MAGIC DROP TABLE IF EXISTS people_silver;

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC DROP TABLE IF EXISTS people_bronze;
# MAGIC CREATE OR REPLACE TABLE people_bronze (
# MAGIC   id string,
# MAGIC   name string,
# MAGIC   email string,
# MAGIC   dob string,
# MAGIC   timestamp string,
# MAGIC   load_timestamp string,
# MAGIC   car_model string,
# MAGIC   --address STRUCT<full_address: String, city: String, zip_code: String>
# MAGIC   address string
# MAGIC )
# MAGIC USING DELTA
# MAGIC LOCATION "/mnt/autoloader-dh/adha/corrupted/bronze";

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC DROP TABLE IF EXISTS people_bronze_converted;
# MAGIC CREATE OR REPLACE TABLE people_bronze_converted (
# MAGIC   id string,
# MAGIC   name string,
# MAGIC   email string,
# MAGIC   dob string,
# MAGIC   timestamp string,
# MAGIC   load_timestamp string,
# MAGIC   car_model string,
# MAGIC   address ARRAY<STRUCT<full_address: String, city: String, zip_code: String>>
# MAGIC )
# MAGIC USING DELTA
# MAGIC LOCATION "/mnt/autoloader-dh/adha/corrupted/bronze-converted";

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS people_silver;
# MAGIC CREATE OR REPLACE TABLE people_silver (
# MAGIC   id long,
# MAGIC   name string,
# MAGIC   email string,
# MAGIC   dob date,
# MAGIC   timestamp timestamp,
# MAGIC   load_timestamp string,
# MAGIC   car_model string,
# MAGIC   address ARRAY<STRUCT<full_address: String, city: String, zip_code: int>>
# MAGIC )
# MAGIC USING DELTA
# MAGIC LOCATION "/mnt/autoloader-dh/adha/corrupted/silver";

# COMMAND ----------

# MAGIC %sql
# MAGIC USE adha_demo;
# MAGIC DESCRIBE DETAIL people_silver;

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE people_silver;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES;
