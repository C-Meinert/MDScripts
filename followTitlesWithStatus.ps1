<#
	"Log user into MD"
#>
function Login-User {
    try {
        # Prompt for username and password
        $credentials = Get-Credential;

        $headers = @{
            'accept'       = 'application/json';
            'content-type' = 'application/json'
        };

        # Authenticate
        $requestUri = "${script:baseUri}/auth/login";
        $requestBody = "{`"username`":`"$($credentials.UserName)`",`"password`":`"$($credentials.GetNetworkCredential().Password)`"}";
        $response = Invoke-WebRequest -Method Post -Headers $headers -Uri $requestUri -Body $requestBody;

        if ($response.StatusCode -ne 200) {
            throw "Failed to Authenticate:`nStatus Code: $($response.StatusCode)";
        }

        Start-Sleep -Seconds 1; # Slow things down
        return ($response.Content | ConvertFrom-Json).token;
    }
    catch {
        throw "Authentication Failed`n$_";
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
        $requestUri = "${script:baseUri}/auth/logout";
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

function Get-MangaStatus {
    param (
        [Parameter(Mandatory = $true)]
        [ValidateNotNull]
        $token,
        [ValidateSet('all', 'reading', 'on_hold', 'plan_to_read', 'completed', 'dropped', 're_reading')]
        [string]$status = 'all'
    )
    try {
        # Headers
        $headers = @{
            'accept'        = 'application/json';
            'content-type'  = 'application/json';
            'Authorization' = "Bearer $($token.Session)"
        };
        $requestUri = "${script:baseUri}/manga/status";
        $response = Invoke-WebRequest -Method Get -Headers $headers -Uri $requestUri;

        Start-Sleep -Seconds 1; # Slow things down
        return $response.statuses;
    }
    catch {
        throw $_;
    }
    finally {
        $token = $NULL;
        $headers = $NULL;
        $response = $NULL;
    }    
}

# Base Uri
$baseUri = 'https://api.mangadex.org';
$token = $NULL;

try {
    $token = Login-User;
	
    Get-MangaStatus -token $token;	
}
catch {
    Write-Error $_;
}
finally {
    Logout-User -token $token;
    $token = $NULL;
}