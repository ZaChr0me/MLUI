# This is a sample Python script.
# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
print(sys.path)
sys.path.append(r"C:\Users\souli\Documents\Travail\EFREI\M2\PFE\MLUI\PluginSource")
print(sys.path)

from python import AiDemo

def predict():
    return AiDemo.play()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    predict()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
