COMPILER = g++
CFLAGS = -std=c++17 -mtune=k8 -m64 -Wall -pedantic -Wall -Wextra -Werror -Wshadow -Wconversion -Wunreachable-code -s
COMPILE = $(COMPILER) $(CFLAGS)
INC = -IC:\\Python310\\include
LIBS = C:\\Python310\\libs\\python310.lib
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