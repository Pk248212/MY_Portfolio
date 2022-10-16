#include<bits/stdc++.h>
#include<string>
#define ll long long
#define repi(i,a,b) for(ll i=a;i<=b;i++)
#define repd(i,a,b) for(ll i=a;i>=b;i--)
#define FASTIO(); ios::sync_with_stdio(0); cin.tie(0);
#define cy cout<<"YES\n"
#define cn cout<<"NO\n"
#define MOD 1000000001
#define vi vector<int>
#define vl vector<ll>
#define pb push_back
#define pf push_front
#define popb pop_back
#define popf pop_front
#define ff first
#define ss second
#define nl cout<<"\n"
#define cm cout<<"-1\n"

using namespace std;

int main(){
    ll t=1;
    cin>>t;
    while(t--){
        ll n;
        cin>>n;
        if(n<4 || n%2==1)cm;
        else if(n==4)cout<<"1 1\n";
        else{
            ll mnm=n/6;
            ll mxm=n/4;
            if(n%6!=0)mnm++;
            cout<<mnm<<" "<<mxm; nl;
/*
            if(n%6==0){
                mnm=n/6;
                mxm=n/4;
            }
            else if(n%4==0){
                mnm++;
            }
            else{

            }*/
        }
    }
    return 0;
}
