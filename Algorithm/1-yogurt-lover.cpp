#include <iostream>
using namespace std;

long long n, a, b, c;
long long res;

long long cacu_res()
{
    long long ans=0;
    if (a<=b-c) ans=n/a;
    else
    {
        long long tmp=0;
        while (n/b>0)
        {
            tmp=n/b;
            ans+=tmp;
            n=n%b+tmp*c;
        }
    }
    return ans;
}

int main()
{
    cin >> n >> a >> b >> c;
    res=cacu_res();
    cout << res;
}