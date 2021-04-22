# Políticas y Roles

Se deben desplegar junto con las VPCs, estos dos componentes son necesarios para el resto de despliegues.  

### CloudFormationRole

La política utilizada para este Rol debe incluir permisos en los siguientes servicios:  
  
1) **S3** Se requiere permisos *Bucket*, *Encryption*, *Object*, *Lifecycle* para los arns especificados, se debe poder crear los buckets a utilizar en el datalake, el bucket donde Athena almacenará los resultados y el bucket donde serverless guarda el deployment.  
2) **lakeformation** Todas las acciones indicadas en lakeformation no soportan arns en resource, se debe indicar '*'.
3) **Glue** Se requiere permisos para la creación de bases de datos, tablas, crawlers, jobs, conexiones, entre otros.
4) **Athena** Se requiere permisos para crear WorkGroups, los cuales utilizarán los usuarios Estandard.
5) **EC2** Se requieren permisos para la creación de VPC Endpoints y Security Groups.  
  
  
>### Importante
>Los permisos para crear bases de datos y tablas se pueden delimintar mediante un ARN, en el caso de CloudFormationRole y GlueETLRole no deberían indicarse para que los nombres coincidan con la fuente.   
>Considerar dejar sólo: arn:aws:glue:us-east-1:${env:AccountId}:database*
  
### GlueETLRole
Este rol se utiliza principalmente para todos los jobs de *Extracción, Transformación y Carga*, su política debe incluir permisos en los servicios: 
  
1) **lakeformation:GetDataAccess** A diferencia del rol CloudFormation, este rol sólo necesita permisos *GetDataAccess* para acceder a la información.
2) **Glue** Requiere permiso para crear tablas, particiones, conexiones y la mayoría de permisos *Get* y/o *Describe*.
3) **CloudWatch** Requiere permisos para crear loggroups y escribir logs
4) **Otros** requiere permisos EC2 para acceder a los VPC Enpoints que utiliza el job para establecer conexión con otros servicios, necesita permisos NetworkInterface Y SecurityGroups para los conectores.  
  
## AdminPolicy
Se requiere crear un usuario Administrador y adjuntar esta política, LakeFormation a diferencia de otros servicios no tiene permisos por defecto, la cuenta raíz no puede acceder a la información si no se indica como Administrador.  
Se crea el usuario Admin específico para LakeFormation.  
  
Los permisos asignados para la POC fueron:
- cloudformation:*
- iam:*
- s3:*
- ec2:*
- logs:*
- glue:*
- lakeformation:*
- cloudwatch:*
- cloudtrail:*
- tag:*
- athena:*
  
## AnalystPolicy
Se requiere crear un usuario para acceso a la informacón y adjuntar esta política.  
Este usuario es para demostración de cómo limitar las tablas a las que puede acceder y los WorkGroups que puede utilizar.  
Los permisos necesarios deben incluir:  
1) Permisos GET sobre Glue únicamente en las bases de datos y tablas que se requiera.
2) Permisos GET sobre los WorkGroup de Athena que se le asignan.
3) Permisos de ejecución de Queries en Athena.
