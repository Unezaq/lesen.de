#!/usr/bin/env python3
"""
Final Website Downloader Script
Properly handles form-based authentication with session management
Downloads entire website with all assets
"""

import os
import re
import sys
import urllib.parse
import urllib.request
import urllib.error
import http.cookiejar
from collections import deque

class WebsiteDownloader:
    def __init__(self, base_url, password, output_dir="downloaded_site"):
        self.base_url = base_url.rstrip('/')
        self.password = password
        self.output_dir = output_dir
        self.visited_urls = set()
        self.to_visit = deque()
        self.domain = urllib.parse.urlparse(base_url).netloc
        
        # Setup cookie handling
        self.cookie_jar = http.cookiejar.CookieJar()
        cookie_processor = urllib.request.HTTPCookieProcessor(self.cookie_jar)
        
        # Setup redirect handler
        redirect_handler = urllib.request.HTTPRedirectHandler()
        
        self.opener = urllib.request.build_opener(cookie_processor, redirect_handler)
        urllib.request.install_opener(self.opener)
        
        self.authenticated_content = None
        
    def login_and_get_content(self):
        """Perform login and get the authenticated content"""
        print("Logging in with password...")
        
        try:
            # Submit login form with POST
            login_data = urllib.parse.urlencode({'code': self.password}).encode('utf-8')
            
            request = urllib.request.Request(
                self.base_url,
                data=login_data,
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            response = self.opener.open(request)
            content = response.read()
            final_url = response.geturl()
            
            print(f"  Response URL: {final_url}")
            print(f"  Cookies: {len(self.cookie_jar)} cookie(s) received")
            
            # Check if we got past the login page
            if b'Zugangscode eingeben' not in content and b'code eingeben' not in content.lower():
                print("  ✓ Login successful!")
                self.authenticated_content = content
                return True, content, final_url
            else:
                print("  ✗ Still on login page - trying alternative method...")
                
                # Try GET request with cookies
                request = urllib.request.Request(
                    self.base_url,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                )
                response = self.opener.open(request)
                content = response.read()
                
                if b'Zugangscode eingeben' not in content:
                    print("  ✓ Login successful on retry!")
                    self.authenticated_content = content
                    return True, content, response.geturl()
                else:
                    print("  ✗ Login failed")
                    return False, content, response.geturl()
                
        except Exception as e:
            print(f"  Login error: {str(e)}")
            return False, None, None
    
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
    
    def download_file(self, url, content=None):
        """Download a single file"""
        if url in self.visited_urls:
            return None
            
        self.visited_urls.add(url)
        
        try:
            # Handle relative URLs
            if not url.startswith('http'):
                url = urllib.parse.urljoin(self.base_url, url)
            
            parsed_url = urllib.parse.urlparse(url)
            
            # Only download from same domain
            if parsed_url.netloc and parsed_url.netloc != self.domain:
                print(f"Skipping external: {url}")
                return None
            
            if content is None:
                print(f"Downloading: {url}")
                request = urllib.request.Request(
                    url,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                )
                response = self.opener.open(request, timeout=30)
                content = response.read()
                content_type = response.headers.get('Content-Type', '')
            else:
                print(f"Saving: {url}")
                content_type = 'text/html'
            
            local_path = self.get_local_path(url)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Write file
            with open(local_path, 'wb') as f:
                f.write(content)
            
            print(f"  → {local_path}")
            
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
    
    def extract_links(self, content, base_url):
        """Extract all links from content"""
        links = set()
        
        try:
            text = content.decode('utf-8', errors='ignore') if isinstance(content, bytes) else content
        except:
            return links
        
        # Patterns to find URLs
        patterns = [
            r'href=["\']([^"\']+)["\']',
            r'src=["\']([^"\']+)["\']',
            r'url\(["\']?([^"\'()]+)["\']?\)',
            r'@import\s+["\']([^"\']+)["\']',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            
            for match in matches:
                # Skip unwanted URLs
                if any(match.startswith(x) for x in ['data:', 'mailto:', 'tel:', 'javascript:', '#', '//']):
                    continue
                
                if not match or match == '#':
                    continue
                
                # Convert to absolute URL
                try:
                    absolute_url = urllib.parse.urljoin(base_url, match)
                    parsed = urllib.parse.urlparse(absolute_url)
                    
                    # Only same domain
                    if not parsed.netloc or parsed.netloc == self.domain:
                        clean_url = urllib.parse.urlunparse((
                            parsed.scheme, parsed.netloc, parsed.path,
                            parsed.params, parsed.query, ''
                        ))
                        links.add(clean_url)
                except:
                    continue
        
        return links
    
    def download_site(self):
        """Download entire website"""
        print("=" * 70)
        print("Website Downloader with Authentication")
        print("=" * 70)
        print(f"URL: {self.base_url}")
        print(f"Output: {self.output_dir}")
        print("=" * 70)
        print()
        
        # Login first
        success, content, final_url = self.login_and_get_content()
        
        if not success:
            print("\n⚠ Warning: Could not authenticate properly")
            print("Continuing with available content...\n")
        
        print("-" * 70)
        
        # Save the main page with authenticated content
        if content:
            result = self.download_file(self.base_url, content)
            if result:
                content, content_type, local_path = result
                
                # Extract links from main page
                links = self.extract_links(content, self.base_url)
                for link in links:
                    if link not in self.visited_urls:
                        self.to_visit.append(link)
        
        # Process queue
        while self.to_visit:
            current_url = self.to_visit.popleft()
            
            if current_url in self.visited_urls:
                continue
            
            result = self.download_file(current_url)
            
            if result:
                content, content_type, local_path = result
                
                # Extract more links from HTML and CSS
                if any(x in content_type.lower() for x in ['html', 'css']) or \
                   any(local_path.endswith(x) for x in ['.html', '.css', '.js']):
                    try:
                        links = self.extract_links(content, current_url)
                        for link in links:
                            if link not in self.visited_urls:
                                self.to_visit.append(link)
                    except Exception as e:
                        pass
        
        print("-" * 70)
        print(f"\n✓ Download complete!")
        print(f"  Files downloaded: {len(self.visited_urls)}")
        print(f"  Location: {os.path.abspath(self.output_dir)}")
        print("=" * 70)


def main():
    URL = "https://pruefvorbnes.onrender.com/"
    PASSWORD = "B48rE3s"
    OUTPUT_DIR = "downloaded_website"
    
    if len(sys.argv) > 1:
        URL = sys.argv[1]
    if len(sys.argv) > 2:
        PASSWORD = sys.argv[2]
    if len(sys.argv) > 3:
        OUTPUT_DIR = sys.argv[3]
    
    downloader = WebsiteDownloader(URL, PASSWORD, OUTPUT_DIR)
    downloader.download_site()


if __name__ == "__main__":
    main()
