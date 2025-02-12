#include <iostream>
#include <limits>

int add(int a, int b) {
    if((b>0 && a> std::numeric_limits<int>::max()-b) || (b<0 && a<std::numeric_limits<int>::min()-b)) 
    {
        return 0; //overflow detected
    }
    return a + b;
}

int main() {
    int x,y;
    std::cout << "Enter the first integer (x): ";
    std::cin >> x;
    std::cout << "Enter the second integer (y): ";
    std::cin >> y;
    int result = add(x, y);  
    std::cout << "Result: " << result << std::endl;
    return 0;
}
