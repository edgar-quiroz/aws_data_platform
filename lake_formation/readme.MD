# LakeFormation
Este template configura los componentes requeridos por AWS LakeFormation, según la documentación aún hay un par de funcionalidad que no están soportadas por CloudFormation y que por el momento se deben crear manual, estos componentes se documentarán indicando (manual).  
  
## LakeformationSettings
Este componente indica el usuario asignado como administrador del datalake.  
  
## Database creator (manual)
En la sección **Admins and database creators** se indican tanto los administradores como los usuarios/roles que tienen permitido crear bases de datos, en nuestro caso se debe dar permisos de creación de bases de datos a **CloudFormationRole**.  
  
Si bien este tipo de permisos si están soportados por *AWS::LakeFormation::Permissions*, CloudFormation no se puede indicar permisos en recursos en los que aún no tiene permisos, en esta versión los permisos se asignan manualmente y más adelante se implementarán mediante **CodePipeline** o **CodeStar**.  
  
## RawDatalakeLocation y CuratedDatalakeLocation
Como se mencionó en el template *Buckets*, S3 almacena todo tipo de información, para indicar cuales buckets pertenecen al data lake se debe crear componentes *AWS::LakeFormation::Resource*.  
  
## DataLocationResource (manual)
Una vez registrados los buckets como ubicaciones del data lake, es necesario indicar quién tiene permisos de acceso, en este momento
*AWS::LakeFormation::Permissions* no soporta el tipo de *Resource* *DataLocationResource*, por lo que se debe hacer manual.  
  
En la sección *data locations* se debe dar permisos **Grant** a los roles **GlueETLRole** y **CloudFormationRole**. 
   
> En una siguiente iteración se va a explorar la posibilidad de utilizar AWS CLI dentro de CodeBuild para omitir todos los pasos manuales.
