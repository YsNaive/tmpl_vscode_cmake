#include <iostream>
#include "mypackage/mypackage.h"

int main(int argc, char* argv[]) {
    std::string name = "World";
    if (argc > 1) {
        name = argv[1];
    }

    mypackage::Greeter greeter(name);
    std::cout << greeter.greet() << std::endl;

#ifdef NDEBUG
    std::cout << "Release Build" << std::endl;
#else
    std::cout << "Debug Build" << std::endl;
#endif

    return 0;
}
