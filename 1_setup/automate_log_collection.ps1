param(
    [Parameter(Mandatory = $true)]
    [string[]]$TestIds # Accepts an array of Atomic Red Team Test ID as an input parameter
)

foreach ($TestId in $TestIds) {
    # Get the last event timestamp before running the attack
    $lastEvent = Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" -MaxEvents 1 | Select-Object TimeCreated
    $startTime = $lastEvent.TimeCreated

    # Run Atomic Red Team Test
    Invoke-AtomicTest $TestId

    # Fetch Sysmon logs generated after running the test
    $sysmonLogs = Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" | Where-Object { $_.TimeCreated -gt $startTime }

    # Extract and display detailed information from each log
    $detailedLogs = $sysmonLogs | ForEach-Object {
        $xml = [xml]$_.ToXml()
        [PSCustomObject]@{
            TimeCreated       = $_.TimeCreated
            EventId           = $_.Id
            ProcessId         = $xml.Event.EventData.Data | Where-Object { $_.Name -eq "ProcessId" } | Select-Object -ExpandProperty '#text'
            ParentProcessId   = $xml.Event.EventData.Data | Where-Object { $_.Name -eq "ParentProcessId" } | Select-Object -ExpandProperty '#text'
            CommandLine       = $xml.Event.EventData.Data | Where-Object { $_.Name -eq "CommandLine" } | Select-Object -ExpandProperty '#text'
            ParentCommandLine = $xml.Event.EventData.Data | Where-Object { $_.Name -eq "ParentCommandLine" } | Select-Object -ExpandProperty '#text'
            Image             = $xml.Event.EventData.Data | Where-Object { $_.Name -eq "Image" } | Select-Object -ExpandProperty '#text'
            ParentImage       = $xml.Event.EventData.Data | Where-Object { $_.Name -eq "ParentImage" } | Select-Object -ExpandProperty '#text'
            CurrentDirectory  = $xml.Event.EventData.Data | Where-Object { $_.Name -eq "CurrentDirectory" } | Select-Object -ExpandProperty '#text'
            Hashes            = $xml.Event.EventData.Data | Where-Object { $_.Name -eq "Hashes" } | Select-Object -ExpandProperty '#text'
            User              = $xml.Event.EventData.Data | Where-Object { $_.Name -eq "User" } | Select-Object -ExpandProperty '#text'
            IntegrityLevel    = $xml.Event.EventData.Data | Where-Object { $_.Name -eq "IntegrityLevel" } | Select-Object -ExpandProperty '#text'
        }
    }

    # Define output CSV file path
    $outputPath = "C:\\Users\\bazinga\\Documents\\SecureSLM\\Run4\\${TestId}.csv"

    # Export the detailed logs to CSV
    $detailedLogs | Export-Csv -Path $outputPath -NoTypeInformation

    # Display success message
    Write-Host "Logs have been successfully exported to $outputPath"
}
