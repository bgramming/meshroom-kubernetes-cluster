# Download Dependencies Script - Clean Version
# Downloads required Docker images for Meshroom

Write-Host "Downloading Meshroom Dependencies..." -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green

$images = @(
    "alicevision/meshroom:latest",
    "alicevision/alicevision:latest",
    "hello-world"
)

foreach ($image in $images) {
    Write-Host "Downloading: $image" -ForegroundColor Cyan
    try {
        docker pull $image
        Write-Host "  Success: $image" -ForegroundColor Green
    } catch {
        Write-Host "  Failed: $image - $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Download complete!" -ForegroundColor Green
Write-Host "Available images:" -ForegroundColor Cyan
docker images
