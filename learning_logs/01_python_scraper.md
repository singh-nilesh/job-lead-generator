# AIM: Build a python scraper for Intershala.
## Requirements:
1. Scrape Job postings from Intershala, and save it to local **jobs.csv** file.
1. Follow **Object-oriented** programing concepts, and industry standards.
    - Use classes to encapsulate functionality.
    - project as a package.(setup.py)
    - Use **logging** to log the scraping process.
    - Use **config** file to store configurations.
    - Use **virtual environment** to manage dependencies.


1. Scrape based on the following filters( Configs ):
- **Job type**: Internship
- **Work mode**: Work from home (Remote)
- **Location**: Mumbai
- **Role**: Machine learning
- **Experience required**: 0 years
- **Stipend**: Minimum ₹5000
- **Salary (LPA)**: ₹5 LPA (for jobs, if applicable)
- **Timeout**: 5 seconds
- **Headers**: Custom User-Agent set
- **Base URL**: [https://internshala.com](https://internshala.com)


## Guides and Suggestions:
- The **Source Urls** change based on the filters, so you will need to construct the URL dynamically based on the configuration.
- First page of the search **Url** returns list of jobs, you can inspect and find the source Urls for respective Job in the individual job postings cards.
- use `BeautifulSoup` to parse the HTML and extract the list of **Job Urls**.
then use those URLs to scrape individual job details.
- The intershala website has a specific structure for job postings, so inspect the HTML to identify the elements you need to scrape.
- Use libraries like `requests`, `BeautifulSoup`, as scraping client.
- You should stick to using CSS selectors for scraping, as they are more robust and easier to maintain than XPath.
- The `Robots.txt` usually prevents scraping, through 
    1. IP blocking
    1. Rate limiting
    1. User-agent blocking
- Use `logging` to log the scraping process, including any errors or exceptions, very helpful for debugging.


## Learning Outcomes:

- How to scrape data from a website using Python and BeautifulSoup.
- Configure and use logger for debugging and tracking.
- How to structure a Python project using object-oriented programming principles.