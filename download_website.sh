#!/bin/bash

# Website Downloader Script using curl
# Downloads website with password authentication

# Configuration
URL="https://pruefvorbnes.onrender.com/"
PASSWORD="B48rE3s"
OUTPUT_DIR="downloaded_website"

# Allow command line arguments
if [ ! -z "$1" ]; then
    URL="$1"
fi

if [ ! -z "$2" ]; then
    PASSWORD="$2"
fi

if [ ! -z "$3" ]; then
    OUTPUT_DIR="$3"
fi

echo "=========================================="
echo "Website Downloader (curl version)"
echo "=========================================="
echo "URL: $URL"
echo "Output: $OUTPUT_DIR"
echo "=========================================="
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Function to download a page and extract links
download_page() {
    local url="$1"
    local output_file="$2"
    
    echo "Downloading: $url"
    
    # Download with password authentication
    curl -u ":$PASSWORD" \
         -L \
         --create-dirs \
         -o "$output_file" \
         -s \
         -w "Status: %{http_code}\n" \
         "$url"
    
    if [ $? -eq 0 ]; then
        echo "  Saved to: $output_file"
    else
        echo "  Failed to download"
    fi
}

# Download main page
echo "Downloading main page..."
download_page "$URL" "$OUTPUT_DIR/index.html"

# Extract and download CSS files
echo ""
echo "Extracting CSS files..."
if [ -f "$OUTPUT_DIR/index.html" ]; then
    grep -oP '(?<=href=")[^"]*\.css' "$OUTPUT_DIR/index.html" | while read -r css_file; do
        # Handle relative URLs
        if [[ $css_file == http* ]]; then
            css_url="$css_file"
        else
            css_url="${URL%/}/${css_file#/}"
        fi
        
        # Create local path
        local_path="$OUTPUT_DIR/${css_file#/}"
        mkdir -p "$(dirname "$local_path")"
        
        download_page "$css_url" "$local_path"
    done
fi

# Extract and download JS files
echo ""
echo "Extracting JavaScript files..."
if [ -f "$OUTPUT_DIR/index.html" ]; then
    grep -oP '(?<=src=")[^"]*\.js' "$OUTPUT_DIR/index.html" | while read -r js_file; do
        # Handle relative URLs
        if [[ $js_file == http* ]]; then
            js_url="$js_file"
        else
            js_url="${URL%/}/${js_file#/}"
        fi
        
        # Create local path
        local_path="$OUTPUT_DIR/${js_file#/}"
        mkdir -p "$(dirname "$local_path")"
        
        download_page "$js_url" "$local_path"
    done
fi

# Extract and download images
echo ""
echo "Extracting images..."
if [ -f "$OUTPUT_DIR/index.html" ]; then
    grep -oP '(?<=src=")[^"]*\.(jpg|jpeg|png|gif|svg|webp|ico)' "$OUTPUT_DIR/index.html" | while read -r img_file; do
        # Handle relative URLs
        if [[ $img_file == http* ]]; then
            img_url="$img_file"
        else
            img_url="${URL%/}/${img_file#/}"
        fi
        
        # Create local path
        local_path="$OUTPUT_DIR/${img_file#/}"
        mkdir -p "$(dirname "$local_path")"
        
        download_page "$img_url" "$local_path"
    done
fi

# Download favicon
echo ""
echo "Downloading favicon..."
download_page "${URL%/}/favicon.ico" "$OUTPUT_DIR/favicon.ico"

echo ""
echo "=========================================="
echo "Download complete!"
echo "Files saved to: $(cd "$OUTPUT_DIR" && pwd)"
echo "=========================================="
