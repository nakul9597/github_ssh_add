import sys
import mechanize
from pathlib import Path
import getpass

# get home directory path and open public key file
home = str(Path.home())
f = open(home+'/.ssh/github_ssh.pub', 'r')

# Browser
br = mechanize.Browser()


# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Chrome')]

# The site we will navigate into, handling it's session

for i in range(3):
    br.open('https://github.com/login')

    # Select the first (index zero) form (the first form is a search query box)
    br.select_form(nr=0)

    # User credentials
    passwd = getpass.getpass(prompt='Enter your github password')
    br.form['login'] = sys.argv[1]
    br.form['password'] = passwd

    # Login
    response = br.submit()
    # response = br.open('https://github.com/settings')
    # print(response.info())
    # print(response.geturl())
    if response.geturl() != "https://github.com":
        print("\n\nWrong password.")
    else:
        break

if response.geturl() != "https://github.com":
    print("\nNumber of tries exceeded.. Retry manually from :\n\n")
    exit()

print("\nlogin successfully")

br.open('https://github.com/settings/ssh/new')

br.select_form(nr=3)
br.form['public_key[title]'] = "test_popos"
br.form['public_key[key]'] = f.read()

response = br.submit()

if response.code == 200:
    print("\n\nKey successfully added in github")
else:
    print("some error")
