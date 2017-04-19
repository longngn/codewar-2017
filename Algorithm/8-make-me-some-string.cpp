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

const char* fi="manafacture.inp";
const char* fo="manafacture.out";

const int maxn = 1e7 + 2;
const ll oo = 1e18;

int n;
ll a,b,f[maxn*2];

void nhap() {
    cin>>n>>a>>b;
}

void xl() {
    nhap();

    fort(i,1,2*n) f[i] = oo;
    fort(i,1,n) {
        f[i] = min(f[i], min(f[i-1], f[i+1]) + a);
        f[i*2] = min(f[i*2], f[i] + b);
    }

    cout<<f[n];
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