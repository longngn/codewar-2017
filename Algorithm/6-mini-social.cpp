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

const int maxn = 1e6+2;
const ll oo = 1e18;

int n, a[maxn];
ll f[maxn];

void nhap() {
    cin>>n;
    fort(i,1,n) cin>>a[i];
}

void xl() {
    nhap();

    ll ma1 = -oo, ma2 = -oo;
    fort(i,1,n) {
        ma1 = max(ma1, f[i-1] + a[i]);
        ma2 = max(ma2, f[i-1] - a[i]);
        f[i] = max(f[i], max(ma1 - a[i], ma2 + a[i]));
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
