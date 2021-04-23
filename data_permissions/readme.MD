# Data Permissions
Una vez que se encuentra con información procesada y lista para ser consumida, es necesario indicar qué usuarios tienen acceso a cuáles tablas.  
  
No importa que las políticas IAM indiquen que el rol tiene acceso al bucket.  
No importa que las políticas IAM indiquen que el rol tiene acceso a la base de datos y tablas del *data catalog*.  
No importa que el VPC Endpoint permita consumir información.
  
Es necesario generar AWS LakeFormation Permissios mediante el componente *AWS::LakeFormation::Permissions* donde se indica el rol/usuario, los permisos y la tabla o base de datos.  
  
Sin estos permisos los usuarios no podrán acceder a la información del data lake.
