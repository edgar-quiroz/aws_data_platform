# AWS Data Plarform

Este repo incluye templates de ejemplo para la creación de una plataforma basada en datos, tomando como base los roles:  
- Data Engineer
- Data Architect
- Data Analyst
- Data Scientist (próximas actualizaciones)
- ML Engineer (próximas actualizaciones)
  
## Data Lake
Un Data Lake es una colección de datos estructurados, no-estructurados y semi-estructurados provenientes de varias fuentes y a los cuales se les puede ejecutar una serie de análisis.

Alguno de los componentes de un Data Lake son:

1) **Data Store**.- S3 es el servicio utilizado para almacenar la información.
2) **Ingestion, process and serve**.- La ingesta se puede hacer con diferentes herramientas, desde funciones Lambda, Kinesis, Kafka o bien crawlers de Glue, la transformación y limpieza se puede realizar con Glue Jobs o bien scripts de Spark.
2) **Data Catalog**.- Glue Data Catalog se utilizará para almacenar la metadata de la información que se contiene en el data lake.
3) **Governance**.- AWS Lake Formation es el encargado de proveer los permisos necesarios y auditoria sobre los accesos a la información.

Un data lake sin alguno de los componentes mencionados anteriormente se considera data swamp.

## Componentes (templates) y orden en despliegue

### /vpc & /iam
Este template se debe desplegar en primera instancia, se encarga de crear la VPC, Roles y permisos necesarios para el resto de templates.  
  
## /infra
Este repo se encarga de crear los conectores que requiere Glue para poder acceder a los datos, Glue por defecto no puede acceder a S3, es necesario crear una conexión tipo Network y un VPC Endpoint.  
  
## /buckets
S3 es un servicio de almacenamiento de uso general, es necesario indicar cuáles de todos los buckets existentes pertenecen al data lake.  
En primera instancia es crear los buckets RAW y CURATED para el data lake así como el bucket que utilizará Athena para almacenar los resultados.
> Otras arquitecturas utilizan buckets adicionales como STAGING.  
  
## /lake_formation
Como se mencionó anteriormente, LakeFormation requiere de un administrador, este template se encarga de indicar al usuario Admin como administrador del data lake.  
Adicional se encarga de indicar que los buckets RAW y CURATED pertenecen al data lake (data lake locations).  
  
## /athena
Este template se encarga de crear los WorkGroups necesarios para todos los perfiles que interactúan con la plataforma.  
  
## /data_catalog
Este template despliega las bases de datos y tablas que se requieran en el data lake.  
Por defecto nada tiene permisos sobre las tablas que se crean, no importa que la política indica que un rol tiene acceso a la base de datos.  
Para indicar permisos se necesita un componente *AWS::LakeFormation::Permissions*, en este template se dan permisos únicamente a los jobs que acceden y cargan la información (GlueETLRole). 
  
## /jobs
Este template despliega los jobs que procesarán la información, pueden ser jobs streaming o batch.  
En esta versión despliega un job streaming que se conecta a Kafka y almacena los datos en el data lake.  
  
## /data_permissions
Similar a lo que ocure en */data_catalog* donde se dan permisos al rol GlueETLRole para acceder a la información.  
En este template se asignan todos los permisos de consumo necesarios que se vayan necesitando, en esta versión se da permisos de consulta al usuario Analyst sobre la tablas creadas.
