# Website Downloader Scripts

Two scripts are provided to download the entire website from https://pruefvorbnes.onrender.com/

## Option 1: Python Script (Recommended)

The Python script is more comprehensive and will automatically crawl all pages and download all assets.

### Usage:

```bash
python3 download_website.py
```

Or with custom parameters:

```bash
python3 download_website.py <URL> <PASSWORD> <OUTPUT_DIR>
```

### Example:

```bash
python3 download_website.py https://pruefvorbnes.onrender.com/ B48rE3s my_website
```

### Features:
- Automatically crawls all linked pages
- Downloads HTML, CSS, JavaScript, images, and all assets
- Handles password authentication
- Preserves directory structure
- Skips external links

---

## Option 2: Bash Script (Simple)

The bash script uses curl and is simpler but less comprehensive.

### Usage:

```bash
./download_website.sh
```

Or with custom parameters:

```bash
./download_website.sh <URL> <PASSWORD> <OUTPUT_DIR>
```

### Example:

```bash
./download_website.sh https://pruefvorbnes.onrender.com/ B48rE3s my_website
```

### Features:
- Downloads main page
- Extracts and downloads CSS files
- Extracts and downloads JavaScript files
- Extracts and downloads images
- Downloads favicon

---

## Default Configuration

Both scripts use these defaults (can be overridden):
- **URL**: https://pruefvorbnes.onrender.com/
- **Password**: B48rE3s
- **Output Directory**: downloaded_website

---

## Output

All files will be saved to the `downloaded_website` directory (or your custom directory name) with the original directory structure preserved.

---

## Requirements

### Python Script:
- Python 3.x (already available on your system)
- No additional packages required (uses standard library)

### Bash Script:
- curl (already available on your system)
- bash
- grep with Perl regex support

---

## Troubleshooting

### If authentication fails:
- Verify the password is correct: `B48rE3s`
- Check if the website requires a different authentication method

### If downloads are incomplete:
- Use the Python script for better crawling
- Check your internet connection
- Verify the website is accessible

### If you get permission errors:
- Make sure the scripts are executable: `chmod +x download_website.py download_website.sh`
- Check write permissions in the output directory

---

## Notes

- The Python script will automatically follow links and download all pages
- External links (different domains) are skipped
- The scripts preserve the original directory structure
- Downloaded files can be viewed locally by opening index.html in a browser
