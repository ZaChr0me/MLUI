# Plugin Unity & Machine Learning (WIP)

## Etat d'avancement

A l'heure actuelle le plugin peut appeler la fonction de test `getInteger()` depuis [**_pyTest.py_**](./python/pyTest.py) mais n'arrive pas à exécuter correctement le code pour demander à l'IA une décision (fonction `play()` de [**_python.AiDemo_**](./python/AiDemo.py)). 

Il est cependant possible de jouer au puissance 4 contre l'IA de démonstration dans python en lançant directement [**_python.AiDemo_**](./python/AiDemo.py). 

## Configuration python et IA

Tensorflow est assez capricieux vis-à-vis des versions de python. Ce projet a été réalisé sous **_Python 3.7.9_**, nous recommandons donc cette version. Tensorflow est en version **_2.8_**.

Pour faire fonctionner la partie python du projet, vous aurez besoin de :
>**_Tensorflow 2.8_**
>>`pip install tensorflow==2.8.0`

>**_Numpy_**
>>`pip install numpy`

>IPython
>>`pip install IPython`

>Scipy
>>`pip install scipy`

## Compiler le plugin :

Assurez-vous que le [makefile](./Makefile) est correctement paramétré, c'est-à-dire:
- Vérifiez et possiblement changer la version et les emplacements des fichiers python.
    - Variable **_INC_** pour le dossier de votre **_Python/include_** 
    - Variable **_LIBS_** pour le path de votre **_python37.lib_** (regarder dans le dossier **_/libs_** de votre python)
- Vérifiez que le compilateur fonctionne (`g++ --version`). S'il n'est pas installé, vous pouvez suivre le tutoriel suivant pour Windows et VS Code : https://code.visualstudio.com/docs/languages/cpp ou juste installer msys2 (https://www.msys2.org/)

>`|Optionel|` Compilez le code au format exe et testez le:
>- run [**_makeExe.bat_**](./makeExe.bat) ou la commande `make TYPE=executable`
>- run **_PlugintTest.exe_**

Compilez le fichier dll
- run [**_makeDLL.bat_**](./makeDLL.bat) ou la commande `make TYPE=library`

Vous aurez maintenant le dll sous le nom **_ProjectPlugin.dll_**

## Utilisation du plugin

Pour l'instant, il n'est pas possible de charger le script python depuis l'editeur unity, donc il est préférable de placer le module [python](./python) directement dans le dossier au côté de l'exécutable.

- Rajoutez le plugin au dossier **_Assets/Plugins_** du projet unity (le créer s'il n'existe pas)
- Utilisez le script [**_RunProjectPlugin.cs_**](./RunProjectPlugin.cs) comme base
- Vérifiez que le script se fait bien charger, en lançant uniquement la fonction `TestPluginBase()` (retour console)
- si c'est le cas, décommanter la fonction `TestPluginPython()` et compiler le projet pour pouvoir le lancer hors de l'éditeur
- mettre le fichier [**_pyTest.py_**](./python/pyTest.py) dans un dossier python au coté de l'executable
- lancer le projet compilé et regarder si le champ de texte est correct (sensé renvoyer 10)
