# xbpse - Xero Bulk Pay Slip Exporter

**xbpse** (Xero Bulk Pay Slip Exporter) is a Python tool designed to automate the process of exporting bulk pay slips from Xero. This tool leverages Selenium for authentication and session management and uses the `requests` library to efficiently download pay slips in PDF format.

## Features

- **Automated Login**: Uses Selenium to automate the login process, ensuring seamless access to Xero.
- **Session Management**: Retrieves session cookies from Selenium, enabling authenticated requests to Xero’s API.
- **Bulk Export**: Efficiently fetches multiple pages of pay slip data and downloads each pay slip as a PDF.
- **Custom File Naming**: Saves pay slips with filenames that include the relevant pay period dates, making it easy to organize and find files.

## Prerequisites

- Python 3.x
- Google Chrome
- ChromeDriver (compatible with your Chrome version)
- Required Python packages: `selenium`, `requests`

You can install the necessary Python packages with:

```bash
pip install selenium requests
```

## Demo

![Demo GIF](https://github.com/BlenderItUp/xbpse-XeroBulkPaySlipExporter/blob/main/Demo.gif)

Check out the demo above to see how **xbpse** works in action.

## Usage

### Important Note on `CID`

When entering the `CID` during the setup, ensure it includes the exclamation mark (`!`). For example, if your `CID` is `A3K4`, you should enter it as `!A3K4`.

1. **Run the Script**:

After running the script, you will be prompted to enter your Xero `CID`. You can find this in the URL when logged into Xero. Navigate to the EmployeePortal where you want to download your pay slips. From there, check your current URL and copy the `CID` code (e.g., `!32GA1`).

2. **Login**:

   The script will open a Chrome window. Log in to your Xero account as usual.

3. **Export Pay Slips**:

   Once logged in, the script will automatically start fetching and downloading pay slips based on the data retrieved from Xero’s API. The pay slips will be saved in the `output` directory with filenames that include the start and end dates of the pay period.

## Example Output

The exported pay slips will be saved as:
output/
│
├── PaySlip_2024-06-24_to_2024-06-30__250043116.pdf
├── PaySlip_2024-07-01_to_2024-07-07__250043117.pdf
└── ...
