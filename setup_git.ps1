$gitDir = "$env:LOCALAPPDATA\Programs\Git"
New-Item -ItemType Directory -Force -Path $gitDir | Out-Null
$zip = "$env:TEMP\mingit.zip"

Write-Output "Downloading MinGit..."
Invoke-WebRequest -Uri "https://github.com/git-for-windows/git/releases/download/v2.47.1.windows.1/MinGit-2.47.1-64-bit.zip" -OutFile $zip

Write-Output "Extracting MinGit to $gitDir..."
Expand-Archive -Path $zip -DestinationPath $gitDir -Force

$gitExe = "$gitDir\cmd\git.exe"
if (Test-Path $gitExe) {
    Write-Output "MinGit successfully installed at: $gitExe"
    & $gitExe --version
} else {
    Write-Output "Extraction failed."
}
