#include <iostream>
#define fort(i, a, b) for(int i = (a); i <= (b); i++)
#define forl(i, a, b) for(int i = (a); i >= (b); i--)
using namespace std;

typedef unsigned long long ll;

const int maxn = 2e5+2;
int m,n,k;
ll a[maxn], _a[maxn], res;

void nhap() {
    cin>>n>>m>>k;
    fort(i, 1, n) cin>>a[i];
}

int x[12];

void tohop(int i, int lastvt) {
    if (i > m) {
        ll s = 0;
        fort(j,1,n) _a[j]=a[j];
        fort(j,1,m) _a[x[j]] *= k;
        fort(j,1,n) s |= _a[j];
        res = max(res,s);
        return;
    }
    fort(j,lastvt,n) {
        x[i] = j;
        tohop(i+1, j);
    }
}

void xl() {
    nhap();
    
    x[m+1] = n+1;
    tohop(1, 1);
    cout<<res;
}

int main(int argc, const char * argv[]) {
    ios::sync_with_stdio(false);
    xl();
}