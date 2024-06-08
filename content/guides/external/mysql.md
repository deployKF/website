---
icon: custom/mysql
description: >-
  Learn how and why deployKF needs MySQL.
  Learn how to use an external MySQL database to improve the performance and reliability of __Kubeflow Pipelines__ and __Katib__.
---

# MySQL

Learn how and why deployKF needs MySQL.
Learn how to use an external MySQL database to improve the performance and reliability of __Kubeflow Pipelines__ and __Katib__.

---

## __What is MySQL?__

[:custom-mysql-color: __MySQL__](https://www.mysql.com/) is an extremely popular and open-source [_relational database management system_](https://en.wikipedia.org/wiki/Relational_database_management_system).
Many of the world's largest applications use MySQL to store and manage their data.

---

## __Why does deployKF use MySQL?__

MySQL is a dependency of the following ML & Data tools, which are part of deployKF:

- [__Kubeflow Pipelines__](../../reference/tools.md#kubeflow-pipelines): stores metadata about pipelines, experiments, and runs
- [__Katib__](../../reference/tools.md#kubeflow-katib): stores metadata about hyperparameter tuning experiments

---

## __Connect an External MySQL__

By default, deployKF includes an [embedded MySQL instance](https://github.com/deployKF/deployKF/tree/v0.1.4/generator/templates/manifests/deploykf-opt/deploykf-mysql).
However, to improve the performance and reliability of Kubeflow Pipelines and Katib, we recommend using an external MySQL database.

!!! danger "Embedded MySQL"

    You should ALWAYS use an external MySQL database.
    The embedded MySQL is a single-instance server running in a Kubernetes Pod, with no backups or high-availability.

### __1. Prepare MySQL__

You may use any MySQL database service, as long as it is accessible from the Kubernetes cluster where deployKF is running.

You may consider using one of the following services:

Platform | MySQL Service
--- | ---
Amazon Web Services | [Amazon Relational Database Service (RDS)](https://aws.amazon.com/rds/)
Microsoft Azure | [Azure Database for MySQL](https://azure.microsoft.com/en-us/services/mysql/)
Google Cloud | [Cloud SQL](https://cloud.google.com/sql)
Alibaba Cloud | [ApsaraDB RDS for MySQL](https://www.alibabacloud.com/product/apsaradb-for-rds-mysql)
IBM Cloud | [IBM Cloud Databases for MySQL](https://www.ibm.com/cloud/databases-for-mysql)
Self-Hosted | [MySQL Community Edition](https://www.mysql.com/products/community/)

You must create some databases (schemas) and a user with the appropriate permissions to access them.

!!! warning "MySQL User Authentication"

    You MUST set the user's authentication plugin to [`mysql_native_password`](https://dev.mysql.com/doc/refman/8.0/en/native-pluggable-authentication.html), NOT [`caching_sha2_password`](https://dev.mysql.com/doc/refman/8.0/en/caching-sha2-pluggable-authentication.html), which is the [default in MySQL 8.0.4+](https://dev.mysql.com/blog-archive/upgrading-to-mysql-8-0-default-authentication-plugin-considerations/).
    Kubeflow Pipelines does not support `caching_sha2_password` ([`kubeflow/pipelines#9549`](https://github.com/kubeflow/pipelines/issues/9549)).

    The following SQL command will show the authentication plugin for each user:

    ```sql
    SELECT user, host, plugin FROM mysql.user;
    ```

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

### __2. Disable the Embedded MySQL__

The [`deploykf_opt.deploykf_mysql.enabled`](https://github.com/deployKF/deployKF/blob/v0.1.4/generator/default_values.yaml#L1162) value controls if the embedded MySQL instance is deployed.

The following values will disable the embedded MySQL instance:

```yaml
deploykf_opt:
  deploykf_mysql:
    enabled: false
```

### __3. Connect Katib__

To connect Katib to your external MySQL database, you will need to configure the following values:

Value | Purpose
--- | ---
[`kubeflow_tools.katib.mysqlDatabase`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L1306-L1308) | name of database/schema
[`kubeflow_tools.katib.mysql`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L1290-L1304) | connection details & credentials

The following values will connect Katib to an external MySQL database at `mysql.example.com` on port `3306`, using the `katib` database, reading the username and password from a Kubernetes secret called `my-secret-name` (from the `kubeflow` namespace):

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

### __4. Connect Kubeflow Pipelines__

To connect Kubeflow Pipelines to your external MySQL database, you will need to configure the following values:

Value | Purpose
--- | ---
[`kubeflow_tools.pipelines.mysqlDatabases`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L1775-L1780) | names of databases/schemas
[`kubeflow_tools.pipelines.mysql`](https://github.com/deployKF/deployKF/blob/v0.1.3/generator/default_values.yaml#L1759-L1773) | connection details & credentials

The following values will connect Kubeflow Pipelines to an external MySQL database at `mysql.example.com` on port `3306`, using the `kfp_cache`, `kfp_metadata`, and `kfp_pipelines` databases, reading the username and password from a Kubernetes secret called `my-secret-name` (from the `kubeflow` namespace):

```yaml
kubeflow_tools:
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