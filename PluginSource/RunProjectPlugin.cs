using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.UI;
using UnityEditor;
using System.Runtime.InteropServices;
using System.Runtime;



public class NewBehaviourScript : MonoBehaviour
{
    [DllImport("ProjectPlugin", CharSet = CharSet.Unicode)]
    public static extern float ExamplePluginFunction();
    [DllImport("ProjectPlugin", CharSet = CharSet.Unicode)]
    public static extern void TestIfPythonWorks();
    [DllImport("ProjectPlugin", CharSet = CharSet.Unicode)]
    public static extern int ATestFunction(int value);
    [DllImport("ProjectPlugin", CharSet = CharSet.Unicode)]
    public static extern bool ScriptLoadExample([In] byte[] source, int sourceLength, int maxDestLength);

    public Text testText;
    // Start is called before the first frame update
    void Start()
    {
      TestPluginBase();
      TestPluginPython();
    }
    void TestPluginBase(){
      print(ExamplePluginFunction());
      TestIfPythonWorks();
    }
    void TestPluginPython(){
        int val = ATestFunction(5);
        testText.text = val.ToString();
        //byte[] s = System.Text.Encoding.ASCII.GetBytes("pyTest");
        //bool r = ScriptLoadExample(s, s.Length, 100);
        //print(r);
        //testText.text = (r) ? "true" : "false";
    }
}
