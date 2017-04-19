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

map<string, int> score, numberOfMatches, goals, goalDiff;

void nhap() {
    fort(i,1,5) {
        string team1, team2;
        char colon;
        int goal1, goal2;
        cin>>team1>>team2>>goal1>>colon>>goal2;
        if (goal1 > goal2) score[team1] += 3, score[team2] += 0;
        else if (goal1 < goal2) score[team1] += 0, score[team2] += 3;
        else score[team1]++, score[team2]++;
        
        numberOfMatches[team1]++, numberOfMatches[team2]++;
        goals[team1] += goal1, goals[team2] += goal2;
        goalDiff[team1] += goal1 - goal2, goalDiff[team2] += goal2 - goal1;
    }
}

bool cmp(string team1, string team2) {
    if (score[team1] > score[team2]) return true;
    else if (score[team1] < score[team2]) return false;
    if (goalDiff[team1] > goalDiff[team2]) return true;
    else if (goalDiff[team1] < goalDiff[team2]) return false;
    if (goals[team1] > goals[team2]) return true;
    else if (goals[team1] < goals[team2]) return false;
    return team1 < team2;
}

void xl() {
    nhap();
    
    string vTeam = "VIETNAM", oTeam;
    forc(it, numberOfMatches) if (it->first != "VIETNAM" && it->second < 3) oTeam = it->first;
    vector<string> teams;
    forc(it, score) teams.pb(it->first);
    
    prii res(-1,-1);

    fort(oGoal, 0, 100) fort(vGoal, oGoal + 1, 101) {
        int vScore, oScore;
        if (vGoal > oGoal) vScore = 3, oScore = 0;
        else if (vGoal < oGoal) vScore = 0, oScore = 3;
        else vScore = oScore = 1;
        score[vTeam] += vScore, score[oTeam] += oScore;
        goals[vTeam] += vGoal, goals[oTeam] += oGoal;
        goalDiff[vTeam] += vGoal - oGoal, goalDiff[oTeam] += oGoal - vGoal;
        
        sort(teams.begin(), teams.end(), cmp);
        if (teams[0] == "VIETNAM" || teams[1] == "VIETNAM")
            if (res.first == -1 or vGoal - oGoal < res.first - res.second)
                res = mp(vGoal, oGoal);
        
        score[vTeam] -= vScore, score[oTeam] -= oScore;
        goals[vTeam] -= vGoal, goals[oTeam] -= oGoal;
        goalDiff[vTeam] -= vGoal - oGoal, goalDiff[oTeam] -= oGoal - vGoal;
    }
    
    if (res.first == -1) cout<<"IMPOSSIBLE";
    else cout<<res.first<<':'<<res.second;
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
