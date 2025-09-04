
from src.core.config import ScraperConfig
from src.core.logger import scraper_logger as logger

def compile_url(cfg:ScraperConfig) -> list[str]:
    """
    Compile source URLs for both internships and jobs based on configuration.
    Args:
        cfg (ScraperConfig): Configuration object containing search parameters
        
    Returns:
        List[str]: List of generated URLs for searching internships and/or jobs
    """
    logger.info(" init Compiling source URLs for Job and Internsips")
    url_list = []
    if cfg.internship :
        url_list.append(_build_internship_url(cfg))
    
    if cfg.job:
        url_list.append(_build_job_url(cfg))
    
    if not len(url_list) > 0:
        logger.error("No links compiled, Check The config file for issue.") 
    return url_list

def _build_internship_url(cfg:ScraperConfig):
    """
    Construct a search URL for internships based on configuration parameters.
    
    Args:
        cfg (ScraperConfig): Configuration object containing search parameters
        
    Returns:
        Optional[str]: A fully formed URL for internship search, or None if internship search is not enabled
    """
    logger.info(" Building Internship base url")
    if not cfg.remote:
        return

    segments = []
    # base URL
    segments.append(str(cfg.base_urls["internshala"]+"/internships/"))
    
    # construct mid segment
    roles = ",".join(cfg.roles) if cfg.roles else None
    locations = "in-" + ",".join(cfg.locations) if cfg.locations else None
    if cfg.remote:
        parts = ['work-from-home', roles, 'internships', locations]
    
    elif cfg.part_time:
        if roles:
            parts = ['part-time', roles,'jobs', locations]
        else:
            parts = ['part-time-jobs', locations]
            
    elif roles or locations:
        parts = [roles, 'internship', locations]
    else:
        parts = []
    # Remove None values and append
    mid_seg = "-".join(part for part in parts if part) + "/" if parts else None
    if mid_seg:
        segments.append(mid_seg)
        
        
    # Partime
    if(cfg.remote and cfg.part_time):
        segments.append("part-time-true/")
    
    # stipend
    stipend = ['', '2000', '4000', '6000', '8000', '10000']
    if(int(cfg.min_stipend) >= 2000):
        index = int(eval(f'{cfg.min_stipend} / 2000'))
        segments.append("stipend-" + stipend[index if index < 6 else 5])
    
    url = "".join(segments) + "/"
    final_url = url.replace(' ', '-').lower()
    logger.info(f"Finished compling base URL, {final_url}")
    return final_url


def _build_job_url(cfg:ScraperConfig):
    """
    Construct a search URL for jobs based on configuration parameters.
    
    Args:
        cfg (ScraperConfig): Configuration object containing search parameters
        
    Returns:
        Optional[str]: A fully formed URL for job search, or None if job search is not enabled
                      
    Note:
        The URL structure adapts based on experience level, directing to either regular jobs or fresher jobs endpoints
    """
    logger.info("Building Jobs Base URL")
    if not cfg.job:
        return
    
    segments = []
    
    if cfg.experience_years < 1: exp = 0
    elif cfg.experience_years > 5: exp = 2
    else: exp = 1
    
    # base URL
    segments.append(cfg.base_urls["internshala"])
    segments.append(str("/jobs/" if exp != 0 else "/fresher-jobs/"))
    
    # construct mid segment
    roles = ",".join(cfg.roles) if cfg.roles else None
    locations = "in-" + ",".join(cfg.locations) if cfg.locations else None
    if cfg.part_time:
        parts = ['part-time', roles, 'jobs', locations]
    elif roles or locations:
        parts = [roles, 'jobs', locations]
    else:
        parts = []
        
    # Remove None values and append
    mid_seg = "-".join(part for part in parts if part) + "/" if parts else None
    if mid_seg:
        segments.append(mid_seg)
        
    # remote
    if(cfg.remote):
        segments.append("work-from-home/")
    
    # Experience
    if exp == 1:
        segments.append("experience-" + str(int(cfg.experience_years)) + "/")
    elif exp == 2:
        segments.append("experience-5plus/")
        
    # package, in Lpa
    salary = ['', '2', '4', '6', '8', '10']
    if(int(cfg.min_salary) >= 2):
        index = int(eval(f'{cfg.min_salary} / 2'))
        segments.append("salary-" + salary[index if index < 6 else 5])
    
    url = "".join(segments) + "/"
    final_url = url.replace(' ', '-').lower()
    logger.info(f"Finished compling base URL, {final_url}")
    return final_url