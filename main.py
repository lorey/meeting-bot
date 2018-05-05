import config
import meetingbot


def main():
    print('I\'m a bot')
    h = meetingbot.crm.Hubspot(config.HUBSPOT_API_KEY)

    email = input('Email:')
    note = input('Note:')
    result = h.push_note(email, note)
    print(result)


if __name__ == '__main__':
    main()