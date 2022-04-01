#include "cpp/pythonHelper.hpp"

int main()
{
  CPyInstance pyInstance;

/*   FILE *pyScript = _Py_fopen("./python/pyTest.py", "r");
  PyRun_SimpleFile(pyScript, "./python/pyTest.py");

  FILE *tfScript = _Py_fopen("./python/main.py", "r");
  PyRun_SimpleFile(tfScript, "./python/main.py"); 
 */
  CPyObject pName = PyUnicode_FromString("python.main");
  CPyObject pModule = PyImport_Import(pName);

  if (pModule)
  {
    CPyObject pFunc = PyObject_GetAttrString(pModule, "predict");
    if (pFunc && PyCallable_Check(pFunc))
    {
      CPyObject pValue = PyObject_CallObject(pFunc, NULL);

      printf_s("C: predict() = %ld\n", PyLong_AsLong(pValue));
    }
    else
    {
      printf("ERROR: function predict()\n");
    }
  }
  else
  {
    printf_s("ERROR: Module not imported\n");
  }

  return 0;

  printf("\nPress any key to exit...\n");
  return 0;
}