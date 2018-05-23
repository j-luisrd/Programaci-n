#Descripción: Crea gráficas y datos importantes de un Snapshot.

for file in SNAPSHOTS/*
do
 filename=$(echo $file | cut -d / -f 2)
 d_m=$file/dark_matter.csv
 g=$file/gas.csv
 echo ''Iniciando análisis para $filename...''
 python Proyecto.py $d_m $g $filename
 echo ''Análisis completo para Snapshot $filename.''
done


