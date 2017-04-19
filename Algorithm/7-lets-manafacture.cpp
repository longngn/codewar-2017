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

const int maxn = 1e5 + 2;
int n;
struct Block {
    int in, out, h;
} a[maxn];
ll f[maxn], t[maxn * 2];
int m = 0;

void nhap() {
    cin>>n;
    fort(i,1,n) cin>>a[i].in>>a[i].out>>a[i].h;
}

bool cmp(Block a, Block b) {
    return a.out == b.out ? a.in > b.in : a.out > b.out;
}

void update(int i, ll v) {
    while (i <= m) {
        t[i] = max(t[i], v);
        i += (i & -i);
    }
}

ll get(int i) {
    ll res = 0;
    while (i > 0) {
        res = max(res, t[i]);
        i -= (i & -i);
    }
    return res;
}

void xl() {
    nhap();
    sort(a+1, a+n+1, cmp);
    
    f[0] = 0;
    
    map<int, int> ax;
    fort(i,1,n) ax[a[i].in] = 0, ax[a[i].out - 1] = 0;
    forc(it, ax) it->second = ++m;
    
    fort(i,1,n) {
        f[i] = get(ax[a[i].out - 1]) + a[i].h;
        update(ax[a[i].in], f[i]);
    }
    
    ll res = 0;
    fort(i,1,n) res = max(res, f[i]);
    
    cout<<res;
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