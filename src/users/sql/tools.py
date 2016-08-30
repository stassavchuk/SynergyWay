"""This module provides special tools for database.

"""

from random import randint


def data_generator(n):
    """
    Generator of random data. Yields tuple of random generated name, email and phone number.
    :param n: Count of data to generate.
    :return: Generator of tuple (name, email, status, phone, m_phone)
    """
    f_name_start = ['Mo', 'He', 'Ja', 'Schmu', 'Schlo']
    f_name_end = ['donei', 'shel', 'mon', 'mo', 'diah']
    l_name_start = ['Gold', 'Wasser', 'Edel', 'Bergen', 'Braun']
    l_name_end = ['berg', 'stein', 'meyer', 'owsky', 'heimer']

    operator = ['050', '067', '095', '063', '093']

    mailbox = ['gmail.com', 'hotmail.com', 'yahoo.com', 'protonmail.com', 'mail.com']

    for i in xrange(n):
        name = str(f_name_start[randint(0, 4)])
        name += str(f_name_end[randint(0, 4)])
        name += ' '
        name += str(l_name_start[randint(0, 4)])
        name += str(l_name_end[randint(0, 4)])

        email = name.replace(' ', '.').lower() + '@' + str(mailbox[randint(0, 4)])

        status = bool(randint(0, 1))

        phone = '+38' + str(operator[randint(0, 4)]) + str(randint(1000000, 9999999))

        m_phone = '+38032' + str(randint(1000000, 9999999))

        yield (name, email, status, phone, m_phone)
