import hashlib
import sys
import requests


def request_pass(password_query, last):
    url = 'https://api.pwnedpasswords.com/range/' + password_query
    res = requests.get(url)
    if res.status_code != 200:
        print('Connection Problem')
    return read_response(res, last)


def sha1_convert(password):
    sha1pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    firstfive = sha1pass[:5]
    last = sha1pass[5:]
    return request_pass(firstfive, last)


def read_response(res, last):
    response_txt = res.text
    hashes = (line.split(':') for line in response_txt.splitlines())
    total = 0
    for item, count in hashes:
        if item == last:
            total += int(count)
    if total != 0:
        return total
    else:
        return 0


def main(argv):
    for password in argv:
        check_count = sha1_convert(password)
        if check_count:
            print(f'************************************************************ \n'
                  f'This password "{password}" has been seen {check_count} times before.\n'
                  f'If you\'ve ever used it anywhere before, change it!\n'
                  f'************************************************************ ')
        else:
            print(f'Good news — "{password}" No Match found!')
    return 'All Done!'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
