Templates para AWS CloudFormation
==================================

Cada carpeta incluye los recursos necesarios para generar cada proyecto

* Weblogic: Templates para crear 2 instancias en cluster en AWS.



Weblogic
--------

Templates para generar dos servidores en modalidad Cluster. Donde el primero es un servidor Admin y un Managed Server y el segundo es solo un Managed Server que está incluido al Cluster original. El Cluster está manejado por un balanceador de carga.

Los scripts en python manejan el tema de IPs dinámicos de AWS, borrando y creando nuevos servidores al servidor Admin (con WLST).


