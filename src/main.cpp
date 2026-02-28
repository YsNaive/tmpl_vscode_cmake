#include <iostream>
#include "foo.h"
int main(int argc, char* argv[]) {
    std::cout << "Hello, CMake!" << std::endl;
    
    foo f;
    f.say_hello();

    return 0;
}
