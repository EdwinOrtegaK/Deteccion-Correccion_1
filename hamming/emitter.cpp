#include <bits/stdc++.h>
using namespace std;

static bool isBinary(const string& s){
    return !s.empty() && all_of(s.begin(), s.end(), [](char c){ return c=='0'||c=='1'; });
}
static bool isPow2(int x){ return x && (x & -x) == x; }

int main(){
    ios::sync_with_stdio(false); 
    cin.tie(nullptr);

    cout << "Hamming (emisor C++). Ingrese mensaje binario (MSB->LSB): " << flush;
    string m;
    if(!(cin >> m)){ return 0; }
    if(!isBinary(m)){ cerr<<"Error: solo 0's y 1's\n"; return 1; }

    // Longitud de datos
    int md = (int)m.size();

    // Calcular r tal que 2^r >= m + r + 1
    int r = 0; while((1<<r) < md + r + 1) r++;
    int n = md + r;

    // Codeword 1-indexado
    vector<int> cw(n+1, 0);

    // Rellenar bits de datos en posiciones que NO son potencia de 2
    int j = md-1;
    for(int i=1;i<=n;i++){
        if(!isPow2(i)){
            cw[i] = (j>=0 ? (m[j]-'0') : 0);
            j--;
        }
    }

    // Calcular paridades
    for(int p=1; p<=n; p<<=1){
        int parity = 0;
        for(int i=1;i<=n;i++){
            if(i & p) parity ^= cw[i];
        }
        cw[p] = parity;
    }

    // Construir salida MSB->LSB
    string out; out.reserve(n);
    for(int i=n;i>=1;i--) out.push_back(char('0'+cw[i]));
    cout << "Codeword: " << out << "\n";
    return 0;
}
