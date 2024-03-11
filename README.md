# Scrabble-and-IA-project

Para correr lo que tenemos hasta ahora, hacer desde este mismo directorio:
python3 prueba.py

### Instalación de pipreqs

Si aún no tienes `pipreqs` instalado, puedes hacerlo fácilmente mediante pip. Abre una terminal y ejecuta el siguiente comando:

```bash
pip install pipreqs
```

### Generación del archivo requirements.txt

Una vez instalado pipreqs, navega en la terminal hasta la carpeta principal de tu proyecto. Desde allí, puedes generar el archivo requirements.txt ejecutando:

```bash
pipreqs ./
```

Este comando analizará el proyecto y creará un `requirements.txt` en la raíz del proyecto, listando todas las dependencias externas identificadas.

### Actualización del archivo requirements.txt

Si ya tienes un archivo requirements.txt pero deseas actualizarlo para reflejar cualquier cambio en las dependencias de tu proyecto, puedes usar el comando pipreqs con la opción --force para sobrescribir el archivo existente:

```bash
pipreqs ./ --force
```

Este comando generará un nuevo `requirements.txt`, reemplazando el anterior, con las dependencias actuales del proyecto.
