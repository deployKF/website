# Connect an external MySQL Database

This guide explains how to __use an external MySQL database__ with deployKF.

---

## Overview

deployKF includes an embedded MySQL instance, however, you may want to replace this with an external MySQL database.

!!! danger "Production Usage"

    The embedded MySQL instance is only intended for development and testing purposes.
    It is a single-instance MySQL server, with no backups, and no high-availability.
    For production usage, you should always use an external MySQL database.

??? info "Supported MySQL Services"

    deployKF should work with any MySQL service!

    Here are some MySQL services listed by platform:
    
    Platform | MySQL Service
    --- | ---
    Amazon Web Services | [Amazon Relational Database Service (RDS)](https://aws.amazon.com/rds/)
    Microsoft Azure | [Azure Database for MySQL](https://azure.microsoft.com/en-us/services/mysql/)
    Google Cloud | [Cloud SQL](https://cloud.google.com/sql)
    Alibaba Cloud | [ApsaraDB RDS for MySQL](https://www.alibabacloud.com/product/apsaradb-for-rds-mysql)
    IBM Cloud | [IBM Cloud Databases for MySQL](https://www.ibm.com/cloud/databases-for-mysql)

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

!!! warning "MySQL Authentication Plugin"

    Kubeflow Pipelines is only capable of connecting to MySQL as a user authenticated by the [`mysql_native_password`](https://dev.mysql.com/doc/refman/8.0/en/native-pluggable-authentication.html) plugin ([`kubeflow/pipelines#9549`](https://github.com/kubeflow/pipelines/issues/9549)).

    Note that in MySQL 8.0.4, [the default authentication plugin was changed](https://dev.mysql.com/blog-archive/upgrading-to-mysql-8-0-default-authentication-plugin-considerations/), so you may have to explicitly set the `mysql_native_password` plugin for the user you create. 
    Alternatively, you may set your MySQL server's `default-authentication-plugin` to `mysql_native_password`.

## 2. Connect Katib

The following values configure Katib to use an external MySQL database:

??? value "[`kubeflow_tools.katib.mysql`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1237-L1251)"

    These values configure which MySQL server is used by Katib.

??? value "[`kubeflow_tools.katib.mysqlDatabase`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1253-L1255)"

    This value configures the name of the MySQL database (schema) which Katib will use.


## 3. Connect Kubeflow Pipelines

The following values configure Kubeflow Pipelines to use an external MySQL database:

??? value "[`kubeflow_tools.pipelines.mysql`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1706-L1720)"

    These values configure which MySQL server is used by Kubeflow Pipelines.

??? value "[`kubeflow_tools.pipelines.mysqlDatabases`](https://github.com/deployKF/deployKF/blob/v0.1.1/generator/default_values.yaml#L1722-L1727)"

    These values configure the names of the MySQL databases (schemas) which Kubeflow Pipelines will use.