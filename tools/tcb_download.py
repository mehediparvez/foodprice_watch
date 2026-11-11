"""
Download all Excel files from TCB Daily Retail Market Prices (pages 1-15)
and save them into:  Downloads/TCB_Daily_RMP

* Uses only Python's built-in libraries - nothing to install.
* RESUMES: links already downloaded are remembered in _done_links.txt and
  skipped instantly, so if the internet drops you just run it again.
* Retries automatically when the connection fails.
* Half-downloaded files are never kept (saved as .part, renamed when complete).
"""

import os
import re
import ssl
import time
import zipfile
import urllib.request
import urllib.error
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, unquote

# ---------------- settings ----------------
BASE_URL = "https://tcb.gov.bd/pages/daily-rmps?page={page}&page_size=100"
FIRST_PAGE = 1
LAST_PAGE = 15
SAVE_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads", "TCB_Daily_RMP")
DELAY_SECONDS = 1      # pause between downloads, to be polite to the server
RETRIES = 6            # attempts per request before giving up on it
# ------------------------------------------

DONE_LOG = os.path.join(SAVE_FOLDER, "_done_links.txt")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}
EXCEL_RE = re.compile(r"\.(xlsx|xls|xlsm|csv)(\?|$)", re.IGNORECASE)

UNVERIFIED = ssl.create_default_context()
UNVERIFIED.check_hostname = False
UNVERIFIED.verify_mode = ssl.CERT_NONE


def open_url_once(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        return urllib.request.urlopen(req, timeout=60)
    except urllib.error.URLError as e:
        if isinstance(getattr(e, "reason", None), ssl.SSLError):
            return urllib.request.urlopen(req, timeout=60, context=UNVERIFIED)
        raise


def with_retries(action, what):
    """Run action(); on network errors wait and try again."""
    for attempt in range(1, RETRIES + 1):
        try:
            return action()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise
            err = e
        except Exception as e:  # timeouts, connection reset, no internet...
            err = e
        wait = min(60, 5 * attempt)
        print(f"   network problem ({err}); retry {attempt}/{RETRIES} in {wait}s...")
        time.sleep(wait)
    raise RuntimeError(f"gave up on {what}")


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href.strip())


def find_excel_links(page_url):
    def fetch():
        with open_url_once(page_url) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    html = with_retries(fetch, page_url)
    parser = LinkParser()
    parser.feed(html)
    links = []
    for href in parser.links:
        full = urljoin(page_url, href)
        if EXCEL_RE.search(full) or "download" in href.lower():
            links.append(full)
    return list(dict.fromkeys(links))


def filename_from(resp, url):
    cd = resp.headers.get("Content-Disposition", "") or ""
    m = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)"?', cd)
    if m:
        name = unquote(m.group(1))
    else:
        name = unquote(os.path.basename(urlparse(url).path)) or "file.xlsx"
    return re.sub(r'[\\/:*?"<>|]', "_", name)


def is_complete(path):
    """A finished .xlsx is a valid zip file; a cut-off download is not."""
    if path.lower().endswith((".xlsx", ".xlsm")):
        return zipfile.is_zipfile(path)
    return os.path.getsize(path) > 0


def download(url):
    """Returns 'saved', 'exists' or 'skipped'."""
    def fetch():
        with open_url_once(url) as resp:
            name = filename_from(resp, url)
            if not EXCEL_RE.search(name):
                ctype = resp.headers.get("Content-Type", "") or ""
                if "sheet" not in ctype and "excel" not in ctype:
                    return "skipped", name
            path = os.path.join(SAVE_FOLDER, name)
            if os.path.exists(path) and is_complete(path):
                return "exists", name
            tmp = path + ".part"
            with open(tmp, "wb") as f:
                while True:
                    chunk = resp.read(65536)
                    if not chunk:
                        break
                    f.write(chunk)
            if not is_complete(tmp):
                os.remove(tmp)
                raise IOError("download was cut off")
            os.replace(tmp, path)
            return "saved", name
    return with_retries(fetch, url)


def load_done():
    if not os.path.exists(DONE_LOG):
        return set()
    with open(DONE_LOG, encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


def mark_done(url):
    with open(DONE_LOG, "a", encoding="utf-8") as f:
        f.write(url + "\n")


def main():
    os.makedirs(SAVE_FOLDER, exist_ok=True)
    for f in os.listdir(SAVE_FOLDER):           # clean leftovers from a crash
        if f.endswith(".part"):
            os.remove(os.path.join(SAVE_FOLDER, f))
    done = load_done()
    print(f"Saving files to: {SAVE_FOLDER}")
    earlier = len(done)
    print(f"Already finished earlier: {earlier} link(s)\n")

    saved = exists = skipped = failed = 0
    for page in range(FIRST_PAGE, LAST_PAGE + 1):
        page_url = BASE_URL.format(page=page)
        print(f"Page {page}: {page_url}")
        try:
            links = find_excel_links(page_url)
        except Exception as e:
            print(f"   could not open page: {e}")
            failed += 1
            continue

        todo = [l for l in links if l not in done]
        print(f"   found {len(links)} link(s), {len(todo)} still to download")
        for link in todo:
            try:
                result, name = download(link)
                if result == "saved":
                    saved += 1
                    print(f"   saved: {name}")
                    time.sleep(DELAY_SECONDS)
                elif result == "exists":
                    exists += 1
                else:
                    skipped += 1
                    print(f"   skipped (not Excel): {name}")
                mark_done(link)
                done.add(link)
            except Exception as e:
                failed += 1
                print(f"   FAILED: {link} -> {e}")

    print("\n============ SUMMARY ============")
    print(f"New files saved    : {saved}")
    print(f"Done in earlier runs: {earlier}")
    print(f"Already on disk    : {exists}")
    print(f"Skipped (not Excel): {skipped}")
    print(f"Failed             : {failed}")
    if failed:
        print("\nSome downloads failed - just run the script again to retry them.")
    input("\nPress Enter to close...")


if __name__ == "__main__":
    main()
