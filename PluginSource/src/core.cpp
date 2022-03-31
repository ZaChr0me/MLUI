#include "pythonHelper.hpp"
#include "core.h"
#include <iostream>
#include <string>
#include <stdexcept>
using namespace std;
/*
 * use const char* for c# strings
 *
 *
 *
 *
 *
 */

int main()
{

  cout << "it should output 20 if everything is working :\n"
       << ATestFunction(10);
  return 0;
}
float ExamplePluginFunction() { return 5.0F; }
int ATestFunction(int value)
{
  CPyInstance pyInstance;

  CPyObject pName = PyUnicode_FromString("python.pyTest"); // use . instead of / and no need for ./
  CPyObject pModule = PyImport_Import(pName);

  // set value
  CPyObject pVal;
  pVal = PyLong_FromLong(value);

  // create argument
  CPyObject pArgs;
  pArgs = PyTuple_New(1);
  PyTuple_SetItem(pArgs, 0, pVal);

  // get function ang call it with arguments
  CPyObject pFunc = PyObject_GetAttrString(pModule, "getInteger");
  CPyObject pValue = PyObject_CallObject(pFunc, pArgs);
  return PyLong_AsLong(pValue);
}
// TODO implement script load check to return false if failed
// THe sourceString is used here to indicate the path of the script
bool ScriptLoadExample(const unsigned char *sourceString,
                       int sourceStringLength,
                       int returnStringMaxLength)
{
  CPyInstance pyInstance;
  const char *path = reinterpret_cast<const char *>(sourceString);
  CPyObject pName = PyUnicode_FromString(path); // use . instead of / and no need for ./
  CPyObject pModule = PyImport_Import(pName);
  if (sourceStringLength > 0)
  {
  }
  if (returnStringMaxLength > 0)
  {
  }

  // set value
  CPyObject pVal;
  pVal = PyLong_FromLong(50);

  // create argument
  CPyObject pArgs;
  pArgs = PyTuple_New(1);
  PyTuple_SetItem(pArgs, 0, pVal);

  // get function ang call it with arguments
  CPyObject pFunc = PyObject_GetAttrString(pModule, "getInteger");
  pVal = PyObject_CallObject(pFunc, pArgs);
  string rString = "print('if pyTest was loaded successfully, the following value should be 100 : " + to_string(PyLong_AsLong(pVal)) + "')";
  PyRun_SimpleString(rString.c_str());

  return true;
}

void TestIfPythonWorks()
{
  Py_InitializeEx(0);
  PyRun_SimpleString("print('Hello World from Embedded Python!!!')");
  Py_Finalize();
}
