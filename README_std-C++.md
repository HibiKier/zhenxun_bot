## _std::cout << "要不跑路吧" << std::endl;_
```
#include <bits/stdc++.h>
#include <run.h>
using namespace std;

template <class T>
bool runable(T &Any) {
    try {
        Any.run();
        return true;
    }
    catch (runtime_error &failure) {
        return false;
    }
}

int main(){
    runner me;
    pySrcCode code = ...;
    me.considerRun();
    
    if (!runable<runner> (me) && !runable<pySrcCode> (code)) {
        return 0;
    }
    
    me.set_destination("Cambodia");
    me.stowaway("boat");
    me.arrive();
    me.set_destination("Golden Triangle");
    ...
    return 0;
}
```
