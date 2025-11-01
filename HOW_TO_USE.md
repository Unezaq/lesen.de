# Website Downloader - Complete Guide

## 🎯 Quick Start

The website has already been downloaded! All files are in the `downloaded_website/` directory.

To view the downloaded website:
```bash
# Open the main page in your browser
open downloaded_website/pruefvorbnes.onrender.com/index.html
```

---

## 📦 What You Have

### 1. Downloaded Website
- **Location**: `downloaded_website/`
- **Files**: 238 HTML pages
- **Status**: ✅ Complete and ready to use

### 2. Download Scripts

#### **download_website_final.py** (Recommended)
The most advanced script with full authentication support.

```bash
python3 download_website_final.py
```

**Features:**
- ✅ Form-based password authentication
- ✅ Session cookie management  
- ✅ Automatic crawling of all pages
- ✅ Downloads all HTML, CSS, JS, images
- ✅ Preserves directory structure
- ✅ Handles redirects properly

#### **download_website_advanced.py**
Alternative Python script with similar features.

```bash
python3 download_website_advanced.py
```

#### **download_website.py**
Basic Python downloader.

```bash
python3 download_website.py
```

#### **download_website.sh**
Bash script using curl (simpler but less comprehensive).

```bash
./download_website.sh
```

---

## 🔧 Customizing the Download

All scripts accept command-line arguments:

```bash
python3 download_website_final.py <URL> <PASSWORD> <OUTPUT_DIR>
```

### Examples:

**Download to a different directory:**
```bash
python3 download_website_final.py https://pruefvorbnes.onrender.com/ B48rE3s my_custom_folder
```

**Download a different website:**
```bash
python3 download_website_final.py https://example.com/ mypassword output_folder
```

---

## 📖 Viewing the Downloaded Website

### Method 1: Direct Browser Access (Simplest)
Just double-click any HTML file or use:
```bash
open downloaded_website/pruefvorbnes.onrender.com/index.html
```

### Method 2: Local Web Server (Recommended for full functionality)

**Python:**
```bash
cd downloaded_website
python3 -m http.server 8000
```
Then visit: http://localhost:8000/pruefvorbnes.onrender.com/

**Node.js:**
```bash
cd downloaded_website
npx http-server -p 8000
```
Then visit: http://localhost:8000/pruefvorbnes.onrender.com/

**PHP:**
```bash
cd downloaded_website
php -S localhost:8000
```
Then visit: http://localhost:8000/pruefvorbnes.onrender.com/

---

## 📂 File Structure

```
/vercel/sandbox/
├── download_website_final.py      ⭐ Best script (recommended)
├── download_website_advanced.py   Alternative Python script
├── download_website.py            Basic Python script
├── download_website.sh            Bash script with curl
├── DOWNLOAD_INSTRUCTIONS.md       Detailed instructions
├── DOWNLOAD_SUMMARY.md            Download results summary
├── HOW_TO_USE.md                  This file
└── downloaded_website/            ✅ Your downloaded website
    └── pruefvorbnes.onrender.com/
        ├── index.html             Main page
        ├── index1/                B1 section
        ├── index2/                B2 section
        ├── home/                  Home page
        ├── logout/                Logout page
        └── quiz/                  233 quiz pages
            ├── 1/index.html
            ├── 2/index.html
            └── ...
```

---

## 🔐 Authentication Details

- **URL**: https://pruefvorbnes.onrender.com/
- **Password**: B48rE3s
- **Method**: Form POST with `code` parameter
- **Session**: Managed via cookies

The scripts automatically:
1. Submit the password via POST request
2. Receive and store session cookies
3. Use cookies for all subsequent requests
4. Download authenticated content

---

## 🎨 Website Content

### What's Included:
- ✅ All HTML pages (238 files)
- ✅ Embedded CSS (inline styles)
- ✅ Embedded JavaScript (inline scripts)
- ✅ SVG icons (inline)
- ✅ Complete quiz system
- ✅ Navigation pages (B1, B2)

### What's NOT Needed:
- ❌ No external CSS files (all embedded)
- ❌ No external JS files (all embedded)
- ❌ No external images (uses inline SVG)

**Result**: Each HTML file is completely self-contained and works offline!

---

## 🚀 Re-downloading or Updating

To download the website again (e.g., if content has changed):

```bash
# Remove old download
rm -rf downloaded_website

# Download fresh copy
python3 download_website_final.py
```

Or download to a new directory:
```bash
python3 download_website_final.py https://pruefvorbnes.onrender.com/ B48rE3s new_download_$(date +%Y%m%d)
```

---

## 🛠️ Troubleshooting

### Problem: "Login failed"
- Verify the password is correct: `B48rE3s`
- Check your internet connection
- The website might have changed its authentication method

### Problem: "Files not downloading"
- Check internet connection
- Verify the website is accessible
- Try the alternative scripts

### Problem: "Can't open HTML files"
- Make sure you have a web browser installed
- Try using a local web server (Method 2 above)

### Problem: "Links don't work"
- Use a local web server instead of opening files directly
- Some features may require server-side processing

---

## 📊 Script Comparison

| Feature | final.py | advanced.py | basic.py | .sh |
|---------|----------|-------------|----------|-----|
| Authentication | ✅ Best | ✅ Good | ⚠️ Basic | ⚠️ Basic |
| Auto-crawling | ✅ Yes | ✅ Yes | ✅ Yes | ⚠️ Limited |
| Session cookies | ✅ Yes | ✅ Yes | ⚠️ Basic | ❌ No |
| Redirect handling | ✅ Yes | ✅ Yes | ⚠️ Basic | ⚠️ Basic |
| Error handling | ✅ Excellent | ✅ Good | ⚠️ Basic | ⚠️ Basic |
| **Recommended** | ⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ |

---

## 💡 Tips

1. **Backup**: Keep a copy of the downloaded files
   ```bash
   cp -r downloaded_website downloaded_website_backup_$(date +%Y%m%d)
   ```

2. **Search content**: Find specific text across all pages
   ```bash
   grep -r "search term" downloaded_website/
   ```

3. **Count pages**: See how many pages were downloaded
   ```bash
   find downloaded_website -name "*.html" | wc -l
   ```

4. **Archive**: Create a zip file for easy sharing
   ```bash
   zip -r website_backup.zip downloaded_website/
   ```

---

## ✅ Success Checklist

- [x] Scripts created and executable
- [x] Website downloaded (238 files)
- [x] Authentication successful
- [x] All pages accessible
- [x] Documentation complete

---

## 📞 Need Help?

If you encounter issues:
1. Check the error messages in the script output
2. Verify your internet connection
3. Ensure the website is still accessible online
4. Try alternative scripts
5. Check if the password has changed

---

**🎉 Enjoy your offline copy of the website!**
