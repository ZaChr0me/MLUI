COMPILER = g++
CFLAGS = -std=c++17 -mtune=k8 -m64 -Wall -pedantic -Wall -Wextra -Wshadow -Wconversion -Wunreachable-code -s -Wl,--whole-archive
COMPILE = $(COMPILER) $(CFLAGS)
INC = -Wl,--whole-archive -IC:\\Users\\souli\\AppData\\Local\\Programs\\Python\\Python37\\include
LIBS = C:\\Users\\souli\\AppData\\Local\\Programs\\Python\\Python37\\libs/python37.lib -Wl,--no-whole-archive
IL = $(INC) $(LIBS)

#naming vars
TYPE=executable
NAME=PluginTest
BUILD=build
.PHONY: all clean

All: build $(TYPE) clean 

executable:
	$(COMPILE) -o $(NAME) -g src/core.cpp $(IL)


library: core 
	$(COMPILE) -shared -v -o $(NAME) $(BUILD)/core.o $(IL)

core:
	$(COMPILE) -c src/core.cpp -o $(BUILD)/core.o $(IL)

build:
	mkdir -p $(BUILD)

clean: 
	rm build -r