#include "cpp/pythonHelper.cpp"

int main()
{
  CPyInstance pyInstance;

  FILE *pyScript = _Py_fopen("./python/pyTest.py", "r");
  PyRun_SimpleFile(pyScript, "./python/pyTest.py");

  printf("\nPress any key to exit...\n");
  return 0;
}