from schema import Schema

# Settings helpers
azure_key, default_key, destination_key = 'azure', 'default', 'destination'
tenant_id_key, client_id_key = 'tenantId', 'clientId'
per_page_key, max_page_key, min_wait_time_key, max_wait_time_key = 'per_page', 'max_page', 'min_wait_time', 'max_wait_time'
email_key = 'email'
config_schema = Schema({
    azure_key: {
        'tenantid': str,
        'clientid': str,
        str: object,
    },
    default_key: {
        'per_page': int,
        'max_page': int,
        'min_wait_time': int,
        'max_wait_time': int
    },
    destination_key: {
        'email': str
    }
})


def check_config(config):
    config_dict = {}
    for section in config.sections():
        section_values = dict(config.items(section))
        for key, value in section_values.items():
            try:
                section_values[key] = int(value)
            except (ValueError, TypeError):
                # If conversion to int fails, leave the value unchanged
                pass
        config_dict[section] = section_values
    config_schema.validate(config_dict)


# url and web config helpers
def get_headers(access_token):
    return {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }


def fetch_emails_url(per_page, skip):
    return f'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages?$top={per_page}&$skip={skip}'


def get_email_forward_payload(destination_email, message):
    return {
            'message': {
                'subject': message['subject'],
                'toRecipients': [{'emailAddress': {'address': destination_email}}],
            }
        }


def forward_email_url(message):
    return f'https://graph.microsoft.com/v1.0/me/messages/{message["id"]}/forward'


# email subjects containing these strings would be ignored and not forwarded to destination email
subject_substrings = ['Complete your daily screening']

