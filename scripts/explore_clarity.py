"""
Explore Arkansas Clarity Elections to find available election data
"""
import clarify
import requests
from bs4 import BeautifulSoup

# Try to find Arkansas election URLs
# Common patterns for Clarity URLs:
# https://results.enr.clarityelections.com/AR/{election_id}/{report_id}/en/summary.html

# Let's try to scrape the main AR page to find available elections
def find_ar_elections():
    """Try different approaches to find Arkansas Clarity elections"""
    
    # Try known patterns for recent Arkansas elections
    # Format: https://results.enr.clarityelections.com/AR/{election_id}/{report_id}/
    
    # Try 2024 General
    test_urls = [
        "https://results.enr.clarityelections.com/AR/115450/web.285569/#/summary",
        "https://results.enr.clarityelections.com/AR/115450/285569/en/summary.html",
        "https://results.enr.clarityelections.com/AR/113429/web.277746/#/summary",  # 2022?
        "https://results.enr.clarityelections.com/AR/113429/277746/en/summary.html",
    ]
    
    print("Testing Arkansas Clarity URLs:\n")
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✓ Found: {url}")
                print(f"  Status: {response.status_code}")
                
                # Try to create a Jurisdiction object
                try:
                    j = clarify.Jurisdiction(url=url, level='state')
                    print(f"  Election: {j.report_url('xml') if hasattr(j, 'report_url') else 'N/A'}")
                except Exception as e:
                    print(f"  Clarify error: {e}")
            else:
                print(f"✗ Not found: {url} (Status: {response.status_code})")
        except Exception as e:
            print(f"✗ Error accessing {url}: {e}")
        print()

if __name__ == '__main__':
    find_ar_elections()
