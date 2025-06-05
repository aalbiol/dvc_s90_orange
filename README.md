

# dvc_clasificacion_S90_Orange

Datos y pipelines para clasificar vistas de Naranjas con **anotaciones MIL**

* Las imágenes de cada fruto están en un fichero npz .Cada fichero npz tiene 
  * una lista de las vistas.

  * las vistas pueden tener tamaños diferentes

  * Las vistas pueden tener un número arbitrario de canales. En arándanos tienen 4 RGB-NIR

* Las anotaciones no especifican en qué vistas se ve el defecto y se encuentrane en un fichero JSON
  * En el fichero json además de las anotaciones se especifica el significado de los canales del npz: R,G,B,NIR,...





# Añadir remoto S3
```
dvc remote add -d s90_s3  s3://msc-dev-datalake/datasets/S90_DL
```




______________________________________________________

# Procedimientos manuales

## Añadir un nuevo lote de imágenes:

* Crear una nueva carpeta en *data* 
```
mkdir data/nuevo_lote
```

* Copiar dentro de ellas los subdirectorios conteniendo .npz, .png, .json

* Crear preanotaciones para anotar con CVAT

  * Crear una lista con las nuevas imágenes
  ```
  find data/nuevo_lote -name \*.json > data/nuevo_lote.txt
  ```
  * Crear un fichero de configuración clonando el de un modelo entrenado, y poner como lista de *test* *data/nuevo_lote.txt*
    * Configurar un directorio de salida de la evaluación diferente
    * Realizar la evaluación
    ```
    python ../src_clasificacion_vistas/evaluate/evaluatePatchMIL_Lists.py config/config_preanot.yml
    ```
    * Con el cuaderno *notebooks_dataset/preanotar_nuevo_lote.ipynb* Generar los jsons y pngs para subir a CVAT


* Recoger anotaciones de CVAT
    * Usando el cuaderno *notebooks_dataset/preanotarimbricar_jsons_frutos_quitar_views_annotations_remove_discarded_nuevo_lote.ipynb*, **configurando adecuadamente los directorios** de la evaluación y de salida, generar los pngs y jsons para CVAT . Elimina las imágenes de la carpeta "discarded"

* Subir a git y a dvc
  * git add *.json
  * dvc add *.png
  * dvc add *.npz
  * git commit -m "Nuevo dataset introducido"
  * git push
  * dvc push

* Generar listas de train, val y test
  * Buscar los nombres de los jsons nuevos
  * Crear una lista aleatorizada de los mismos
  * Sobre esa lista
    * 70 % primeros a data/train_list_nuevo_lote.txt
    * 20 % centrales a data/val_list_nuevo_lote.txt
    * el resto a data/test_list_nuevo_lote.txt
  * cat data/train_list_nuevo_lote.txt >> data/train_list.txt
  * idem con val_list y test_list.
## Para entrenar a mano

* El fichero generado está configurado en el yaml

* El fichero generado contiene información sobre fecha de creación, datos empleados, parámetros de entrenamiento,...


```
conda activate mscandvc
cd dvc_s90_orange
python ../src_clasificacion_vistas/train/trainPatchMIL_Lists.py config2/configSara.yaml
```

### Guadar modelo en DVC

Si se utiliza *dvc repro* esto no es necesario

```
dvc add out_models/modelo.pkl
dvc push
```

Lo anterior actualiza/crea fichero out_models.pkl.dvc

Seguidamente deberemos hacer **git commit**

### Exportar modelo a formato Torch Script

Para exportar el modelo en formato Torch Script para inferencia en C++ hay que
ejecutar el script **export_pkl_to_ts_model.py**.

Para ello:

```
cd ../src_dl_utils/tools
python export_pkl_to_ts_model.py .\..\..\dvc_s90_orange\out_models\s90_patch_Alba6_from5_2.pkl
```
Con esto, se generará el modelo exportado en el mismo directorio que el modelo pkl, con el mismo nombre pero formato .ts

## Para evaluar a mano

Se lee el modelo y todas las imágenes de train y validación y se guardan sus scores.
El resultado se escribe en la carpeta out_evaluate (configurado en yaml)

También se calculan los aucs de cada tipo de defecto

```
conda activate mscandvc
cd dvc_s90_orange
ppython ../src_clasificacion_vistas/evaluate/evaluatePatchMIL_Lists.py config2/configSara.yaml
```








## Para 

# Ejecución automática

Se pueden reproducir todos los pasos anteriores de un tirón, por ejemplo si se modifica la configuración al añadir una nueva carpeta de imágenes.

Se lee el fichero **dvc.yaml** , que és donde se describen todos los pasos:


* Entrenamiento

* Evaluación



```
conda activate mscandvc
cd dvc_olivas_clasificacion_vistas
dvc repro
```



