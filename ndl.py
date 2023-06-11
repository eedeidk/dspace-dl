from bs4 import BeautifulSoup as bs
import os, requests, time
from urllib.parse import urlparse, urljoin
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from datetime import datetime


def make_session():
	session = requests.Session()
	session.headers.update({
		'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/000000000 Safari/537.36'
	})
	session.verify = False
	return session

def get_page(url:str):
	session = make_session()
	time.sleep(1)
	r = session.get(url, verify=False)
	# check content type
	content_type = r.headers.get('Content-Type')
	if not content_type or 'text/html' not in content_type:
		print(url, content_type)
		return None, None
	else:
		url_p = urlparse(url)
		# print(url_p)
		parent_url = str(url_p.scheme)+'://'+str(url_p.hostname)
		# print(parent_url)
		r.raise_for_status()
		return parent_url, r.text

def check_if_page_dspace_generated(soup:bs):
	table= soup.find('table')
	# table2= soup.find('table', summary='This table browses all dspace content')
	if not table:
		# print('Not DSpace generated')
		return False
	else:
		# print('DSpace generated')
		return table

def extract_links(soup:bs, parent_url:str):
	targ = soup.find('div', class_='col-md-12')
	targets = targ.find_all('h4', class_='list-group-item-heading')
	# print(targ.prettify())
	all_elems = []
	all_elems_link = []
	for each in targets:
		elems = each.get_text(strip=True)
		elems_link = parent_url + str(each.a['href'])
		print(elems, elems_link)
		wfile(fname, f'{elems} : {elems_link}')
		all_elems.append(elems)
		all_elems_link.append(elems_link)
	return all_elems, all_elems_link

def parse_page(parent_url:str, resp:str):
	soup = bs(resp, 'lxml')
	## check if dspace content:
	if check_if_page_dspace_generated(soup)== False:
		un, ul = extract_links(soup, parent_url)
		ds = False
	else:
		un, ul = parse_table(soup, parent_url)
		ds = True
	return un, ul, ds

def parse_table(soup:bs, parent_url:str):
	uname = []
	ulist = []
	table = soup.find('table', summary='This table browses all dspace content')
	# next page feature missing
	if table:
		rows = table.find_all('tr')
		for row in rows:
			cols = row.find_all('td', headers='t2')
			names = [ele.text.strip() for ele in cols]
			urls = [ele.a['href'] for ele in cols]
			for name in names:
				if not name=='':
					uname.append(name)
			for url in urls:
				if not url=='':
					ulist.append(parent_url + url)
		# print(uname, ulist)
	else:
		table = soup.find('table', class_='table panel-body')
		td = table.find('td', headers='t1')
		uname.append(td.text.strip())
		ulist.append(parent_url + td.a['href'])
		usize = table.find('td', headers='t3').text.strip()
		print(f'{uname[0]} - {usize} - {ulist[0]}')
		wfile(fname,  f'{ulist[0]}')
		# input('Enter to continue')
	return uname, ulist

def loopme(url:str):
	parent_url, response = get_page(url)
	# check if the url is not to any file
	if not parent_url == None:
		uname, ulist, ds = parse_page(parent_url, response)
		return uname, ulist

def wfile(filename:str, data:str):
	with open(filename, 'a') as f:
		f.writelines(data+'\n')


fname = datetime.now().strftime("%Y%m%d-%H%M%S") + '.txt'
print(fname)

def main():
	names = ['Entered']
	urls = [input("Enter Webpage to search for links: ")]
	while urls:
		url = urls.pop(0)
		name = names.pop(0)
		print(name)
		# wfile(fname, name+'\n===')
		un, ul = loopme(url)
		if ul:
			for each in ul:
				urls.append(each)
			for each in un:
				names.append(each)
				# for i in range(len(ul)):
				# 	print(un[i])
				# 	wfile(fname,  un[i])
				# 	name3, link3 = loopme(ul[i])
				# 	for each in link3:
				# 		urls.append(each)

if __name__ == '__main__':
	main()