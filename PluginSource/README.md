#WIP

pour compiler le plugin :

- s'assurer que le makefile est parametré, c'est à dire
- checker et possiblement changer la version et les emplacements des fichiers python
- checker que le compilateur fonctionne (`g++ --version`).S'il n'est pas installé, suivre le tutoriel suivant pour windows et vs code : https://code.visualstudio.com/docs/languages/cpp ou juste installer msys2 (https://www.msys2.org/)
- |optionel| run **_makeExe.bat_** ou la commande `make TYPE=executable`
- |optionel| run **_PlugintTest.exe_**
- run **_makeDLL.bat_** ou la commande `make TYPE=library`

vous aurez maintenant le dll sous le nom **_ProjectPlugin.dll_**

pour utiliser le plugin :  
pour l'instant, il n'est pas possible de charger le script python dans l'editeur unity, donc il est préférable de compiler et de placer le pyTest directement dans le dossier au coté de l'executable.

- rajouter le plugin au dossier **_Assets/Plugins_** du projet unity (le créer s'il n'existe pas)
- utiliser le script **_RunProjectPlugin.cs_**
- vérifiez que le script se fait bien charger, en
