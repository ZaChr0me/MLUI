extern "C"
{
  __declspec(dllexport) float __stdcall ExamplePluginFunction();
  __declspec(dllexport) int __stdcall ATestFunction(int value);
  __declspec(dllexport) bool __stdcall ScriptLoadExample(const unsigned char *sourceString,
                                                         int sourceStringLength,
                                                         int returnStringMaxLength);
  __declspec(dllexport) void __stdcall TestIfPythonWorks();
}