extern "C"
{
  __declspec(dllexport) float __stdcall ExamplePluginFunction();
  __declspec(dllexport) int __stdcall ATestFunction(int value, const char *pythonPath);
  __declspec(dllexport) const char *__stdcall TestIfPythonWorks();
}