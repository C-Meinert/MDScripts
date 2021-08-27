$script:baseUri = 'https://api.mangadex.org';

function Login {
    param (
        [Parameter(Mandatory = $true, HelpMessage = 'PSCredential object containing users mangadex credentials')]
        [PSCredential]$mdCredentials
    )
    try {
        $headers = @{
            'accept'       = 'application/json';
            'content-type' = 'application/json'
        };

        # Authenticate
        $requestUri = "${$script:baseUri}/auth/login";
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
}

function Logout {
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
		$requestUri = "${$script:baseUri}/auth/logout";
		$response = Invoke-WebRequest -Method Post -Headers $headers -Uri $requestUri;

		if ($response.StatusCode -ne 200) {
			throw "Failed to logout:`nStatus Code: $($response.StatusCode)";
		}
	}
	catch {
		throw $_;
	}    
}

Export-ModuleMember -Function Login, Logout