import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to make a request for a specific page
def fetch_page(page, start):
    body = body_template.format(
        token=verification_token,
        page=page,
        start=start,
        limit=50
    )
    response = session.post(url, headers=headers, data=body, params={"CID": CID})
    
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.reason}")
        print(f"Response content: {response.text}")
        return None
    
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"Failed to decode JSON: {response.text}")
        return None
    
def convert_json_date(json_date_str):
    timestamp = int(json_date_str[6:-2]) / 1000  # Convert from milliseconds to seconds
    return time.strftime('%Y-%m-%d', time.gmtime(timestamp))

def safe_rename(default_filename, new_filename):
    if os.path.exists(new_filename):
        base, extension = os.path.splitext(new_filename)
        counter = 1
        while os.path.exists(new_filename):
            new_filename = f"{base}_{counter}{extension}"
            counter += 1
    os.rename(default_filename, new_filename)

# Ask the user for the CID input
CID = input("Please enter your CID: ")

# Create a folder for downloaded files
folder_name = "output"
os.makedirs(folder_name, exist_ok=True)

# Configure Chrome options to specify download directory and enable logging
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": os.path.abspath(folder_name),
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Setup Selenium WebDriver
driver = webdriver.Chrome(options=chrome_options)

print("Please sign in to Xero")
# Open the login page with the user-provided CID
login_url = f"https://payroll.xero.com/EmployeePortal/PayRunHistory?CID={CID}"
driver.get(login_url)

# Wait until the user is logged in
WebDriverWait(driver, 300).until(EC.url_to_be(login_url))

# Once logged in, get the cookies from Selenium and use them in the requests session
cookies = driver.get_cookies()
session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

# Extract the verification token from the page
verification_token = driver.execute_script(
    "return document.querySelector('input[name=__RequestVerificationToken]').value"
)

driver.quit()  # Close the browser once login is complete

# URL and headers for the request
url = "https://payroll.xero.com/EmployeePortal/PayRunHistory/ListAjax"
headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "https://payroll.xero.com/",
    "Host": "payroll.xero.com",
}

# Define the body template for the POST request
body_template = (
    "__RequestVerificationToken={token}"
    "&page={page}"
    "&start={start}"
    "&limit={limit}"
    "&sort=[{{\"property\":\"PostedDateTime\",\"direction\":\"ASC\"}}]"
)

all_data = []
page = 1
start = 0

while True:
    print(f"Fetching page {page} starting at {start}...")
    data = fetch_page(page, start)
    
    if not data or not data.get('Data'):
        print("No more data found or an error occurred.")
        break
    
    all_data.extend(data['Data'])
    
    page += 1
    start += 50

print(f"Total records fetched: {len(all_data)}")

# Iterate over the consolidated data and download each PDF
for item in all_data:
    payslip_id = item['PaySlipID']
    payee_id = item['PayeeID']
    # Get the start and end dates from the period
    start_date = convert_json_date(item['Period']['Weeks'][0]['StartDate'])
    end_date = convert_json_date(item['Period']['Weeks'][0]['EndDate'])
    
    # Construct the URL using the CID provided by the user
    pdf_url = f"https://payroll.xero.com/EmployeePortal/PayRunHistory/PrintPaySlip/{payslip_id}?payeeID={payee_id}&CID={CID}"
    
    # Make a GET request to download the PDF
    pdf_response = session.get(pdf_url)
    pdf_filename = f"{folder_name}/PaySlip_{start_date}_to_{end_date}__{payslip_id}.pdf"
    
    # Write the PDF file to the folder
    with open(pdf_filename, "wb") as pdf_file:
        pdf_file.write(pdf_response.content)
    
    print(f"Downloaded PaySlip: {pdf_filename}")

print("\n--Download Finished--")
