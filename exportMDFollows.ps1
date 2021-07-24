[CmdletBinding()]
param (
	[Parameter(Mandatory = $false, HelpMessage = 'Directory follow export should be placed')]
	[string]$OutputDir = "${env:UserProfile}/Desktop"
)

<#
	"Log user into MD"
#>
function Authenticate-User {
	try {
		# Prompt for username and password
		$credentials = Get-Credential;

		$headers = @{
			'accept'       = 'application/json';
			'content-type' = 'application/json'
		};

		# Authenticate
		$requestUri = "${baseUri}/auth/login";
		$requestBody = "{`"username`":`"$($credentials.UserName)`",`"password`":`"$($credentials.GetNetworkCredential().Password)`"}";
		$response = Invoke-WebRequest -Method Post -Headers $headers -Uri $requestUri -Body $requestBody;

		if ($response.StatusCode -ne 200) {
			throw "Failed to Authenticate:`nStatus Code: $($response.StatusCode)";
		}

		return ($response.Content | ConvertFrom-Json).token;
	}
	catch {
		throw"Authentication Failed`n$_";
	}
	finally {
		# Clean Up
		$credentials = $NULL;
		$requestBody = $NULL;
		$response = $NULL;
	}	
}

function Logout-User {
	param (
		$token
	)
	try {
		# Headers
		$headers = @{
			'accept'        = 'application/json';
			'content-type'  = 'application/json';
			'Authorization' = "Bearer $($token.Session)"
		};
		# Logout
		$requestUri = "${baseUri}/auth/logout";
		$response = Invoke-WebRequest -Method Post -Headers $headers -Uri $requestUri;

		if ($response.StatusCode -ne 200) {
			throw "Failed to logout:`nStatus Code: $($response.StatusCode)";
		}
	}
	catch {
		throw $_;
	}
	finally {
		$token = $NULL;
		$headers = $NULL;
	}
}

function Export-FollowData {
	param (
		$token
	)
	try {
		# Headers
		$headers = @{
			'accept'        = 'application/json';
			'content-type'  = 'application/json';
			'Authorization' = "Bearer $($token.Session)"
		};

		# Get Follows
		$limit = 50;
		$offset = 0;
		$resultCount = 0;
		$exportData = @{'follows' = @() };
		do {
			$requestUri = "${baseUri}/user/follows/manga?limit=${limit}&offset=${offset}";
			$response = Invoke-WebRequest -Method Get -Headers $headers -Uri $requestUri;
			Start-Sleep -Seconds 1; # Slow things down

			$results = ($response.Content | ConvertFrom-Json).results;
			$resultCount = $results.Count;

			foreach ($result in $results) {
				[string]$id = $result.data.id;
				[string]$title = $result.data.attributes.title.en;
				[array]$altTitles = ($result.data.attributes.altTitles | ForEach-Object { $_.en });
				# TODO: Fix alt titles

				$exportData.follows += @{'id' = $id; 'title' = $title; 'altTitles' = $altTitles };
			}
			$offset += $limit;
		}
		while ($resultCount -ge $limit)

		return $exportData
	}
	catch {
		throw $_;
	}
	finally {
		$token = $NULL;
		$headers = $NULL;
		$response = $NULL;
		$results = $NULL;
	}
	
}
# Base Uri
$baseUri = 'https://api.mangadex.org';

try {
	$token = Authenticate-User;
	
	Start-Sleep -Seconds 1; # Slow things down

	(Export-FollowData -token $token) | ConvertTo-Json | Out-File -FilePath "$OutputDir/mdexport.json";

	Logout-User -token $token;
}
catch {
	Write-Error $_;
}
finally {
	$token = $NULL;
}