import requests
import feedparser
import os
import certifi

def search_arxiv_paper():
    # -------------------------------
    # 1️⃣ Define broad Computer Science query
    # -------------------------------
    # "cat:cs.*" matches all computer science categories
    search_query = "cat:cs.*"
    max_results = 1  # number of papers to fetch
    sort_by = "submittedDate"
    sort_order = "descending"

    # -------------------------------
    # 2️⃣ Build the API URL
    # -------------------------------
    base_url = "https://export.arxiv.org/api/query"
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": sort_by,
        "sortOrder": sort_order
    }

    # -------------------------------
    # 3️⃣ Fetch data from arXiv
    # -------------------------------
    response = requests.get(base_url, params=params, verify=certifi.where())
    feed = feedparser.parse(response.text)

    # -------------------------------
    # 4️⃣ Display latest papers
    # -------------------------------
    # for i, entry in enumerate(feed.entries, start=1):
    #     print(f"📘 {i}. {entry.title}")
    #     print(f"👨‍🔬 Authors: {', '.join(author.name for author in entry.authors)}")
    #     print(f"📅 Published: {entry.published}")
    #     print(f"📝 Summary: {entry.summary[:300]}...")
    #     print(f"🔗 PDF: {entry.id.replace('abs', 'pdf')}\n")
    #     print("--------------------------------------------------")
    
    
    # -------------------------------
    # 4️⃣ Download latest papers
    # -------------------------------
    for i, entry in enumerate(feed.entries, start=1):
        download_arxiv_paper(entry, download_dir="arxiv_papers")
        

def download_arxiv_paper(entry, download_dir="arxiv_papers"):
    """Download a single arXiv paper PDF efficiently."""
    os.makedirs(download_dir, exist_ok=True)
    title = entry.title.replace("/", "-").replace(":", "-")
    pdf_url = entry.id.replace("abs", "pdf") + ".pdf"
    file_path = os.path.join(download_dir, f"{title}.pdf")

    print(f"🔗 Downloading: {pdf_url}")

    try:
        with requests.get(pdf_url, stream=True, timeout=60, verify=certifi.where()) as r:
            r.raise_for_status()
            with open(file_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"✅ Saved: {file_path}\n")
    except requests.exceptions.SSLError:
        print("⚠️ SSL verification failed, retrying without verification (not recommended for production)...")
        try:
            with requests.get(pdf_url, stream=True, timeout=60, verify=certifi.where()) as r:
                r.raise_for_status()
                with open(file_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            print(f"✅ Saved (insecure mode): {file_path}\n")
        except Exception as e:
            print(f"❌ Failed to download {pdf_url}: {e}\n")
    except Exception as e:
        print(f"❌ Failed to download {pdf_url}: {e}\n")


if __name__ == "__main__":
    search_arxiv_paper()



