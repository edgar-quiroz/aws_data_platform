# AWS Data Lake using Lake Formation and CloudFormation

Un Data Lake es una colección de datos estructurados, no-estructurados y semi-estructurados provenientes de varias fuentes y a los cuales se les puede ejecutar una serie de análisis.

Alguno de los componentes de un Data Lake son:

1) **Data Store**.- S3 es el servicio utilizado para almacenar la información.
2) **Ingestion, process and serve**.- La ingesta se puede hacer con diferentes herramientas, desde funciones Lambda, Kinesis, Kafka o bien crawlers de Glue, la transformación y limpieza se puede realizar con Glue Jobs o bien scripts de Spark.
2) **Data Catalog**.- Glue Data Catalog se utilizará para almacenar la metadata de la información que se contiene en el data lake.
3) **Governance**.- AWS Lake Formation es el encargado de proveer los permisos necesarios y auditoria sobre los accesos a la información.

Un data lake sin alguno de los componentes mencionados anteriormente se considera data swamp.

## Prueba de concepto
En esta prueba de concepto se utilizarán los servicios: 
1) AWS S3 como recurso del data lake y para almacenar los resultados de Athena.
2) AWS Glue Data Catalog como administrador de metadata.
3) AWS Glue Crawler para obtener datos de la fuente y poblar el data catalog.
4) AWS Athena query análisis, exploración de datos.
5) AWS Lake Formation para administrar los permisos y auditar acceso a datos.

## Templates
Se tiene dos templates con los componentes a desplegar:

### lakeformation 
Contiene los componentes del data lake, desde buckets S3, Glue Data Catalog, WorkGroup de Athena, etc.

### Data Access
Es el listado de permisos a usuarios que pueden acceder al data lake.

## IAM Policies
Para esta prueba se requieren 4 roles con sus respectivas políticas.  
  
### CloudFormationRole

Es el encargado de generar los despliegues de los componentes, su política debe incluir permisos sobre:

1) AWS Glue para la creación de crawlers y bases de datos.
2) AWS Lake formation para la asignación de permisos y registrar los buckets que pertenecen al data lake.
3) AWS Athena para la creación de workgroups.
4) AWS S3 para buckets tanto del data lake como para resultados de Athena.

```yaml
CloudFormationPolicy:
    Type: AWS::IAM::ManagedPolicy
    Properties:
    ManagedPolicyName: CloudFormationPolicy
    Path: '/'
    PolicyDocument:
        Version: '2012-10-17'
        Statement:
        - Sid: S3BucketPermissions
            Effect: Allow
            Action:
            - s3:*Bucket*
            - s3:*Encryption*
            - s3:PutLifecycleConfiguration
            - s3:GetLifecycleConfiguration
            Resource: 
            - arn:aws:s3:::*serverlessdeploy*
            - arn:aws:s3:::cdp-*
        - Sid: S3ObjectPermissions
            Effect: Allow
            Action:
            - s3:PutObject
            - s3:GetObject
            - s3:DeleteObject
            Resource: 
            - arn:aws:s3:::*serverlessdeploy*/*
            - arn:aws:s3:::*cdp-*/*
        - Sid: LakeformationPermissions
            Effect: Allow
            Action:
            - lakeformation:PutDataLakeSettings
            - lakeformation:GetDataLakeSettings
            - lakeformation:GrantPermissions
            - lakeformation:RevokePermissions
            - lakeformation:BatchGrantPermissions
            - lakeformation:BatchRevokePermissions
            - lakeformation:RegisterResource 
            - lakeformation:DeregisterResource
            Resource: '*'
        - Sid: PassRoles
            Effect: Allow
            Action:
            - iam:PassRole
            - iam:GetRole
            Resource:
            - arn:aws:iam::<AccountId>:role/GlueETLRole
        - Sid: GluePermissions
            Effect: Allow
            Action:
            - glue:CreateDatabase
            - glue:DeleteDatabase
            - glue:UpdateDatabase
            - glue:GetDatabases
            - glue:GetDatabase
            - glue:CreateCrawler
            - glue:DeleteCrawler
            - glue:UpdateCrawler
            - glue:StartCrawler
            - glue:StopCrawler
            - glue:GetCrawler
            - glue:GetTables
            - glue:GetTable
            - glue:GetTableVersions
            - glue:GetTableVersion
            - glue:SearchTables
            - glue:GetPartitions
            - glue:GetPartition
            Resource: 
            - arn:aws:glue:us-east-1:<AccountId>:crawler/cdp-*
            - arn:aws:glue:us-east-1:<AccountId>:database/cdp-*
            - arn:aws:glue:us-east-1:<AccountId>:table/*
            - arn:aws:glue:us-east-1:<AccountId>:catalog
            - arn:aws:glue:us-east-1:<AccountId>:userDefinedFunction/cdp-*
        - Sid: AthenaWorkGroupPermissions
            Effect: Allow
            Action:
            - athena:DeleteWorkGroup
            - athena:CreateWorkGroup
            - athena:UpdateWorkGroup
            - athena:GetWorkGroup
            Resource: 
            - arn:aws:athena:us-east-1:<AccountId>:workgroup/cdp-*
```   
  
### GlueETLRole

Es el encargado de obtener la información de los buckets fuente y poblar el data catalog, su política debe incluir permisos sobre:

1) AWS Glue para la creación de tablas y particiones.
2) AWS Logs para la generación de logs y métricas.
3) AWS S3 para obtener información del bucket.

En esta versión no se incluyen Glue Jobs, si en una segunda iteración se crean los jobs, esta política debe ser actualizada con los permisos necesarios.

```yaml
GlueETLPolicy:
    Type: AWS::IAM::ManagedPolicy
    Properties:
    ManagedPolicyName: GlueETLPolicy
    Path: '/'
    PolicyDocument:
        Version: '2012-10-17'
        Statement:
        - Sid: GluePermissions
            Effect: Allow
            Action:
            - glue:GetDatabases
            - glue:GetDatabase
            - glue:CreateTable
            - glue:DeleteTable
            - glue:UpdateTable
            - glue:GetTables
            - glue:GetTable
            - glue:DeleteTableVersion
            - glue:BatchDeleteTable
            - glue:BatchDeleteTableVersion
            - glue:CreatePartition
            - glue:BatchCreatePartition
            Resource:
            - arn:aws:glue:us-east-1:<AccountId>:database/cdp-*
            - arn:aws:glue:us-east-1:<AccountId>:table/cdp*
            - arn:aws:glue:us-east-1:<AccountId>:catalog
            - arn:aws:glue:us-east-1:<AccountId>:userDefinedFunction/cdp-*
        - Sid: LogsPermissions
            Effect: Allow
            Action:
            - logs:CreateLogGroup
            - logs:CreateLogStream
            - logs:PutLogEvents
            - logs:AssociateKmsKey
            Resource: 
            - arn:aws:logs:us-east-1:<AccountId>:log-group:/aws-glue/crawlers:*
        - Sid: S3Permissions
            Effect: Allow
            Action:
            - s3:GetObject
            - s3:PutObject
            - s3:DeleteObject
            Resource:
            - arn:aws:s3:::cdp-*/*
            - arn:aws:s3:::aws-glue-*/*
        - Sid: GenericPermissions
            Effect: Allow
            Action:
            - s3:GetBucketLocation
            - s3:ListBucket
            - s3:ListAllMyBuckets
            Resource: '*'
```

### Admin user
AWS Lake Formation por defecto no tiene administradores y a diferencia de otros servicios la cuenta raíz no tiene acceso a sus componentes.

La política del administrador debe contener todos los permisos para Lake Formation, inicialmente sólo se va a utilizar para 3 acciones.
1) Registrar al rol **CloudFormationRole** como database creator.
2) Asignar los permisos necesarios al rol **CloudFormationRole** para que a su vez pueda asignar los permisos a los usuarios que se van a crear, es decir, para crear un usuario con permisos SELECT sobre una base de datos, **CloudFormationRole** debe tener permisos SELECT y grant SELECT sobre esa misma base de datos.
3) Asignar acceso a los datos al rol **GlueETLRole**, esta acción por el momento no está soportada en CloudFormation por lo cual se debe hacer manual, en la sección **Data Locations** se agregan permisos *Grant* sobre el bucket fuente al rol **GlueETLRole**.

Una vez desplegado el template **lakeformation** se deben ejecutar estas 3 acciones antes de ejecutar el crawler y asignar permisos.

El crawler va a crear las tablas.
No se pueden asignar permisos sin antes haber ejecutado el crawler.

```yaml
AdminPolicy:
    Type: AWS::IAM::ManagedPolicy
    Properties:
    ManagedPolicyName: AdminPolicy
    Path: '/'
    PolicyDocument:
        Version: '2012-10-17'
        Statement:
        - Sid: AdminPermissions
            Effect: Allow
            Action:
            - cloudformation:*
            - iam:*
            - s3:*
            - logs:*
            - glue:*
            - lakeformation:*
            - cloudwatch:*
            - cloudtrail:*
            - tag:*
            - athena:*
            Resource: '*'
        # - Effect: Allow
        #     Action:
        #     - ram:CreateResourceShare
        #     - ram:DeleteResourceShare
        #     Resource: "*"
        #     Condition:
        #     StringLikeIfExists:
        #         ram:RequestedResourceType:
        #         - glue:Table
        #         - glue:Database
        #         - glue:Catalog
        # - Effect: Allow
        #     Action:
        #     - ram:UpdateResourceShare
        #     - ram:DeleteResourceShare
        #     Resource: "*"
        #     Condition:
        #     StringLike:
        #         ram:ResourceShareName:
        #         - LakeFormation*
        # - Effect: Allow
        #     Action:
        #     - glue:PutResourcePolicy
        #     - glue:DeleteResourcePolicy
        #     - organizations:DescribeOrganization
        #     - organizations:DescribeAccount
        #     - ram:Get*
        #     - ram:List*
        #     Resource: "*"
        # - Effect: Allow
        #     Action:
        #     - organizations:ListRoots
        #     - organizations:ListAccountsForParent
        #     - organizations:ListOrganizationalUnitsForParent
        #     Resource: "*"
```

El bloque comentado son los permisos necesarios para hacer cross account access.

### Analytics user
Este usuario se crea como ejemplo para el acceso a los datos, el usuario Admin se controlaría en la cuenta que contiene el data lake y el resto de usuarios son los 'Clientes' del data lake.

La política para el usuario Analyst está delimitada a:

1) Acceder a los datos de lake formation.
2) Acceder sólo a las bases de datos Glue que se indiquen.
3) Acceder sólo al workgroup de Athena que se indique, el cual tiene limites y controles para su rol.
4) Escribir sobre S3 los resultados generados por Athena.

```yaml
AnalystPolicy:
    Type: AWS::IAM::ManagedPolicy
    Properties:
    ManagedPolicyName: AnalystPolicy
    Path: '/'
    PolicyDocument:
        Version: '2012-10-17'
        Statement:
        - Sid: LakeformationPermissions
            Effect: Allow
            Action:
            - lakeformation:GetDataAccess 
            Resource: '*'
        - Sid: GluePermissions
            Effect: Allow
            Action:
            - glue:GetDatabases
            - glue:GetDatabase
            - glue:GetTables
            - glue:GetTable
            - glue:SearchTables
            - glue:GetTableVersions
            - glue:GetPartitions
            Resource: 
            - arn:aws:glue:us-east-1:<AccountId>:database/cdp-*
            - arn:aws:glue:us-east-1:<AccountId>:table/cdp*
            - arn:aws:glue:us-east-1:<AccountId>:catalog
            - arn:aws:glue:us-east-1:<AccountId>:userDefinedFunction/cdp-*
        - Sid: AthenaWorkGroupPermissions
            Effect: Allow
            Action:
            - athena:GetWorkGroup
            - athena:StartQueryExecution
            - athena:GetQueryResults
            - athena:GetWorkGroup
            - athena:CancelQueryExecution
            - athena:StopQueryExecution
            - athena:GetQueryExecution
            Resource: 
            - arn:aws:athena:us-east-1:<AccountId>:workgroup/cdp-*
        - Sid: AthenaListWorkGroupPermissions
            Effect: Allow
            Action:
            - athena:ListWorkGroups
            Resource: '*'
        - Sid: S3ObjectPermissions
            Effect: Allow
            Action:
            - s3:PutObject
            - s3:GetObject
            - s3:AbortMultipartUpload
            Resource:
            - arn:aws:s3:::*athena-results-bucket/*
        - Sid: S3ListPermissions
            Effect: Allow
            Action:
            - s3:GetBucketLocation
            - s3:ListBucket
            - s3:ListAllMyBuckets
            Resource: '*'
```