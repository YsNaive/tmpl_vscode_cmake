#pragma once

#include <string>

namespace mypackage {

class Greeter {
public:
    Greeter(const std::string& name);
    std::string greet() const;

private:
    std::string name_;
};

} // namespace mypackage
