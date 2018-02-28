#!/usr/bin/env python
import requests
from random import randint
import os
import argparse
import json
from datetime import datetime
from urllib3.exceptions import MaxRetryError
# import pprint


def send_catfacts(catfacts_file, webhook_url):
	""" Attempts to post to Slack webhook url to post catfact.
	
	catfacts_file -- str (path to catfacts file)
	webhook_url	-- str (Slack webhook url)
	"""
	payload = {"text": fetch_random_catfact(catfacts_file)}
	try:
		r = requests.post(webhook_url, 
						  data=json.dumps(payload),
						  headers={'Content-Type': 'application/json'}
						  )
	except (MaxRetryError, requests.exceptions.ConnectionError):
		proxies = {
				"http":"http://proxy-us.intel.com:911", 
				"https": "http://proxy-us.intel.com:911"
			  }
		r = requests.post(webhook_url, 
						  data=json.dumps(payload),
						  headers={'Content-Type': 'application/json'},
						  proxies=proxies
						  )
	print("\t{time} -- Status code was {code}\n".format(time=datetime.now(),code=r.status_code))


def fetch_random_catfact(catfacts_file):
	""" Fetch random cat fact from catfacts_file, remove that line, 
	and rewrite remaining lines to file.
	
	catfacts_file -- path to catfacts file
	"""
	with open(catfacts_file, "r", encoding="utf-8") as f:
		lines = f.readlines()
		if lines:
			index = randint(0, len(lines))
			catfact = lines[index]
			# del lines[index]
			# f.writelines(lines)
			return catfact
		

def get_all_catfacts():
	""" Attempts to fetch catfacts. If the request fails, 
	tries again with proxies.
	"""
	proxies = {
				"http":"http://proxy-us.intel.com:911", 
				"https": "http://proxy-us.intel.com:911"
			  }
	r = try_querying_catfacts()
	if not r:
		r = try_querying_catfacts(proxies)
		if not r:
			raise requests.exceptions.RequestException("Unable to fetch catfacts. Aborting.")
	# pp = pprint.PrettyPrinter(indent=4)
	# pp.pprint(r.text)
	with open("c:/Users/wboyerx/Desktop/catfacts.txt", "w+", encoding="utf-8") as f:
		try:
			for x in json.loads(r.text)['data']:
				f.write(str(x['fact']) + '\n')
		except KeyError:
			raise KeyError("Expected results from /facts query (multiple records), "
						   "not a singleton /fact.")


def try_querying_catfacts(proxies={"http":"", "https": ""}, limit=500):
	""" Given a dict of http and https proxies, attempt to fetch catfacts.
	proxies -- dict
	
	Returns: requests object or None
	"""
	try:
		r = requests.get("https://catfact.ninja/facts?limit={limit}".format(limit=limit), proxies=proxies)
	except requests.exceptions.RequestException as e:
		return None
	else:
		return r


def nonempty_catfacts_file(catfacts_file):
	""" Path must both refer to a file, and that file must be nonempty.

	catfacts_file -- str (refers to path of catfacts file)
	
	Returns: boolean
	"""
	
	try:
		return os.path.isfile(catfacts_file) and (os.path.getsize(catfacts_file) > 0)
	except OSError:
		return False

			
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="The dumbest, most overwrought script you've ever seen.")
	parser.add_argument("-f", "--filename", type=str, default="c:/Users/wboyerx/Desktop/catfacts.txt", help="Full path to file containing catfacts, one per newline.")
	parser.add_argument("-w", "--webhook", type=str, default="https://hooks.slack.com/services/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", help="Link to slack webhook.")
	args = parser.parse_args()
	
	if not nonempty_catfacts_file(args.filename):
		print("Catfacts file is empty; attempting to fetch complete list of available catfacts.")
		get_all_catfacts()
	
	send_catfacts(args.filename, args.webhook)