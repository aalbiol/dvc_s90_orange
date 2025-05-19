

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
    * Usando el cuaderno *notebooks/preanotar_nuevo_lote.ipynb*, **configurando adecuadamente los directorios** de la evaluación y de salida, generar los pngs y jsons para CVAT

* Recoger anotaciones de CVAT

## Para entrenar a mano

* El fichero generado está configurado en el yaml

* El fichero generado contiene información sobre fecha de creación, datos empleados, parámetros de entrenamiento,...


```
conda activate mscandvc
cd dvc_s90_orange
python ../src_clasificacion_vistas/train/trainPatchMIL_Lists.py config/config.yaml
```

### Guadar modelo en DVC

Si se utiliza *dvc repro* esto no es necesario

```
dvc add out_models/modelo.pkl
dvc push
```

Lo anterior actualiza/crea fichero out_models.pkl.dvc

Seguidamente deberemos hacer **git commit**

## Para evaluar a mano

Se lee el modelo y todas las imágenes de train y validación y se guardan sus scores.
El resultado se escribe en la carpeta out_evaluate (configurado en yaml)

También se calculan los aucs de cada tipo de defecto

```
conda activate mscandvc
cd dvc_s90_orange
python ../src_clasificacion_vistas/evaluate/evaluateMIL .py config/config.yaml
```

## Para generar report a mano 

Reejecuta todas las celdas de un cuaderno releyendo los ficheros con los scores de la última evaluación y actualiza el jupyter

```
conda activate mscandvc
cd dvc_s90_orange
jupyter nbconvert --to notebook --execute  reports/analisis_prestaciones.ipynb
```

## Para realizar inferencia a  mano

La salida se guarda en ficheros json (uno por directorio) en out_predict
```
conda activate mscandvc
cd dvc_s90_orange
python ../src_clasificacion_vistas/evaluate/predictMIL .py config/config1.yaml directorio1 directorio2 directorio3
```


## Para generar reports a mano

Reejecuta todas las celdas de un cuaderno releyendo los ficheros con los scores de la última evaluación y actualiza el jupyter

```
conda activate mscandvc
cd dvc_s90_orange
jupyter nbconvert --to notebook --execute  reports/analisis_prestaciones.ipynb
```


## Para 

# Ejecución automática

Se pueden reproducir todos los pasos anteriores de un tirón, por ejemplo si se modifica la configuración al añadir una nueva carpeta de imágenes.

Se lee el fichero **dvc.yaml** , que és donde se describen todos los pasos:

* split train-val

* Entrenamiento

* Evaluación

* Reports


```
conda activate mscandvc
cd dvc_olivas_clasificacion_vistas
dvc repro
```

# Inferencia sobre imágenes no anotadas

Existe un script que recibe como entrada una lista de directorios y calcula los scores de cada defecto de cada imagen

De un fichero yaml de configuración se lee:

* Los patrones para encontrar imágenes 
* la configuración de donde se guarda el resultado
* El modelo a emplear (contiene información sobre la normalización)

```
python ../src_clasificacion_vistas/predict/predict.py config/config.yaml  directorio1 directorio2 ...'
```

