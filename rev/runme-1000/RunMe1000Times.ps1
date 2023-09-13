### DON'T INSPECT THE SOURCE BEFORE RUNNING THE SCRIPT! THAT'S CHEATING ###

#printFlag  ***DEBUG***
function printFlag {
$EncodedText = 'VW5hYmxlIHRvIHByb2Nlc3MgeW91ciByZXF1ZXN0OiBQbGVhc2UgdHJ5IGFnYWlu'
$DecodedText = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($EncodedText))
"Decoded flag: $DecodedText"
}
#printFlag  ***DEBUG***


function LoadXml(){ 
	param(
		[Parameter(Mandatory=$true)][string]$XMLPath
		)
	try{
		$global:XmlDocument = [xml](Get-Content -Path $XMLPath)
		} catch {
	ErrorExit -message "Unable to open 'Important' .xml file"
	}
}


function updateRunCounter {
$counter = Get-Random -Maximum 1000
$winning = 'VGhvdXNhbmQ='

if ($XmlDocument.FlagFlagFlag.Counter -eq [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($winning))) {
$counter = 1000
}
Write-Host "Your lucky number is:" $counter
if($counter -eq 1000) {
    $signature = $XmlDocument.FlagFlagFlag.Signature
    $Except = $signature[-1..-$signature.Length] -join ''
    $DecodedText = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($Except))
        if($counter -eq 1000) {
            Write-Host Winning: $DecodedText
        }
    }
}

function checkXmlData {
$file = '.\CountCount.xml'

#If the file does not exist, create it.
if (-not(Test-Path -Path $file -PathType Leaf)) {
     try {
         $null = New-Item -ItemType File -Path $file -Force -ErrorAction Stop
         #Write-Host "The file [$file] has been created."
@"
        <FlagFlagFlag>
        <Counter>1</Counter>
        <Signature>Q1RGe01JU0NoaWVmTWFuYWdlZDEwMDB9</Signature>
        </FlagFlagFlag>
"@ | Set-Content $file -Encoding UTF8
     }
     catch {
         throw $_.Exception.Message
     }
 }
# If the file already exists, show the message and do nothing.
 else {
     #Write-Host "Everything failed. Please rerun the script"
 }
 }

checkXmlData
LoadXml .\CountCount.xml
updateRunCounter
#printFlag  ***DEBUG***