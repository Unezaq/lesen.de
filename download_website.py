#!/usr/bin/env python3
"""
Website Downloader Script
Downloads entire website with HTML, CSS, JS, images, and all assets
Supports password-protected sites
"""

import os
import re
import sys
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path
from html.parser import HTMLParser
from collections import deque

class WebsiteDownloader:
    def __init__(self, base_url, password, output_dir="downloaded_site"):
        self.base_url = base_url.rstrip('/')
        self.password = password
        self.output_dir = output_dir
        self.visited_urls = set()
        self.to_visit = deque()
        self.domain = urllib.parse.urlparse(base_url).netloc
        
    def setup_auth(self):
        """Setup password authentication"""
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.base_url, '', self.password)
        auth_handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(auth_handler)
        urllib.request.install_opener(opener)
        
    def get_local_path(self, url):
        """Convert URL to local file path"""
        parsed = urllib.parse.urlparse(url)
        path = parsed.path
        
        if not path or path == '/':
            path = '/index.html'
        elif not os.path.splitext(path)[1]:
            path = path.rstrip('/') + '/index.html'
            
        local_path = os.path.join(self.output_dir, parsed.netloc, path.lstrip('/'))
        return local_path
    
    def download_file(self, url):
        """Download a single file"""
        if url in self.visited_urls:
            return None
            
        self.visited_urls.add(url)
        
        try:
            print(f"Downloading: {url}")
            
            # Handle relative URLs
            if not url.startswith('http'):
                url = urllib.parse.urljoin(self.base_url, url)
            
            # Only download from same domain
            if urllib.parse.urlparse(url).netloc != self.domain:
                print(f"  Skipping external URL: {url}")
                return None
            
            response = urllib.request.urlopen(url, timeout=30)
            content = response.read()
            content_type = response.headers.get('Content-Type', '')
            
            local_path = self.get_local_path(url)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Write file
            mode = 'wb' if isinstance(content, bytes) else 'w'
            with open(local_path, mode) as f:
                f.write(content)
            
            print(f"  Saved to: {local_path}")
            
            return content, content_type, local_path
            
        except urllib.error.HTTPError as e:
            print(f"  HTTP Error {e.code}: {url}")
            return None
        except urllib.error.URLError as e:
            print(f"  URL Error: {e.reason}")
            return None
        except Exception as e:
            print(f"  Error: {str(e)}")
            return None
    
    def extract_links(self, html_content, base_url):
        """Extract all links from HTML content"""
        links = set()
        
        # Find all href attributes
        href_pattern = r'(?:href|src)=["\']([^"\']+)["\']'
        matches = re.findall(href_pattern, str(html_content))
        
        for match in matches:
            # Skip data URIs, mailto, tel, etc.
            if match.startswith(('data:', 'mailto:', 'tel:', 'javascript:', '#')):
                continue
                
            # Convert to absolute URL
            absolute_url = urllib.parse.urljoin(base_url, match)
            
            # Only add URLs from same domain
            if urllib.parse.urlparse(absolute_url).netloc == self.domain:
                links.add(absolute_url)
        
        return links
    
    def download_site(self):
        """Download entire website"""
        print(f"Starting download of: {self.base_url}")
        print(f"Output directory: {self.output_dir}")
        print("-" * 60)
        
        # Setup authentication
        self.setup_auth()
        
        # Start with base URL
        self.to_visit.append(self.base_url)
        
        while self.to_visit:
            current_url = self.to_visit.popleft()
            
            if current_url in self.visited_urls:
                continue
            
            result = self.download_file(current_url)
            
            if result:
                content, content_type, local_path = result
                
                # If it's HTML, extract and queue more links
                if 'text/html' in content_type:
                    try:
                        html_content = content.decode('utf-8') if isinstance(content, bytes) else content
                        links = self.extract_links(html_content, current_url)
                        
                        for link in links:
                            if link not in self.visited_urls:
                                self.to_visit.append(link)
                                
                    except Exception as e:
                        print(f"  Error parsing HTML: {str(e)}")
        
        print("-" * 60)
        print(f"Download complete!")
        print(f"Total files downloaded: {len(self.visited_urls)}")
        print(f"Files saved to: {os.path.abspath(self.output_dir)}")


def main():
    # Configuration
    URL = "https://pruefvorbnes.onrender.com/"
    PASSWORD = "B48rE3s"
    OUTPUT_DIR = "downloaded_website"
    
    # Allow command line arguments
    if len(sys.argv) > 1:
        URL = sys.argv[1]
    if len(sys.argv) > 2:
        PASSWORD = sys.argv[2]
    if len(sys.argv) > 3:
        OUTPUT_DIR = sys.argv[3]
    
    print("=" * 60)
    print("Website Downloader")
    print("=" * 60)
    print(f"URL: {URL}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)
    print()
    
    downloader = WebsiteDownloader(URL, PASSWORD, OUTPUT_DIR)
    downloader.download_site()


if __name__ == "__main__":
    main()
