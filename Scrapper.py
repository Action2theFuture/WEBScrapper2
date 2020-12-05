import requests
from bs4 import BeautifulSoup

def get_last_page(URL):
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extra_job(html):
    title = html.find("h2", {"class": "fs-body3"}).find("a")["title"]
    company, location = html.find("h3", {
        "class": "fs-body1"
    }).find_all(
        "span", recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id = html["data-jobid"]
    return {
        "title": title,
        "company": company,
        "location": location,
        "apply_link": f"https://stackoverflow.com/jobs/{job_id}"
    }


def extra_jobs(last_page, URL):
    jobs = []
    for page in range(last_page):
        print(f"Scrappingpage SO : {page}")
        result = requests.get(f"{URL}?pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extra_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    URL = f"https://stackoverflow.com/jobs?q={word}&sort=1"
    last_page = get_last_page(URL)
    jobs = extra_jobs(last_page, URL)
    return jobs
