#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Build and publish ark-asa-parser to PyPI
.DESCRIPTION
    Cleans old builds, creates new distribution, and uploads to PyPI using your existing .pypirc
#>

param(
    [switch]$SkipBuild,
    [switch]$TestPyPI
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Publishing ark-asa-parser to PyPI" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Ensure we're in the right directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Check if build and twine are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
$buildInstalled = python -m pip list | Select-String "build"
$twineInstalled = python -m pip list | Select-String "twine"

if (-not $buildInstalled -or -not $twineInstalled) {
    Write-Host "Installing build tools..." -ForegroundColor Yellow
    python -m pip install --upgrade build twine
}

if (-not $SkipBuild) {
    # Clean old builds
    Write-Host "`nCleaning old builds..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue
    
    # Build package
    Write-Host "`nBuilding package..." -ForegroundColor Yellow
    python -m build
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`n❌ Build failed!" -ForegroundColor Red
        exit 1
    }
    
    # Check package
    Write-Host "`nChecking package..." -ForegroundColor Yellow
    twine check dist/*
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`n❌ Package check failed!" -ForegroundColor Red
        exit 1
    }
}

# Upload
Write-Host "`nUploading to PyPI..." -ForegroundColor Yellow
Write-Host "(Using your existing .pypirc configuration)`n" -ForegroundColor Gray

if ($TestPyPI) {
    twine upload --repository testpypi dist/*
}
else {
    twine upload dist/*
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "✅ Successfully published to PyPI!" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Green
    Write-Host "View at: https://pypi.org/project/ark-asa-parser/`n" -ForegroundColor Cyan
}
else {
    Write-Host "`n❌ Upload failed!" -ForegroundColor Red
    exit 1
}
