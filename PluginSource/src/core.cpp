#include "pythonHelper.hpp"
#include "core.h"
#include <iostream>
#include <string>
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
       << ATestFunction(10, "python.pyTest");
  return 0;
}
float ExamplePluginFunction() { return 5.0F; }
int ATestFunction(int value, const char *pythonPath)
{
  CPyInstance pyInstance;
  CPyObject pName = PyUnicode_FromString(pythonPath); // use . instead of / and no need for ./
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

const char *TestIfPythonWorks()
{
  CPyInstance pyInstance;
  // PyRun_SimpleString("print('Hello World from Embedded Python!!!')");
  return "it works";
}
