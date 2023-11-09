# Connect an external MySQL Database

This guide explains how to __use an external MySQL database__ with deployKF.

---

## Introduction

deployKF includes an embedded MySQL instance.
However, you will likely want to replace this with an external MySQL database for production usage.

!!! danger "Embedded MySQL is NOT for Production"

    The [embedded MySQL instance](https://github.com/deployKF/deployKF/tree/v0.1.3/generator/templates/manifests/deploykf-opt/deploykf-mysql) is only intended for development and testing purposes.
    It is a single-instance MySQL server, with no backups, and no high-availability.
    For production usage, you should always use an external MySQL database.

!!! warning "MySQL 8.0.4+"

    Kubeflow Pipelines ONLY supports authenticating with the [`mysql_native_password`](https://dev.mysql.com/doc/refman/8.0/en/native-pluggable-authentication.html) plugin and NOT the [`caching_sha2_password`](https://dev.mysql.com/doc/refman/8.0/en/caching-sha2-pluggable-authentication.html) plugin (see [`kubeflow/pipelines#9549`](https://github.com/kubeflow/pipelines/issues/9549)).

    Since MySQL version 8.0.4, [the default authentication plugin is `caching_sha2_password`](https://dev.mysql.com/blog-archive/upgrading-to-mysql-8-0-default-authentication-plugin-considerations/), so you may have to explicitly set the `mysql_native_password` plugin for the user you create. 
    
    Alternatively, you may set your MySQL server's `default-authentication-plugin` to `mysql_native_password`.

## 1. Disable Embedded MySQL

The [`deploykf_opt.deploykf_mysql.enabled`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L993) value controls if the embedded MySQL instance is deployed.

For example, to disable MySQL, set the following value:

```yaml
deploykf_opt:
  deploykf_mysql:
    enabled: false
```

## 2. Create Databases and User

You must manually create the databases (schemas) for Kubeflow Pipelines and Katib, and assign the correct permissions to the users they connect as.

For example, you might run the following SQL commands to create the databases and users:

```sql
-- create the databases
CREATE DATABASE IF NOT EXISTS `katib`;
CREATE DATABASE IF NOT EXISTS `kfp_cache`;
CREATE DATABASE IF NOT EXISTS `kfp_metadata`;
CREATE DATABASE IF NOT EXISTS `kfp_pipelines`;

-- create the 'kubeflow' user (allowing access from any host)
CREATE USER 'kubeflow'@'%' IDENTIFIED WITH mysql_native_password BY 'MY_PASSWORD';

-- grant access to the databases
GRANT ALL PRIVILEGES ON `katib`.* TO 'kubeflow'@'%';
GRANT ALL PRIVILEGES ON `kfp_cache`.* TO 'kubeflow'@'%';
GRANT ALL PRIVILEGES ON `kfp_metadata`.* TO 'kubeflow'@'%';
GRANT ALL PRIVILEGES ON `kfp_pipelines`.* TO 'kubeflow'@'%';
```

Here are some MySQL database services which can be used with deployKF:

Platform | MySQL Service
--- | ---
Amazon Web Services | [Amazon Relational Database Service (RDS)](https://aws.amazon.com/rds/)
Microsoft Azure | [Azure Database for MySQL](https://azure.microsoft.com/en-us/services/mysql/)
Google Cloud | [Cloud SQL](https://cloud.google.com/sql)
Alibaba Cloud | [ApsaraDB RDS for MySQL](https://www.alibabacloud.com/product/apsaradb-for-rds-mysql)
IBM Cloud | [IBM Cloud Databases for MySQL](https://www.ibm.com/cloud/databases-for-mysql)
Self-Hosted | [MySQL Community Edition](https://www.mysql.com/products/community/)

## 3. Connect Katib

To connect Katib to your external MySQL database, you will need to configure the following values:

- [`kubeflow_tools.katib.mysqlDatabase`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L1306-L1308) - database/schema name
- [`kubeflow_tools.katib.mysql`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L1290-L1304) - connection details & credentials

For example, the following values will connect Katib to an external MySQL database:

```yaml
kubeflow_tools:
  katib:
    mysqlDatabase: "katib"

    mysql:
      useExternal: true
      host: "mysql.example.com"
      port: 3306
      auth:
        ## (OPTION 1):
        ##  - set username/password with values (NOT RECOMMENDED)
        #username: kubeflow
        #password: password

        ## (OPTION 2):
        ##  - read a kubernetes secret from the 'kubeflow' namespace
        ##  - note, `existingSecret*Key` specifies the KEY NAMES in the 
        ##    secret itself, which contain the secret values
        existingSecret: "my-secret-name"
        existingSecretUsernameKey: "username"
        existingSecretPasswordKey: "password"
```


## 4. Connect Kubeflow Pipelines

To connect Kubeflow Pipelines to your external MySQL database, you will need to configure the following values:

- [`kubeflow_tools.pipelines.mysqlDatabases`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L1775-L1780) - database/schema names
- [`kubeflow_tools.pipelines.mysql`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L1759-L1773) - connection details & credentials

For example, the following values will connect Kubeflow Pipelines to an external MySQL database:

```yaml
kubectl_tools:
  pipelines:
    mysqlDatabases:
      cacheDatabase: kfp_cache
      metadataDatabase: kfp_metadata
      pipelinesDatabase: kfp_pipelines

    mysql:
      useExternal: true
      host: "mysql.example.com"
      port: 3306
      auth:
        ## (OPTION 1):
        ##  - set username/password with values (NOT RECOMMENDED)
        #username: kubeflow
        #password: password

        ## (OPTION 2):
        ##  - read a kubernetes secret from the 'kubeflow' namespace
        ##  - note, `existingSecret*Key` specifies the KEY NAMES in the 
        ##    secret itself, which contain the secret values
        existingSecret: "my-secret-name"
        existingSecretUsernameKey: "username"
        existingSecretPasswordKey: "password"
```