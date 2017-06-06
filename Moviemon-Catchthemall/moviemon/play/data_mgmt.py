from django.conf import settings
from moviemon.settings import MAP, SESSION, SAVE_DIR
from os import listdir, remove
from os.path import isfile, join

import requests
import json
import pickle
import random

class Data_mgmt:

	def get_strength(self):
		return self.strength

	Status = 0

	def load_default_settings(self):
		self.Status = 0
		self.strength = 0
		self.Boli = False
		self.moviedex = []
		self.movielist = []
		self.index = 1
		self.movie_index = -1
		self.position = settings.PLAYER_START
		self.nbr_balls = 0
		for name in settings.MOVIES:
			response = requests.get("http://www.omdbapi.com/?t=" + name + "&plot=short&r=json")
			self.movielist.append(json.loads(response.text))
		self.dic = {"position": self.position, "nbr_balls": self.nbr_balls, "Moviedex": self.moviedex, "Movies": self.movielist, "movie_index": self.movie_index}
		self.picklize()

	def load(self, f):
		try:
			game = pickle.load(open(f, 'rb'))
			return game
		except Exception as e:
			return self.load_default_settings()

	def load_save(self, f):
		return self.load(SAVE_DIR + f)

	def dump_session(self):
		self.dump_to_file(SESSION)

	def dump_to_file(self, path):
		pickle.dump(self, open(path, 'wb'))

	def dump(self):
		obj = self.unpicklize()
		return (obj)

	def get_random_movie(self):
		obj = self.dump()
		mv = obj['Movies']
		dex = obj['Moviedex']
		while len(dex) < len(mv):
			var = random.choice(mv)
			# start methode sale
			count = 0
			for i in dex:
				if dex[i]['Title'] == var['Title']:
					count += 1
			if count == 0:
				return var
			# end methode sale

	def get_Status(self):
		return self.Status

	def set_Status(self, v):
		self.Status = v

	def get_movie(self, name):
		obj = self.dump()['Movies']
		for item in obj:
			if item['Title'] == name:
				return item

	def picklize(self):
		f = open("data_pickled", "wb")
		pickle.dump(self.dic, f)
		f.close()

	def unpicklize(self):
		f = open("data_pickled", "rb")
		obj = pickle.load(f)
		f.close()
		return obj

	def save_game(self, title, old=None):
		if old:
			remove(SAVE_DIR + old)
		movielist = len(self.movielist)
		file_name = SAVE_DIR + "slot" + title + "_" + str(len(self.moviedex))
		file_name +=  "_" + str(len(self.movielist)) + ".mmg"
		self.dump_to_file(file_name)

	def get_all_save(self):
		f = onlyfiles = [f for f in listdir(SAVE_DIR) if isfile(join(SAVE_DIR, f))]
		l_save = {'a': [], 'b': [], 'c': []}
		for save in f:
			if len(save) < 14 and save[-4:] != ".mmg":
				continue
			elif save[:4] != 'slot':
				continue
			elif save[4] in ['a', 'b', 'c']:
				if l_save[save[4]]:
					continue
				else:
					name = "Slot %s : %s" % (save[4].upper(),
											 save[5:].replace('_', ' ')[:-4])
					l_save[save[4]] = [name ,save]
		l_save = [l_save['a'], l_save['b'], l_save['c']]
		return l_save
