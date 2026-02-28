#include "foo.h"
#include <iostream>
void foo::say_hello() const
{
    std::cout << "Hello, foo!" << std::endl;
}