import requests
from bs4 import BeautifulSoup
import unittest

class Work(object):
	def __init__(self, work_id, work_name, chapter_text_ls):
		self.work_id = work_id
		self.work_name = work_name
		self.chapter_text_ls = chapter_text_ls
		self.chapter_count = len(self.chapter_text_ls)

	#Helper function to fetch the html of a work from the internet
	@staticmethod
	def get_work_html(work_id):
		#the url for the webpage of all chapters of a work
		work_url = "https://archiveofourown.org/works/{}?view_full_work=true".format(work_id)

		try:
			response = requests.get(work_url)
			response.raise_for_status()
			return(response.text)
		except requests.exceptions.RequestException as e:
			raise SystemExit(e)

	#A factory method that uses the work id the fetch more information about the work
	@staticmethod
	def get_work_from_id(work_id):
		work_html = Work.get_work_html(work_id)
		soup = BeautifulSoup(work_html, "html.parser")
		
		main_html = soup.find(id="main")
		#Get the name of the work
		work_name_html = main_html.find(class_="title heading")
		work_name = work_name_html.get_text().strip()
		#Get the contents of each chapter
		chapters_html = main_html.find(id="chapters")
		chapters_divs = chapters_html.find_all(class_="userstuff")
		chapters_text = [chapter.get_text() for chapter in chapters_divs]
		
		#Create a work object from the work's info and return it
		return(Work(work_id, work_name, chapters_text))
	
#Test cases for Work class
class WorkTest(unittest.TestCase):
	#Tests if the work name is able to be fetched
	def test_work_name(self):
		manacled_work_id = 14454174
		work = Work.get_work_from_id(manacled_work_id)
		self.assertEqual(work.work_name, "Manacled")

	def test_work_count(self):
		manacled_work_id = 14454174
		work = Work.get_work_from_id(manacled_work_id)
		self.assertEqual(work.chapter_count, 143)
		print(work.chapter_count)

if __name__ == "__main__":
	unittest.main()
	#test_work_id = 14454174 #work id of "Manacled"
	#work = Work.get_work_from_id(test_work_id)
	#orkTest.