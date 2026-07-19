param(
    [switch]$RealDataset,
    [int]$MaxSamplesPerSplit = 400
)
$ErrorActionPreference = "Stop"
& "$PSScriptRoot\one_click_windows.ps1" @PSBoundParameters
