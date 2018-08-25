$content = @{
    __post__=1
    content='first post'
}
$json = $content | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:8000 -Method Post -Body $json -ContentType 'application/json'