# Jobs
  
Este template contiene los jobs de procesamiento, estos jobs se pueden implementar desde la fuente hasta el destino o bien, únicamente del bucket *RAW* al *CURATED*.  
  
> Glue detecta automáticamente tipo de job **streaming** o **batch** utilizando el script de python.
  
## StreamingJob
Este job consume la informacón de Kafka y la deposita directamente en el data catalog, el el código fuente se indica cual es el origen y destino de información.  
  
Los pasos en el flujo de información son los siguientes: 
  
1) **KafkaTable** Esta tabla indica los metadatos necesarios para consumir la información, desde el tópico hasta la estructura del payload de Kafka definido como columnas y tipos de datos, se debe indicar la base de datos que contiene esta tabla la cual es **StreamingDatabase**.  

2) **EmployeeTable** Esta tabla almacenará el resultado dentro del data lake, se define el formato y columnas que tendrá la información, la contiene la base de datos **CompanyDatabase**. 
  
3) **NetworkConnection** y **GlueKafkaConnection** Ambos conectores son necesarios para la comunicación entre servicios, estos se configuran en la propiedad *Connections*.  
  
Una vez creado el job, dentro de **Glue Studio** se puede monitorear su progreso, iniciar manualmente o programado.  
  
### Parámetros
**--job-bookmark-option** indica si el job debe almacenar checkpoints de los registros procesados (job-bookmark-enable/job-bookmark-disable).  
**--TempDir** Si se habilita la opción bookmarks, se debe indicar una ubicación donde Glue almacenará los checkpoints.