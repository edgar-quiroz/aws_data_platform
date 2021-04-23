# Infra

Los Glue Jobs por defecto no tienen acceso a todos los servicios AWS, es necesario generar una serie de componentes para establecer la comunicación requerida.  
  
## KafkaSecurityGroup
Todos los Glue Connectors requieren un Security Group el cual permite la comunicación con otros servicios, este sg se utiliza para establecer la comunicación con Kafka. 

## S3Endpoint 
Un componente intermedio entre la comunicación Glue-S3 es un VPC Endpoint, el conector no lo pide explícitamente pero para su funcionamiento da por hecho que habrá un conector configurado para el servicio S3 con los permisos necesarios para acceder a los objetos.
  
## NetworkConnection
Glue no tiene comunicación directa con S3, para establecer esa comunicacón es necesario crear un conector tipo *Network* el cual implicitamente requiere un VPC Endpoint funcionando.

## GlueKafkaConnection
De igual forma, par aque Glue pueda acceder a Kafka es necesario tener configurado un conector tipo Kafka, *al parecer* este conector no requiere el VPC Endpoint funcionando.