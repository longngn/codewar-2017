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

const int maxn = 5005;

int n, a[maxn], f[maxn], m;

void nhap() {
    cin>>n>>m;
    double coord;
    fort(i,1,n) cin>>a[i]>>coord;
}

void xl() {
    nhap();

    fort(i,1,n)
        fort(j,0,i-1) if (a[j] <= a[i]) f[i] = max(f[i], f[j] + 1);

    int fMax = 0;
    fort(i,1,n) fMax = max(fMax, f[i]);

    cout<<n - fMax;
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
