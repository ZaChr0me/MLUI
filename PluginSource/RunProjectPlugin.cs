//script pour Unity d'exemple pour voir comment charger et faire fonctionner le plugin
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.UI;
using UnityEditor;
using System.Runtime.InteropServices;



public class NewBehaviourScript : MonoBehaviour
{
    [DllImport("ProjectPlugin.dll")]
    private static extern float ExamplePluginFunction();
    [DllImport("ProjectPlugin.dll")]
    private static extern int ATestFunction(int val,string pythonScriptPath);

    // Start is called before the first frame update
    void Start()
    {
        print(ExamplePluginFunction());
    }
}
