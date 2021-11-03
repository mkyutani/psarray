# psarray

Python interface for Powershell script.

# class PSArray

## method build(powershell_script) returns array_of_hash

* Sample source using PSArray.

```
from PSArray import PSArray

powershell_script = 'get-service'

array = PSArray().build(powershell_script)
print(f'type: {type(array)}')
print(f'keys: {array[0].keys()}')
print(f'length: {len(array)}')
print(f'the first instance: {array[0]}')
print(f'the last instance: {array[-1]}')
```

* Result.

```
$ python3 ./a.py
type: <class 'list'>
keys: dict_keys(['Name', 'RequiredServices', 'CanPauseAndContinue', 'CanShutdown', 'CanStop', 'DisplayName', 'DependentServices', 'MachineName', 'ServiceName', 'ServicesDependedOn', 'ServiceHandle', 'Status', 'ServiceType', 'StartType', 'Site', 'Container'])
length: 302
the first instance: {'Name': 'AarSvc_5bf6d', 'RequiredServices': '{}', 'CanPauseAndContinue': 'False', 'CanShutdown': 'False', 'CanStop': 'True', 'DisplayName': 'AarSvc_5bf6d', 'DependentServices': '{}', 'MachineName': '.', 'ServiceName': 'AarSvc_5bf6d', 'ServicesDependedOn': '{}', 'ServiceHandle': 'SafeServiceHandle', 'Status': 'Running', 'ServiceType': '240', 'StartType': 'Manual', 'Site': '', 'Container': ''}
the last instance: {'Name': 'ZeroConfigService', 'RequiredServices': '{RPCSS}', 'CanPauseAndContinue': 'False', 'CanShutdown': 'False', 'CanStop': 'True', 'DisplayName': 'Intel(R) PROSet/Wireless Zero Configuration Service', 'DependentServices': '{}', 'MachineName': '.', 'ServiceName': 'ZeroConfigService', 'ServicesDependedOn': '{RPCSS}', 'ServiceHandle': 'SafeServiceHandle', 'Status': 'Running', 'ServiceType': 'Win32OwnProcess', 'StartType': 'Automatic', 'Site': '', 'Container': ''}
```
* This is one liner enumerating your Windows Tasks like startup tab of task manager.

```
$ python3 main.py '$r = @(); $ns = "\Software\"; $nw = "Microsoft\Windows\CurrentVersion\"; $nr = $nw + "Run"; $ne = ":" + $ns + $nw + "Explorer\StartupApproved\*"; $nm = "HKLM:" + $ns; $nc = "HKCU:" + $ns; $l = @("User", "System", "WoW"); $e = @($nc, $nm, ($nm + "Wow6432Node\")); $f = @("", "common "); foreach ($i in 0..2) { $k = get-item ($e[$i] + $nr); $k.getvaluenames() |%{ $r += [pscustomobject]@{ l = "Run:" + $l[$i]; n = $_; c = $k.getvalue($_) }}}; foreach ($i in 0..1) { ((new-object -com shell.application).namespace("shell:" + $f[$i] + "startup").items() |%{ $r += [pscustomobject]@{ l = "Startup:" + $l[$i]; n = $_.name; c = $_.path }})}; $x = get-itemproperty ("HKLM" + $ne), ("HKCU" + $ne); $nuwp = ($r |? c -ne "" |%{ $o = [pscustomobject]@{ location = $_.l; name = $_.n; disabled = 0; command = $_.c; path = $null }; $x |%{ $p = $_.PSPath; $_ | get-member -type noteproperty |? name -eq $o.name |%{ $v = get-itempropertyvalue $p -name $o.name; $o.path = $p; $o.disabled = $v[0] -band 1 }}; $o }); $uwp = (get-appxpackage |% { try { $x = $_; $t = (get-appxpackagemanifest $_).package.applications.application.extensions.extension |? category -like "*.startuptask"; if ($t -ne $null) { $p = $nc + "Classes\Local Settings" + $ns + $nw + "AppModel\SystemAppData\" + $x.packagefamilyname + "\" + $t.startuptask.taskid; $s = (get-item $p).getvalue("state"); $o = [pscustomobject]@{ location = "UWP"; name = $x.name; disabled = $s -band 1; command = $x.installlocation + "\" + $t.executable; path = $p}; $o }}catch{}}); $nuwp+$uwp'
```
