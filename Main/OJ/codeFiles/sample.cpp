#include <iostream>
using namespace std;

int main() {
  int t;
  cin >> t;
  while (t>0)
  {
    int first_number, second_number, sum;
    
  cin >> first_number >> second_number;

  // sum of two numbers in stored in variable sumOfTwoNumbers
  sum = first_number + second_number;

  // prints sum 
  cout << sum <<endl;
  t--;
  }   
  return 0;
}