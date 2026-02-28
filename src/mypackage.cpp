#include "mypackage/mypackage.h"

namespace mypackage {

Greeter::Greeter(const std::string& name) : name_(name) {}

std::string Greeter::greet() const {
    return "Hello, " + name_ + "!";
}

} // namespace mypackage
