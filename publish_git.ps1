$gitExe = "$env:LOCALAPPDATA\Programs\Git\cmd\git.exe"
$projectDir = "C:\Users\noorjahan dalwai\.gemini\antigravity\scratch\financial-literacy-project"

Set-Location $projectDir

Write-Output "1. Initializing Git Repository..."
& $gitExe init

Write-Output "2. Setting Git Author Config..."
& $gitExe config user.name "noorjahandalwai5-star"
& $gitExe config user.email "noorjahandalwai@users.noreply.github.com"

Write-Output "3. Staging project files..."
& $gitExe add .

Write-Output "4. Creating initial commit..."
& $gitExe commit -m "Initial commit: Financial Literacy Data Science & Machine Learning Analysis"

Write-Output "5. Renaming default branch to main..."
& $gitExe branch -M main

Write-Output "6. Configuring remote origin..."
$existingRemote = & $gitExe remote
if ($existingRemote -contains "origin") {
    & $gitExe remote set-url origin https://github.com/noorjahandalwai5-star/financial-literacy-analysis.git
} else {
    & $gitExe remote add origin https://github.com/noorjahandalwai5-star/financial-literacy-analysis.git
}

Write-Output "7. Repository local setup complete!"
& $gitExe status
