import connector

if __name__ == "__main__":
    domain = "ftp.freebsd.org"
    path = "/pub/FreeBSD/"

    protocol = input("Connecting to {}. Use 0-http, 1-ftp: ".format(domain))

    if protocol == 0:
        is_secure = bool(input('Use secure? 1-yes 0-no'))
        connector = connector.HTTPConnector(is_secure)
    else:
        connector = connector.FTPConnector(False)

    try:
        content = connector.read(domain, path)
        print connector.parse(content)
    except Exception as e:
        print e
