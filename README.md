Templates para AWS CloudFormation
==================================

Cada carpeta incluye los recursos necesarios para generar cada proyecto

* Weblogic: 2 instancias en cluster.
* Portal Web: Instancias con Auto Scaling.


Weblogic
--------

Son los templates para generar dos servidores en modalidad Cluster. Donde el primero es un servidor Admin y un Managed Server y el segundo es solo un Managed Server que está incluido al Cluster original. El Cluster está manejado por un balanceador de carga.

Los scripts en python manejan el tema de IPs dinámicos de AWS, borrando y creando nuevos servidores al servidor Admin (con WLST).


Portal Web
----------

Template para generar una granja de instancias con auto scaling (crecimiento horizontal a medida que se necesita).
