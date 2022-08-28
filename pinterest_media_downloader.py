"""
* ⚠️ Unfinished (only shows URLs, the download functionality is not added yet)
* ⚠️ It relies on Pinterest API V3 public endpoint which may get inactive any time.
"""

import requests

class PinterestMediaDownloader:
	info_url = "https://api.pinterest.com/v3/pidgets/pins/info/?pin_ids={}"
	
	def __init__(self, pin_url):
		self.session = requests.Session()
		self.pin_url = pin_url
		# values to get
		self.pin_id = None
		self.media = []
		self.data = None
		self.best_sizes = []

	def get_pin_id(self):
		# get pin id
		history = self.session.get(self.pin_url).history
		self.pin_id = history[-1].headers["location"].split("/")[4] if history else self.pin_url.split("/")[4]

	def get_pin_data(self):
		# fetch pin info
		self.data = self.session.get(self.__class__.info_url.format(self.pin_id)).json()["data"][0]
	  
	def get_pin_media(self): 
		# if the post is a story
		if spd := self.data.get("story_pin_data"):
			for page in spd["pages"]:
				# if the story page is a video
				if v := page["blocks"][0].get("video"):
					self.media.append(v.get("video_list")) 
				# if the story page is an image
				elif i := page["blocks"][0].get("image"):
					self.media.append(i.get("images"))
				else:
					pass
		# if the post is a single video
		elif v := self.data.get("videos"):
			self.media.append(v.get("video_list"))
		# if the post is a single image
		elif i := self.data.get("images"):
			self.media.append(i)
		else:
			pass
		
	def get_best_sizes(self):
		for i, m in enumerate(self.media):
			# remove .m3u8 urls
			for s in list(m):
				if m[s]["url"].strip().endswith(".m3u8"):
					m.pop(s)
			# sort urls by size
			new_m = sorted(m.values(), key=lambda s: s["width"]*s["height"], reverse=True)
			
			# best size for a particular image/video
			self.best_sizes.append(new_m[0])

	def run(self):
		self.get_pin_id()
		self.get_pin_data()
		self.get_pin_media()
		self.get_best_sizes()

"""
# ____ test ____ 
d = PinterestMediaDownloader("https://pin.it/4GikuR8")
d.run()
print(d.best_sizes)
"""
