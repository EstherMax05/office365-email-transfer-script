from azure.identity import DeviceCodeCredential
from configparser import SectionProxy

import asyncio
import configparser
import messages_helpers
import random
import requests
import settings_helpers
import time


class Graph:
    settings: SectionProxy
    device_code_credential: DeviceCodeCredential

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings[settings_helpers.client_id_key]
        tenant_id = self.settings[settings_helpers.tenant_id_key]

        self.device_code_credential = DeviceCodeCredential(client_id, tenant_id=tenant_id)

    async def get_user_token(self):
        graph_scopes = self.settings['graphUserScopes']
        access_token = self.device_code_credential.get_token(graph_scopes)
        return access_token.token


async def transfer_emails(graph: Graph, default_settings, destination_settings):
    token = await graph.get_user_token()
    messages_helpers.display('user_token', [token])
    messages_helpers.display('initial_page_question')
    page = int(input())

    max_page = int(default_settings[settings_helpers.max_page_key])
    per_page = int(default_settings[settings_helpers.per_page_key])
    min_wait_time = int(default_settings[settings_helpers.min_wait_time_key])
    max_wait_time = int(default_settings[settings_helpers.max_wait_time_key])
    destination_email = destination_settings[settings_helpers.email_key]

    while page < max_page:
        skip = page * per_page
        messages_helpers.display('read_email_status', [skip, page])
        get_and_forward_emails(token, skip, destination_email, per_page)
        messages_helpers.display('email_reading_complete')
        page = page + 1
        time.sleep(random.randint(min_wait_time, max_wait_time))


def get_and_forward_emails(access_token, skip, destination_email, per_page):
    headers = settings_helpers.get_headers(access_token)

    def forward_email(msg, print_subject=False):
        forward_data = settings_helpers.get_email_forward_payload(destination_email, msg)
        post_response = requests.post(
            settings_helpers.forward_email_url(msg),
            headers=headers,
            json=forward_data,
        )
        if post_response.status_code == 202:
            if print_subject:
                messages_helpers.display('forwarded_email_success', [msg['subject']])
        else:
            messages_helpers.display('forwarded_email_failure', [post_response.status_code, post_response.text])

    # Fetch emails from the source account
    response = requests.get(
        settings_helpers.fetch_emails_url(per_page, skip),
        headers=headers,
    )

    if response.status_code == 200:
        messages = response.json()["value"]
        messages_skipped = 0
        for message in messages:
            if (message['subject'] is not None
                    and any(substring in message['subject'] for substring in settings_helpers.subject_substrings)):
                messages_skipped += 1
                continue
            # Forward the email to the destination account
            forward_email(headers, message)
        if messages_skipped > 0:
            messages_helpers.display('messages_skipped', [messages_skipped])
    else:
        messages_helpers.display('retrieve_email_failure', [response.status_code, response.text])


async def main():
    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg'])

    settings_helpers.check_config(config)  # validate settings

    azure_settings = config[settings_helpers.azure_key]
    default_settings = config[settings_helpers.default_key]
    destination_settings = config[settings_helpers.destination_key]

    graph: Graph = Graph(azure_settings)

    # start service
    choice = -1

    while choice != 0:
        messages_helpers.display('initial_choice')
        try:
            choice = int(input())
        except ValueError:
            choice = -1
        if choice == 0:
            messages_helpers.display('successful_exit')
        elif choice == 1:
            await transfer_emails(graph, default_settings, destination_settings)
        else:
            messages_helpers.display('invalid_choice')

loop = asyncio.get_event_loop()
result = loop.run_until_complete(main())
