# Buckets
Este template crea todos los buckets que se utilizan en la plataforma.   
  
### AthenaResultsBucket
Este bucket almacena los resultados que genera Athena al ejecutar Queries, se utiliza en el template */athena*.  
  
### RawBucket
Este bucket es parte del data lake, almacena la información *raw*, mantiene el formato origen y no genera cambios en la información.  
  
### CuratedBucket
Este bucket es parte del data lake, almacena la información *curated* procesada y estructurada.  
  
> Los buckets RawBucket y CuratedBucket se utilizan principalmente en el template *lake_formation*