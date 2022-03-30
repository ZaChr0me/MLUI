#WIP

pour compiler le plugin :

- s'assurer que le makefile est parametré, c'est à dire
- checker et possiblement changer la version et les emplacements des fichiers python
- checker que le compilateur fonctionne (`g++ --version`).S'il n'est pas installé, suivre le tutoriel suivant pour windows et vs code : https://code.visualstudio.com/docs/languages/cpp ou juste installer msys2 (https://www.msys2.org/)
- |optionel| run **_makeExe.bat_** ou la commande `make TYPE=executable`
- |optionel| run **_PlugintTest.exe_**
- run **_makeDLL.bat_** ou la commande `make TYPE=library`

vous aurez maintenant le dll sous le nom **_ProjectPlugin.dll_**
