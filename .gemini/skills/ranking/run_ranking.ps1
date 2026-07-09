# Run ranking over simulation outputs and persist CSV to assets/ranking_results.csv
$simDir = ".github\skills\simulation\simulations"
$outCsv = ".github\skills\ranking\assets\ranking_results.csv"

$files = Get-ChildItem -Path $simDir -Filter *.md -ErrorAction Stop | Sort-Object Name
if ($files.Count -eq 0) {
    Write-Output "No simulation files found in $simDir"
    exit 1
}

$rows = @()
foreach ($f in $files) {
    $text = Get-Content -Path $f.FullName -Raw
    $meta = @{Company='Unknown';Title='Unknown';Posting='Unknown';Comp='Unknown';Loc='Unknown';Years='Unknown';Degree='Unknown'}
    $m = [regex]::Match($text, '## 0. Metadata[\s\S]*?---')
    if ($m.Success) {
        $block = $m.Value
        foreach ($line in $block -split "`n") {
            if ($line -match "- Company:\s*(.+)") { $meta.Company = $Matches[1].Trim() }
            if ($line -match "- Job Title:\s*(.+)") { $meta.Title = $Matches[1].Trim() }
            if ($line -match "- Posting Date:\s*(.+)") { $meta.Posting = $Matches[1].Trim() }
            if ($line -match "- Compensation:\s*(.+)") { $meta.Comp = $Matches[1].Trim() }
            if ($line -match "- Location\(s\):\s*(.+)") { $meta.Loc = $Matches[1].Trim() }
            if ($line -match "- Years of Experience Required:\s*(.+)") { $meta.Years = $Matches[1].Trim() }
            if ($line -match "- Degree Requirement:\s*(.+)") { $meta.Degree = $Matches[1].Trim() }
        }
    }

    $re = [regex]::Match($text, '\*\*Recruiter Screen Likelihood:\*\*\s*(\d+)%')
    $int = [regex]::Match($text, '\*\*Interview Likelihood:\*\*\s*(\d+)%')
    $recruiter = if ($re.Success) { [int]$re.Groups[1].Value } else { 50 }
    $interview = if ($int.Success) { [int]$int.Groups[1].Value } else { 50 }

    # degree score
    $deg = 0.5
    if ($meta.Degree -match 'Bachelor|Master|PhD') { $deg = 1 }
    elseif ($meta.Degree -match 'High School') { $deg = 0.2 }

    # skill score
    $direct = ([regex]::Matches($text, '\|[^\n]*\|\s*Direct\b')).Count
    $partial = ([regex]::Matches($text, '\|[^\n]*\|\s*Partial\b')).Count
    $skill = 0.5
    if ($direct -ge 3) { $skill = 1 }
    elseif ($direct -ge 1 -and $partial -ge 1) { $skill = 0.75 }
    elseif ($partial -ge 1) { $skill = 0.6 }

    # experience score
    $exp = 0.5
    if ($meta.Years -match '\b\d\+') { $exp = 1 }
    elseif ($meta.Years -match '\b\d+\-\d+') { $exp = 0.8 }
    elseif ($meta.Years -match '1-2|1–2|2\+') { $exp = 0.7 }

    # fit
    $fitMatch = [regex]::Match($text, '## 8. Final Fit Summary[\s\S]*?\n\*\*Category:\*\*\s*(.+)')
    $fit = 0.5
    $fitCategory = "Unknown"
    if ($fitMatch.Success) {
        $c = $fitMatch.Groups[1].Value.Trim()
        $fitCategory = $c
        if ($c -match 'Strong') { $fit = 1 }
        elseif ($c -match 'Moderate') { $fit = 0.75 }
        elseif ($c -match 'Weak') { $fit = 0.4 }
        elseif ($c -match 'Mismatch|Hard') { $fit = 0.1 }
    }

    $pen = 0
    if ($text -match 'Major violation|major violation') { $pen = 30 }
    if ($text -match 'Minor violation') { $pen += 10 }

    $composite = ($recruiter * 0.45) + ($interview * 0.2) + ($deg * 100 * 0.15) + ($skill * 100 * 0.1) + ($exp * 100 * 0.05) + ($fit * 100 * 0.05) - $pen
    $composite = [math]::Round([math]::Max(0, [math]::Min(100,$composite)),2)

    $rows += [PSCustomObject]@{
        Role = $meta.Title
        Company = $meta.Company
        Compensation = $meta.Comp
        Location = $meta.Loc
        YearsRequired = $meta.Years
        Composite = $composite
        Recruiter = $recruiter
        Interview = $interview
        DegreeScore = $deg
        SkillScore = $skill
        ExperienceScore = $exp
        PrefPenalties = $pen
        FitScore = $fit
        FitCategory = $fitCategory
        FileName = $f.Name
        PostingDate = $meta.Posting
    }
}

$ranked = $rows | Sort-Object -Property @{Expression='Composite';Descending=$true}, @{Expression='Recruiter';Descending=$true}

# Add Rank column
$rank = 1
$exportRows = @()
foreach ($r in $ranked) {
    $exportRows += [PSCustomObject]@{
        Rank = $rank
        Role = $r.Role
        Company = $r.Company
        Compensation = $r.Compensation
        Location = $r.Location
        YearsRequired = $r.YearsRequired
        Composite = $r.Composite
        Recruiter = $r.Recruiter
        Interview = $r.Interview
        DegreeScore = $r.DegreeScore
        SkillScore = $r.SkillScore
        ExperienceScore = $r.ExperienceScore
        PrefPenalties = $r.PrefPenalties
        FitScore = $r.FitScore
        FitCategory = $r.FitCategory
        FileName = $r.FileName
        PostingDate = $r.PostingDate
    }
    $rank++
}

# Ensure assets directory exists
$assetsDir = Split-Path -Path $outCsv -Parent
if (-not (Test-Path $assetsDir)) { New-Item -ItemType Directory -Path $assetsDir -Force | Out-Null }

# Export CSV (overwrite)
$exportRows | Export-Csv -Path $outCsv -NoTypeInformation -Force -Encoding UTF8

Write-Output "Ranking persisted to $outCsv" 
