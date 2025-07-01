import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://hac.friscoisd.org"

class HACClient:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.client = httpx.Client(follow_redirects=True)

    def login(self):
        login_url = f"{BASE_URL}/HomeAccess/Account/LogOn"
        r = self.client.get(login_url)
        soup = BeautifulSoup(r.text, "html.parser")

        viewstate = soup.find("input", {"name": "__VIEWSTATE"})["value"]
        viewstategen = soup.find("input", {"name": "__VIEWSTATEGENERATOR"})["value"]
        eventvalidation = soup.find("input", {"name": "__EVENTVALIDATION"})["value"]

        login_data = {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": viewstate,
            "__VIEWSTATEGENERATOR": viewstategen,
            "__EVENTVALIDATION": eventvalidation,
            "LogOnDetails.UserName": self.username,
            "LogOnDetails.Password": self.password,
            "btnLogOn": "Log On"
        }
        login_resp = self.client.post(login_url, data=login_data)
        if "Log On" in login_resp.text:
            raise Exception("Login failed: check credentials")

    def get_transcript_grades(self):
        self.login()
        url = f"{BASE_URL}/HomeAccess/Grades/Transcript"
        r = self.client.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        grades = []
        rows = soup.select("table#plnMain_dgdTranscript tr")[1:]  # Skip header row
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 5:
                grades.append({
                    "school_year": cells[0].text.strip(),
                    "term": cells[1].text.strip(),
                    "course": cells[2].text.strip(),
                    "grade": cells[3].text.strip(),
                    "credits": cells[4].text.strip(),
                })
        return grades

    def get_test_scores(self):
        self.login()
        url = f"{BASE_URL}/HomeAccess/Grades/TXTestScores"
        r = self.client.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        scores = []
        rows = soup.select("table#plnMain_dgTestScores tr")[1:]
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 6:
                scores.append({
                    "year": cells[0].text.strip(),
                    "test": cells[1].text.strip(),
                    "subject": cells[2].text.strip(),
                    "scale_score": cells[3].text.strip(),
                    "performance_level": cells[4].text.strip(),
                    "met_standard": cells[5].text.strip(),
                })
        return scores

    def get_demographics(self):
        self.login()
        url = f"{BASE_URL}/HomeAccess/Registration/Demographic"
        r = self.client.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        demographics = {}
        rows = soup.select("table#plnMain_dgDemographics tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) == 2:
                key = cells[0].text.strip().replace(":", "")
                val = cells[1].text.strip()
                demographics[key] = val
        return demographics

    def get_classwork(self):
        self.login()
        url = f"{BASE_URL}/HomeAccess/Classes/Classwork"
        r = self.client.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        classwork = []
        rows = soup.select("table#plnMain_dgdClasswork tr")[1:]
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 6:
                classwork.append({
                    "date": cells[0].text.strip(),
                    "assignment": cells[1].text.strip(),
                    "category": cells[2].text.strip(),
                    "class": cells[3].text.strip(),
                    "score": cells[4].text.strip(),
                    "total": cells[5].text.strip(),
                })
        return classwork

    def get_school_links(self):
        self.login()
        url = f"{BASE_URL}/HomeAccess/Home/SchoolLinks"
        r = self.client.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        links = []
        anchors = soup.select("table#plnMain_dgSchoolLinks a")
        for a in anchors:
            text = a.text.strip()
            href = a.get("href")
            links.append({"text": text, "url": href})
        return links
