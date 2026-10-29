# PowerShell Generator for Financial Literacy Dataset (500 records)
$csvPath = "C:\Users\noorjahan dalwai\.gemini\antigravity\scratch\financial-literacy-project\data\financial_literacy.csv"

$courses = @("B.Sc Data Science", "B.Sc Computer Science", "B.Com", "B.B.A", "B.A", "B.Tech", "B.Sc Mathematics")
$years = @("1st Year", "2nd Year", "3rd Year", "4th Year")
$expenseCategories = @("Food & Dining", "Travel & Commute", "Entertainment & Leisure", "Study Materials & Books", "Shopping & Fashion")
$budgetHabits = @("Never", "Rarely", "Occasionally", "Regularly")
$savingHabits = @("Does Not Save", "Saves Whatever is Left", "Saves a Fixed Percentage", "Invests Regularly")

$lines = [System.Collections.Generic.List[string]]::new()
$header = "Student_ID,Age_Group,Course,Year_of_Study,Financial_Education,Budgeting_Habit,Monthly_Expense_Category,Saving_Habit,Banking_Knowledge,Digital_Payment_Knowledge,Interest_Rate_Knowledge,Inflation_Knowledge,Loan_Knowledge,Investment_Knowledge,Risk_Awareness,Emergency_Fund_Awareness,Financial_Literacy_Score,Financial_Literacy_Level"
$lines.Add($header)

$rand = [System.Random]::new(42)

for ($i = 1; $i -le 500; $i++) {
    $id = ("STU{0:D4}" -f $i)
    $course = $courses[$rand.Next($courses.Length)]
    $year = $years[$rand.Next($years.Length)]
    
    if ($year -eq "1st Year") {
        $ageGroup = if ($rand.NextDouble() -lt 0.7) { "18-19" } else { "20-21" }
    } elseif ($year -eq "2nd Year") {
        $ageGroup = if ($rand.NextDouble() -lt 0.4) { "18-19" } else { "20-21" }
    } elseif ($year -eq "3rd Year") {
        $ageGroup = if ($rand.NextDouble() -lt 0.6) { "20-21" } else { "22-23" }
    } else {
        $ageGroup = if ($rand.NextDouble() -lt 0.5) { "22-23" } else { "24+" }
    }

    $finEduProb = 0.25
    if ($course -in @("B.Com", "B.B.A")) { $finEduProb = 0.65 }
    elseif ($course -in @("B.Sc Data Science", "B.Tech")) { $finEduProb = 0.40 }
    $finEdu = if ($rand.NextDouble() -lt $finEduProb) { "Yes" } else { "No" }

    $baseBoost = if ($finEdu -eq "Yes") { 0.15 } else { 0.0 }
    $yearBoost = switch ($year) {
        "1st Year" { 0.00 }
        "2nd Year" { 0.08 }
        "3rd Year" { 0.15 }
        "4th Year" { 0.22 }
    }

    $pBanking = [Math]::Min(0.95, 0.70 + $baseBoost + $yearBoost)
    $pDigital = [Math]::Min(0.98, 0.85 + ($baseBoost * 0.5) + ($yearBoost * 0.5))
    $pInterest = [Math]::Min(0.85, 0.35 + $baseBoost + $yearBoost)
    $pInflation = [Math]::Min(0.80, 0.30 + $baseBoost + $yearBoost)
    $pLoans = [Math]::Min(0.80, 0.38 + $baseBoost + $yearBoost)
    $pInvest = [Math]::Min(0.75, 0.28 + $baseBoost + $yearBoost)
    $pRisk = [Math]::Min(0.82, 0.42 + $baseBoost + $yearBoost)
    $pEmergency = [Math]::Min(0.78, 0.35 + $baseBoost + $yearBoost)

    $kBanking = if ($rand.NextDouble() -lt $pBanking) { 1 } else { 0 }
    $kDigital = if ($rand.NextDouble() -lt $pDigital) { 1 } else { 0 }
    $kInterest = if ($rand.NextDouble() -lt $pInterest) { 1 } else { 0 }
    $kInflation = if ($rand.NextDouble() -lt $pInflation) { 1 } else { 0 }
    $kLoans = if ($rand.NextDouble() -lt $pLoans) { 1 } else { 0 }
    $kInvest = if ($rand.NextDouble() -lt $pInvest) { 1 } else { 0 }
    $kRisk = if ($rand.NextDouble() -lt $pRisk) { 1 } else { 0 }
    $kEmergency = if ($rand.NextDouble() -lt $pEmergency) { 1 } else { 0 }

    if ($finEdu -eq "Yes" -and ($kBanking + $kInvest -ge 1)) {
        $budgetHabit = if ($rand.NextDouble() -lt 0.35) { "Regularly" } elseif ($rand.NextDouble() -lt 0.70) { "Occasionally" } elseif ($rand.NextDouble() -lt 0.90) { "Rarely" } else { "Never" }
        $savingHabit = if ($rand.NextDouble() -lt 0.25) { "Invests Regularly" } elseif ($rand.NextDouble() -lt 0.65) { "Saves a Fixed Percentage" } elseif ($rand.NextDouble() -lt 0.95) { "Saves Whatever is Left" } else { "Does Not Save" }
    } else {
        $budgetHabit = if ($rand.NextDouble() -lt 0.10) { "Regularly" } elseif ($rand.NextDouble() -lt 0.30) { "Occasionally" } elseif ($rand.NextDouble() -lt 0.65) { "Rarely" } else { "Never" }
        $savingHabit = if ($rand.NextDouble() -lt 0.05) { "Invests Regularly" } elseif ($rand.NextDouble() -lt 0.25) { "Saves a Fixed Percentage" } elseif ($rand.NextDouble() -lt 0.70) { "Saves Whatever is Left" } else { "Does Not Save" }
    }

    $expenseCat = $expenseCategories[$rand.Next($expenseCategories.Length)]

    $rawScore = $kBanking + $kDigital + $kInterest + $kInflation + $kLoans + $kInvest + $kRisk + $kEmergency
    $scorePct = [Math]::Round(($rawScore / 8.0) * 100, 1)

    $level = if ($scorePct -lt 50.0) { "Basic" } elseif ($scorePct -le 75.0) { "Intermediate" } else { "Advanced" }

    $row = "$id,$ageGroup,$course,$year,$finEdu,$budgetHabit,$expenseCat,$savingHabit,$kBanking,$kDigital,$kInterest,$kInflation,$kLoans,$kInvest,$kRisk,$kEmergency,$scorePct,$level"
    $lines.Add($row)
}

[System.IO.File]::WriteAllLines($csvPath, $lines)
Write-Output "Successfully generated 500 records in $csvPath"

