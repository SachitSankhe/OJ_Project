#include <iostream>
using namespace std;

int main()
{
    int t;
    cin >> t;
    while (t > 0)
    {
        int first_number, second_number, sum;

        cin >> first_number >> second_number;

        // sum of two numbers in stored in variable sumOfTwoNumbers
        if (second_number == 0)
        {
            cout << "NOT DIVISIBLE" << endl;
        }
        else
        {
            sum = first_number / second_number;
            cout << sum << endl;
        }

        // prints sum
        t--;
    }
    return 0;
}