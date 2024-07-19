_messages = {
    'initial_choice': ('Please choose one of the following options:\n\n'
                       '0. Exit\n'
                       '1. Start emails transfer\n'),
    'successful_exit': 'Goodbye...',
    'invalid_choice': 'Invalid choice! Try again.\n',
    'initial_page_question': 'What page should I start fetching from?',
    'email_reading_complete': 'Done reading emails'
}


def get(key, *args):
    if key in _messages:
        return _messages[key].format(*args)
    else:
        print(f'Message key "{key}" not found')
        return None


def display(key, values=None):
    if key in _messages:
        print(_messages[key])
    elif isinstance(values, list):
        _display_with_values(key, values)
    else:
        raise KeyError(f'Message key "{key}" not found')


def _display_with_values(key, values):
    if key == 'user_token':
        res = f'User token: {values[0]} \n'
    elif key == 'read_email_status':
        res = f'Starting to try reading emails... skip: {values[0]}, page: {values[1]}'
    elif key == 'forwarded_email_success':
        res = f'Forwarded email: {values[0]}'
    elif key == 'forwarded_email_failure':
        res = f'Failed to forward email: {values[0]} - {values[1]}'
    elif key == 'retrieve_email_failure':
        res = f'Failed to fetch emails: {values[0]} - {values[1]}'
    elif key == 'messages_skipped':
        res = f'{values[0]} daily screen emails not forwarded'
    else:
        raise KeyError(f'Message key "{key}" not found')

    print(res)
