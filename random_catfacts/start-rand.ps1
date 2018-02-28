# start-rand.ps1
$python="C:\Users\wboyerx\AppData\Local\Programs\Python\Python36\python.exe"
$MyPythonScript="C:\Users\wboyerx\Desktop\cat_facts.py"

while ($true) {
 $rnd = Get-Random -Minimum 360 -Maximum 2880

 Start-Sleep -Seconds $rnd

 & $python $MyPythonScript *>&1 >> "C:\Users\wboyerx\Desktop\cat_facts.log"
}