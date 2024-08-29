$filePath = "C:\Users\(username)\Desktop\DrivesSerialNumbers.txt"
$date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$drives = Get-WmiObject -Class Win32_PhysicalMedia
$serialNumbers = @()
foreach ($drive in $drives) {
    $serialNumbers += "$date - Serial Number: $($drive.SerialNumber)"
}
$serialNumbers | Add-Content -Path $filePath
Write-Output "Serial numbers have been appended to $filePath"

