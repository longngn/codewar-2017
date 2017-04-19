#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <algorithm>
#include <string>
#include <sstream>
#include <map>
#include <set>
#include <vector>
#include <cmath>
#include <utility>
#include <list>
#include <bitset>
#include <functional>
#include <cstring>

using namespace std;

#define pb push_back
#define mp make_pair
#define ins insert
#define ers erase
#define fort(i,a,b) for(int i=(a); i<=(b); i++)
#define forl(i,a,b) for(int i=(a); i>=(b); i--)
#define forc(i,c) for(typeof(c.begin()) i=c.begin(); i!=c.end(); i++)
#define forcn(i,c) for(typeof(c.rbegin()) i=c.rbegin(); i!=c.rend(); i++)

typedef long long ll;
typedef pair<int,int> prii;

const char* fi=".inp";
const char* fo=".out";

bool isPrime(int x) {
    if (x < 2) return false;
    if (x < 4) return true;
    fort(i,2,int(sqrt(x))) if (x % i == 0) return false;
    return true;
}

int get(int n, int ub) {
    int p = n + 1;
    if (!isPrime(p)) return -1;

    ll r; int t;
    forl(b, ub - 1, 2) if (b % p != 0) {
        r = 1, t = 0;
        do {
            t++;
            r = r * b % p;
        } while (r != 1);
        if (t == p - 1) return b;
    }
    return -1;
}

void xl() {
    int n, ub;
    cin>>n>>ub;
    cout<<get(n, ub);
}

int main()
{
#ifndef ONLINE_JUDGE
    //freopen(fi,"r",stdin);
    //freopen(fo,"w",stdout);
#endif
    ios::sync_with_stdio(false);
    xl();
}