#!/usr/bin/env python3
"""
Advanced Website Downloader Script
Downloads entire website with form-based authentication
Handles HTML, CSS, JS, images, and all assets
"""

import os
import re
import sys
import urllib.parse
import urllib.request
import urllib.error
import http.cookiejar
from pathlib import Path
from collections import deque

class AdvancedWebsiteDownloader:
    def __init__(self, base_url, password, output_dir="downloaded_site"):
        self.base_url = base_url.rstrip('/')
        self.password = password
        self.output_dir = output_dir
        self.visited_urls = set()
        self.to_visit = deque()
        self.domain = urllib.parse.urlparse(base_url).netloc
        
        # Setup cookie handling for session management
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar)
        )
        urllib.request.install_opener(self.opener)
        
    def login(self):
        """Perform login with password"""
        print("Attempting to login...")
        
        try:
            # First, get the login page to establish session
            response = urllib.request.urlopen(self.base_url)
            
            # Submit login form
            login_data = urllib.parse.urlencode({'code': self.password}).encode('utf-8')
            request = urllib.request.Request(self.base_url, data=login_data)
            response = urllib.request.urlopen(request)
            
            content = response.read()
            
            # Check if login was successful (not showing login form anymore)
            if b'Zugangscode eingeben' in content or b'code eingeben' in content.lower():
                print("  Login may have failed - still seeing login form")
                return False
            else:
                print("  Login successful!")
                return True
                
        except Exception as e:
            print(f"  Login error: {str(e)}")
            return False
    
    def get_local_path(self, url):
        """Convert URL to local file path"""
        parsed = urllib.parse.urlparse(url)
        path = parsed.path
        
        # Remove query parameters for file path
        if parsed.query:
            path = path
        
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
            
            # Parse URL to check domain
            parsed_url = urllib.parse.urlparse(url)
            
            # Only download from same domain
            if parsed_url.netloc and parsed_url.netloc != self.domain:
                print(f"  Skipping external URL: {url}")
                return None
            
            # Download with session cookies
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request, timeout=30)
            content = response.read()
            content_type = response.headers.get('Content-Type', '')
            
            local_path = self.get_local_path(url)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Write file
            with open(local_path, 'wb') as f:
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
        
        try:
            html_str = html_content.decode('utf-8') if isinstance(html_content, bytes) else html_content
        except:
            return links
        
        # Find all href and src attributes
        patterns = [
            r'href=["\']([^"\']+)["\']',
            r'src=["\']([^"\']+)["\']',
            r'url\(["\']?([^"\'()]+)["\']?\)',  # CSS url()
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html_str, re.IGNORECASE)
            
            for match in matches:
                # Skip data URIs, mailto, tel, etc.
                if match.startswith(('data:', 'mailto:', 'tel:', 'javascript:', '#', '//')):
                    continue
                
                # Skip empty or just fragment
                if not match or match == '#':
                    continue
                    
                # Convert to absolute URL
                absolute_url = urllib.parse.urljoin(base_url, match)
                
                # Only add URLs from same domain
                parsed = urllib.parse.urlparse(absolute_url)
                if not parsed.netloc or parsed.netloc == self.domain:
                    # Remove fragment
                    clean_url = urllib.parse.urlunparse((
                        parsed.scheme, parsed.netloc, parsed.path,
                        parsed.params, parsed.query, ''
                    ))
                    links.add(clean_url)
        
        return links
    
    def download_site(self):
        """Download entire website"""
        print(f"Starting download of: {self.base_url}")
        print(f"Output directory: {self.output_dir}")
        print("-" * 60)
        
        # Login first
        if not self.login():
            print("Warning: Login may have failed, continuing anyway...")
        
        print("-" * 60)
        
        # Start with base URL
        self.to_visit.append(self.base_url)
        
        while self.to_visit:
            current_url = self.to_visit.popleft()
            
            if current_url in self.visited_urls:
                continue
            
            result = self.download_file(current_url)
            
            if result:
                content, content_type, local_path = result
                
                # If it's HTML or CSS, extract and queue more links
                if 'text/html' in content_type or 'text/css' in content_type or local_path.endswith(('.html', '.css')):
                    try:
                        links = self.extract_links(content, current_url)
                        
                        for link in links:
                            if link not in self.visited_urls:
                                self.to_visit.append(link)
                                
                    except Exception as e:
                        print(f"  Error parsing content: {str(e)}")
        
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
    print("Advanced Website Downloader")
    print("=" * 60)
    print(f"URL: {URL}")
    print(f"Password: {PASSWORD}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)
    print()
    
    downloader = AdvancedWebsiteDownloader(URL, PASSWORD, OUTPUT_DIR)
    downloader.download_site()


if __name__ == "__main__":
    main()
