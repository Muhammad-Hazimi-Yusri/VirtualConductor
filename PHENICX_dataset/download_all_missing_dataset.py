# This script uses Playwright to automate the download of a datapack from the Repovizz fragment page.
# Make sure you have Playwright installed and set up: pip install playwright && playwright install

import os
from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup
import re

RAW_EXAMPLE_DIR = os.path.join(os.path.dirname(__file__), 'raw_example')
os.makedirs(RAW_EXAMPLE_DIR, exist_ok=True)

# You can update this with any Repovizz fragment link you want to test
test_repovizz_url = 'https://repovizz.upf.edu/repo/Vizz/232?startTime=0&secsToShow=40'

# List of all subject/fragment combinations
NUM_SUBJECTS = 25
NUM_FRAGS = 3
SUBJECTS = [f"subject{str(i).zfill(2)}" for i in range(1, NUM_SUBJECTS+1)]
FRAGS = [f"frag{str(i).zfill(2)}" for i in range(1, NUM_FRAGS+1)]

# Helper to check if a dataset zip is already downloaded (ignore the random part after take03_)
def is_downloaded(subject, frag, out_dir):
    prefix = f"{subject}_{frag}_take03_"
    for fname in os.listdir(out_dir):
        if fname.startswith(prefix) and fname.endswith('.zip'):
            return True
    return False

# The download will be triggered by clicking the 'Download Datapack (all streams)' button
def download_datapack(repovizz_url, download_dir):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        # Handle the confirmation dialog
        def handle_dialog(dialog):
            print(f"Dialog message: {dialog.message}")
            dialog.accept()
        page.on("dialog", handle_dialog)

        page.goto(repovizz_url)
        page.wait_for_selector('a:has-text("Share")', timeout=10000)
        page.click('a:has-text("Share")', force=True)
        page.wait_for_timeout(1000)
        with page.expect_download() as download_info:
            page.click('a[href="javascript:downloadCompleteDatapack()"]', force=True)
        download = download_info.value
        zip_path = os.path.join(download_dir, download.suggested_filename)
        download.save_as(zip_path)
        print(f'Downloaded: {zip_path}')
        browser.close()

def extract_repovizz_fragment_links(html_path=None):
    from playwright.sync_api import sync_playwright
    if html_path:
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
    else:
        url = "https://www.upf.edu/web/mtg/phenicx-conduct-dataset"
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # Open browser window
            page = browser.new_page()
            page.goto(url)
            print("Please solve any CAPTCHA or Cloudflare challenge in the opened browser window.")
            input("Press Enter here after the dataset page is fully loaded and visible...")
            html = page.content()
            with open("repovizz_debug.html", "w", encoding="utf-8") as f:
                f.write(html)
            browser.close()
    soup = BeautifulSoup(html, "html.parser")
    # Print all tags containing '[Chapter 4]' for debug
    chapter4_candidates = []
    for tag in soup.find_all(True):
        if '[Chapter 4]' in tag.get_text():
            print(f"Found candidate tag: <{tag.name}> {tag.get_text(strip=True)[:80]}")
            chapter4_candidates.append(tag)
    chapter4 = None
    for tag in chapter4_candidates:
        if tag.get_text(strip=True).startswith('[Chapter 4]'):
            chapter4 = tag
            break
    if not chapter4 and chapter4_candidates:
        chapter4 = chapter4_candidates[0]  # fallback to first candidate
    if not chapter4:
        raise RuntimeError("Could not find Chapter 4 heading or marker in any tag. See repovizz_debug.html for page dump.")

    # Find the table after Chapter 4
    table = chapter4.find_next('table')
    if not table:
        # Sometimes the table is rendered as HTML lists or divs, fallback to searching all links after Chapter 4
        links = []
        node = chapter4
        while node:
            node = node.find_next()
            if node and node.name == 'a' and node.get('href', '').startswith('http://repovizz.upf.edu/repo/Vizz/'):
                links.append(node)
            # Stop if we reach Chapter 5 or another major heading
            if node and node.name in ['h2', 'h3', 'h4', 'h5', 'h6'] and '[Chapter 5]' in node.get_text():
                break
        if len(links) != 75:
            raise RuntimeError(f"Expected 75 Repovizz links, found {len(links)}")
        # Map links to (participant, fragment)
        mapping = {}
        for i, link in enumerate(links):
            participant = i // 3 + 1
            fragment = i % 3 + 1
            mapping[(participant, fragment)] = link['href']
        return mapping
    else:
        # Table found, parse rows
        rows = table.find_all('tr')[1:]  # skip header
        mapping = {}
        for i, row in enumerate(rows):
            cols = row.find_all(['td', 'th'])
            if len(cols) < 2:
                continue
            participant = int(cols[0].get_text(strip=True))
            frag_links = cols[1].find_all('a')
            for frag_idx, link in enumerate(frag_links):
                mapping[(participant, frag_idx+1)] = link['href']
        if len(mapping) != 75:
            raise RuntimeError(f"Expected 75 Repovizz links, found {len(mapping)}")
        return mapping

# Example usage: print(extract_repovizz_fragment_links())
if __name__ == '__main__':
    # Automatically extract all Repovizz URLs for Chapter 4 (25x3)
    mapping = extract_repovizz_fragment_links()
    # Convert mapping keys to (subjectXX, fragYY) for compatibility
    repovizz_urls = {}
    for (participant, fragment), url in mapping.items():
        subject = f"subject{participant:02d}"
        frag = f"frag{fragment:02d}"
        repovizz_urls[(subject, frag)] = url

    for subject in SUBJECTS:
        for frag in FRAGS:
            key = (subject, frag)
            if key not in repovizz_urls:
                print(f"No Repovizz URL for {subject} {frag}, skipping.")
                continue
            if is_downloaded(subject, frag, RAW_EXAMPLE_DIR):
                print(f"Already downloaded: {subject}_{frag}_take03_*.zip")
                continue
            print(f"Downloading: {subject} {frag}")
            download_datapack(repovizz_urls[key], RAW_EXAMPLE_DIR)
