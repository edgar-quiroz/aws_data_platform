# Data Catalog
Este template almacena los componentes  del data catalog, pueden ser desde tablas, bases de datos y hasta los crawlers en caso que así se defina.  
  
## CompanyDatabase
Es una base de datos demo la cual almacena información genérica y de pruebas acerca de una compañía, como sus empleados.  

## EmployeeTable
Almacena la información de los empleados, el origen de los datos es Kafka mediante la tabla Kafka.  

## EmployeeTableGrants
Es necesario indicar que el rol **GlueETLRole** tiene permisos para escribir datos en la tabla **EmployeeTable**.  

## StreamingDatabase
Esta base de datos se utiliza para almacenar las tablas que contienen información streaming, en el caso de Kafka, para consumir la información es necesario indicar una tabla la cual almacena los metadatos del tópico, bootstrap-servers y estructura de la información.  
  
## KafkaTable
Esta tabla almacena la información para recibir los datos desde Kafka, entre los parámetros a configurar tenemos:  
- topicName
- typeOfData='kafka'
- bootstrap.servers='server1:9092,server2:9092'

## KafkaTableGrants
Al igual que con la tabla anterior, para cualquier tabla o bases de datos será necesario indicar quién puede acceder a la información, en este caso **GlueETLRole**.
  
