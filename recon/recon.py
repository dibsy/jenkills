import requests
import json
import sys
import colorama
import argparse
import logging

from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


banner = '''

░░░░░██╗███████╗███╗░░██╗██╗░░██╗██╗██╗░░░░░██╗░░░░░░██████╗
░░░░░██║██╔════╝████╗░██║██║░██╔╝██║██║░░░░░██║░░░░░██╔════╝
░░░░░██║█████╗░░██╔██╗██║█████═╝░██║██║░░░░░██║░░░░░╚█████╗░
██╗░░██║██╔══╝░░██║╚████║██╔═██╗░██║██║░░░░░██║░░░░░░╚═══██╗
╚█████╔╝███████╗██║░╚███║██║░╚██╗██║███████╗███████╗██████╔╝
░╚════╝░╚══════╝╚═╝░░╚══╝╚═╝░░╚═╝╚═╝╚══════╝╚══════╝╚═════╝░
'''

LOG_FILE = 'analysis-lite.log'
IP_LIST_FILE = ''

logging.basicConfig(filename=LOG_FILE,level=logging.INFO)

def checkAdminPermission(content,url):
    try:
        if "/manage" in content:
          logging.info("Administrative Prilileges Found on "+url)
    except:
         logging.info("Error in checkAdminPermission while parsing "+url)
    
def parse_for_users(jsonString):         
    try:
            jsonDict = json.loads(jsonString)
            users  = jsonDict["users"]
            for user in users:
                 logging.info(user["user"]["fullName"])

    except:          
            pass

def check_for_builtin_executor(jsonString,url):    
    try:
            jsonDict = json.loads(jsonString)
            executor  = int(jsonDict["numExecutors"])
            if executor>0:
                 logging.info("Jobs can run on Built-In Node on "+url)

    except:          
            logging.info("Error in check_for_builtin_executor while parsing "+url)
    
def parse_for_domains(jsonString):
    try:
        jsonDict = json.loads(jsonString)
        error = 0
        try:
            logging.info(jsonDict["url"])
        except:
            error=1
            pass

        if error == 0:
            return

        try:
            
            logging.info(jsonDict["views"][0]["url"])
        except:
            pass
    except:
        logging.info("JSON parsing error")

def parse_for_jobs_info(jsonString):
    jsonDict = json.loads(jsonString)
    '''
        It will take a long time to scan all the Pipelines when you have large set of IP
        For the demo purpose I am setting it to 2 at MAX but there can be projects with different kind of privileges
    '''

    try:
            jobs  = jsonDict["jobs"]
            #logging.info(jobs)
            counter = 0
            for job in jobs:
                if counter == 2:
                    break

                job_url = job["url"]
                build_url = job_url+"api/json"
                data_jobs = ''
                data_build = ''

                logging.info("Trying job "+job_url)
                if "https" in job_url:
                    data_jobs = get_https_html_data(job_url)
                    jsonString = get_https_json_data(build_url)
                    jsonDict = json.loads(jsonString)
                    last_build_url = jsonDict["lastBuild"]["url"]
                    logging.info("Last Build URL "+last_build_url)
                    data_build = get_https_html_data(last_build_url)

                else:
                    data_jobs = get_http_html_data(job_url)
                    jsonString = get_http_json_data(build_url)
                    jsonDict = json.loads(jsonString)
                    last_build_url = jsonDict["lastBuild"]["url"]
                    logging.info("Last Build URL "+last_build_url)
                    data_build = get_http_html_data(last_build_url)


                if "/configure" in data_jobs:
                    logging.info("Jobs can be configured for "+job_url)
                
                if "Replay" in data_build:
                    logging.info("Builds can be replayed "+last_build_url)


                counter +=1 
    except:          
            logging.info("Error in parse_for_jobs_info "+str(sys.exc_info()[0]))   



def get_https_json_data(url):
    try:
        resp = requests.get(url,timeout=3,verify=False)
        jsonObj = json.dumps(resp.json())
        return jsonObj
    except:
        logging.info("Error in get_https_json_data "+sys.exc_info()[0])
        return '{}'

def get_https_html_data(url):
    try:
        resp = requests.get(url,timeout=3,verify=False)
        return resp.text
    except:
        logging.info("Error in get_https_html_data "+sys.exc_info()[0])
        return '<>'


def get_http_json_data(url):
    try:
        resp = requests.get(url,timeout=3,verify=False)
        jsonObj = json.dumps(resp.json())
        return jsonObj
    except:
        logging.info("Error in get_http_json_data "+sys.exc_info()[0])
        return '{}'

def get_http_html_data(url):
    try:
        resp = requests.get(url,timeout=3,verify=False)
        return resp.text
    except:
        logging.info("Error in get_http_json_data "+sys.exc_info()[0])
        return '<>'



def process():
    with open(IP_LIST_FILE) as fobj:
        ips = fobj.readlines()
        
        for ip in ips:
            error=0
            logging.info(ip)

            try:
                
                url = "https://"+ip+"/api/json"
                jsonObj = get_https_json_data(url)   

                parse_for_domains(jsonObj)                
                check_for_builtin_executor(jsonObj)
                parse_for_jobs_info(jsonObj)


                url = "https://"+ip+"/asynchPeople/api/json"
                jsonObj = get_https_json_data(url)
                parse_for_users(jsonObj)


                url = "https://"+ip
                content = get_https_html_data(url)
                checkAdminPermission(content)              
                                
            except:
                error = 1

            
            try:
                url = "http://"+ip+"/api/json"
                jsonObj = get_http_json_data(url)
                
                parse_for_domains(jsonObj)
                check_for_builtin_executor(jsonObj,url)
                parse_for_jobs_info(jsonObj)

                url = "http://"+ip+"/asynchPeople/api/json"
                jsonObj = get_http_json_data(url)
                parse_for_users(jsonObj)

                url = "http://"+ip
                content = get_http_html_data(url)
                checkAdminPermission(content,url)                           
            except:
                logging.info("Error "+str(sys.exc_info()[0]))
            logging.info("#"*50)
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recon Jenkins')
    parser.add_argument('--logfile')
    parser.add_argument('--iplist',required=True)
    parser.add_argument('--max-pipeline-checks')
    parser.add_argument('--max-jobs-checks')
    args = parser.parse_args()

    if not args.iplist:
        print("Please provide an input file containing ip address in format IP:PORT")
    else:
        IP_LIST_FILE = args.iplist
    if args.logfile:
        LOG_FILE = args.logfile

    print(banner)
    print("[+] Reading IP:PORT from "+IP_LIST_FILE)
    print("[+] Storing the logs in "+LOG_FILE)
    process()
    
