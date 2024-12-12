#### Definition
Ein Data Store ist sequentiell konsistent gdw. jeder Prozess die selbe Reihenfolge von Operationen sieht.
*The result of any execution is the same as if the (read and write) operations by all processes on the data store were executed in some sequential order and the operations of each individual process appear in this sequence in the order specified by its program*

![[Pasted image 20241115154748.png]]
- Keine Aussage über Zeit im Sinne von "die letzte Schreiboperation" o.ä.
- Jeder Prozess muss mit jeder *validen* Reihenfolge von Operationen arbeiten können.
![[Pasted image 20241117124803.png]]
![[Pasted image 20241117124836.png]]
#### Beispiel
![[Pasted image 20241115155113.png]]
