# office365-email-transfer-script
Graduating or just want to forward many emails? This script can be used to transfer pertinent (personal) emails from an office365 email to another personal email. It uses Microsoft Graph and runs as a terminal app.

### Files
#### email_transfer_script.py
This file contains the main logic to read emails from the Microsoft account and forward it to another email.

#### settings_helpers.py
This file contains helper functions for processing the configuration.

#### messages_helpers.py
This file contains helper functions for displaying and providing the user messages.

#### config.cfg
This file contains required configuration parameters. It requires the organization's `tenantId`, the `clientId` and a `client_secret` from Azure active directory. You can find your `tenantId` and `clientId` by going through the steps [here](https://learn.microsoft.com/en-us/entra/fundamentals/how-to-find-tenant#find-tenant-id-through-the-azure-portal) and [here](https://learn.microsoft.com/en-us/answers/questions/1319530/how-to-get-client-id-for-azure-active-directory). You can follow the steps [here](https://learn.microsoft.com/en-us/partner-center/marketplace-offers/create-or-update-client-ids-and-secrets) to create a `client-secret`. When creating a client-secret, be sure that the following permissions are granted: `User.Read`, `Mail.Read` and `Mail.Send`.

### Steps to follow
1. Register an app that can get an access token from Microsoft. [Here is a guide.](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app?tabs=certificate)
2. Edit `config.cfg` to add your azure ad info, api management parameters (i.e. `per_page`: how many emails should be retrieved during each call to the api, `max_page`: the highest page number that should be retrieved, `min_wait_time`: the minimum amount of time to wait between page retrieval calls and `max_wait_time`: the maximum amount of time to wait between page retrieval calls) and the email that should be the receipient of the forwarded emails.
3. Run `email_transfer_script.py` and follow the terminal instructions.

### Dependencies
See `pyproject.toml`.

