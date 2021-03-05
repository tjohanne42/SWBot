import pygame as pg
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
import random
import os

WHITE_TXT = (200, 200, 200)
WHITE_LINE = (179, 179, 179)
GREEN_LINE = (29, 185, 84)
# pixels near corner, 8 pixles on the total line
WHITE_LINE_BORDER1 = (161, 161, 161)
GREEN_LINE_BORDER1 = (33, 165, 80)
# for corner, 4 pixels on the total line
WHITE_LINE_BORDER2 = (103, 103, 103)
GREEN_LINE_BORDER2 = (41, 94, 60)

class MusicPlayer:
	"""docstring for MusicPlayer"""
	def __init__(self, x, y):
		pg.mixer.init(44100, -16, 2, 2048, allowedchanges=pg.AUDIO_ALLOW_ANY_CHANGE)
		width, height = 350, 100
		self.x, self.y = x, y
		self.music_player = pg.Surface((width, height))
		surface = pg.image.load("mpsrc/music_player.png")
		self.fonts = self.load_fonts("mpsrc/Inconsolata-Bold.ttf", 1, 30)
		self.music_player.blit(surface, (0, 0))
		self.volume = 0
		self.last_volume = self.volume
		self.play = True
		self.index = 0
		self.loop = False
		self.random = False
		self.hold = "noone"
		self.surface = {
						"previous" : pg.image.load("mpsrc/previous.png"),
						"previous_a" : pg.image.load("mpsrc/previous_a.png"),
						"next" : pg.image.load("mpsrc/next.png"),
						"next_a" : pg.image.load("mpsrc/next_a.png"),
						"play" : pg.image.load("mpsrc/play.png"),
						"play_a" : pg.image.load("mpsrc/play_a.png"),
						"pause" : pg.image.load("mpsrc/pause.png"),
						"pause_a" : pg.image.load("mpsrc/pause_a.png"),
						"volume_high" : pg.image.load("mpsrc/volume_high.png"),
						"volume_high_a" : pg.image.load("mpsrc/volume_high_a.png"),
						"volume_mid" : pg.image.load("mpsrc/volume_mid.png"),
						"volume_mid_a" : pg.image.load("mpsrc/volume_mid_a.png"),
						"volume_low" : pg.image.load("mpsrc/volume_low.png"),
						"volume_low_a" : pg.image.load("mpsrc/volume_low_a.png"),
						"volume_off" : pg.image.load("mpsrc/volume_off.png"),
						"volume_off_a" : pg.image.load("mpsrc/volume_off_a.png"),
						"point" : pg.image.load("mpsrc/point.png"),
						"point_a" : pg.image.load("mpsrc/point_a.png"),
						"loop" : pg.image.load("mpsrc/loop.png"),
						"loop_a" : pg.image.load("mpsrc/loop_a.png"),
						"loop_on" : pg.image.load("mpsrc/loop_on.png"),
						"loop_on_a" : pg.image.load("mpsrc/loop_on_a.png"),
						"random" : pg.image.load("mpsrc/random.png"),
						"random_a" : pg.image.load("mpsrc/random_a.png"),
						"random_on" : pg.image.load("mpsrc/random_on.png"),
						"random_on_a" : pg.image.load("mpsrc/random_on_a.png")
						}
		self.interactive_rect = {
								"previous" : pg.Rect(21, 35, 15, 16),
								"next" : pg.Rect(84, 35, 16, 16),
								"play" : pg.Rect(45, 28, 30, 30),
								"volume" : pg.Rect(110, 34, 22, 18),
								"trackline" : pg.Rect(10, 13, 299, 4),
								"volumeline" : pg.Rect(140, 41, 60, 4),
								"loop" : pg.Rect(286, 32, 22, 21),
								"random" : pg.Rect(320, 33, 30, 33)
								}
		self.load_musics()
		pg.mixer.music.set_volume(self.volume)
		self.music_load_and_play(self.index)

	def load_musics(self):
		self.tracklist = []
		listdir = os.listdir("music")
		i = 0
		while i < len(listdir):
			if listdir[i].find(".mp3") != -1:
				try:
					pg.mixer.music.load("music/" + listdir[i])
					song = MP3(f"music/{listdir[i]}")
					# self.tracklist[i][2] = NAME SURFACE
					# display x = 20 y = 62 width max = 279 height max = 38
					name = listdir[i].strip(".mp3")
					count = len(self.fonts) - 1
					while count >= 0:
						name_txt = self.fonts[count].render(name, True, WHITE_TXT)
						if name_txt.get_size()[0] <= 279 and name_txt.get_size()[1] <= 38:
							break
						count -= 1
					self.tracklist.append(["music/" + listdir[i], song.info.length, name_txt, song.info.sample_rate])
					print("mp3", name, song.info.bitrate, song.info.sample_rate)
				except:
					print(f"Couldn't load 'music/{listdir[i]}'")
			elif listdir[i].find(".ogg") != -1:
				try:
					pg.mixer.music.load("music/" + listdir[i])
					song = OggVorbis(f"music/{listdir[i]}")
					# self.tracklist[i][2] = NAME SURFACE
					# display x = 20 y = 62 width max = 279 height max = 38
					name = listdir[i].strip(".ogg")
					count = len(self.fonts) - 1
					while count >= 0:
						name_txt = self.fonts[count].render(name, True, WHITE_TXT)
						if name_txt.get_size()[0] <= 279 and name_txt.get_size()[1] <= 38:
							break
						count -= 1
					self.tracklist.append(["music/" + listdir[i], song.info.length, name_txt, song.info.sample_rate])
					print("ogg", name, song.info.bitrate, song.info.sample_rate)
				except:
					print(f"Couldn't load 'music/{listdir[i]}'")
			i += 1

	def load_fonts(self, path, minsize, maxsize):
		fonts = []
		i = minsize
		while i < maxsize:
			fonts.append(pg.font.Font(path, i))
			i += 1
		return fonts

	def music_load_and_play(self, index):
		if pg.mixer.get_init()[0] != self.tracklist[index][3]:
			pg.mixer.init(frequency=self.tracklist[index][3])
		pg.mixer.music.load(self.tracklist[index][0])
		pg.mixer.music.play()
		self.start = pg.time.get_ticks()
		if not self.play:
			self.start = 0
			pg.mixer.music.pause()

	def music_if_ended_play_next(self):
		if not pg.mixer.music.get_busy():
			if not self.loop:
				self.music_increase_index()
			self.music_load_and_play(self.index)

	def music_increase_index(self):
		if self.index == len(self.tracklist) - 1:
			self.index = 0
		else:
			self.index += 1

	def music_decrease_index(self):
		if self.index == 0:
			self.index = len(self.tracklist) - 1
		else:
			self.index -= 1

	def music_get_pos(self):
		if len(self.tracklist) < 1:
			return 0
		elif self.play:
			return pg.time.get_ticks() - self.start
		else:
			return self.start

	def music_pause_play(self):
		if self.play:
			pg.mixer.music.pause()
			self.start = pg.time.get_ticks() - self.start
			self.play = False
		else:
			pg.mixer.music.unpause()
			self.start = pg.time.get_ticks() - self.start
			self.play = True

	def music_rewind(self):
		pg.mixer.music.rewind()
		if self.play:
			self.start = pg.time.get_ticks()
		else:
			self.start = 0

	def music_set_pos(self, timer, rel=True):
		if not rel:
			pg.mixer.music.rewind()
			pg.mixer.music.set_pos(timer / 1000)
			self.start = timer
			return
		pos = self.music_get_pos()
		if pos + timer >= self.tracklist[self.index][1] * 1000:
			if self.play:
				self.start = pg.time.get_ticks() - (self.tracklist[self.index][1] - 0.4) * 1000
			else:
				self.start = (self.tracklist[self.index][1] - 0.4) * 1000
			pg.mixer.music.rewind()
			pg.mixer.music.set_pos(self.tracklist[self.index][1] - 0.4)
		elif pos + timer <= 0:
			self.music_rewind()
		else:
			pg.mixer.music.rewind()
			pg.mixer.music.set_pos((pos + timer) / 1000)
			self.start -= timer
			if not self.play:
				self.start = pos + timer

	def music_set_volume(self, value, rel=True):
		if rel:
			if self.volume + value >= 1:
				self.volume = 1
			elif self.volume + value <= 0.01:
				self.volume = 0
			else:
				self.volume += value
		else:
			self.volume = value
		pg.mixer.music.set_volume(self.volume)

	def music_random_on(self):
		self.random = True
		if len(self.tracklist) - 1 < 3:
			return
		self.tracklist_random = []
		for i in self.tracklist:
			tmp = []
			for x in i:
				tmp.append(x)
			self.tracklist_random.append(tmp)
		i, size = 0, len(self.tracklist_random) - 1
		while i < size:
			rand = i
			while rand == i or rand == self.index:
				rand = random.randint(0, size)
			if i == self.index:
				rand = 0
			tmp = []
			for x in self.tracklist[i]:
				tmp.append(x)
			self.tracklist[i] = []
			for x in self.tracklist[rand]:
				self.tracklist[i].append(x)
			self.tracklist[rand] = []
			for x in tmp:
				self.tracklist[rand].append(x)
			i += 1
		self.index = 0
		print("self.index", self.index)
		print("old tracklist")
		for i in self.tracklist_random:
			print(i[0])
		print("new tracklist")
		for i in self.tracklist:
			print(i[0])

	def music_random_off(self):
		self.random = False
		if len(self.tracklist) - 1 < 3:
			return
		i = 0
		while self.tracklist[self.index][0] != self.tracklist_random[i][0]:
			i += 1
		self.index = i
		self.tracklist = []
		for i in self.tracklist_random:
			tmp = []
			for x in i:
				tmp.append(x)
			self.tracklist.append(tmp)

	def pos_in_interactive(self, name, mx, my, addwidth=0, addheight=0):
		if pg.Rect(self.interactive_rect[name].x + self.x - addwidth / 2, self.interactive_rect[name].y + self.y - addheight / 2,
			self.interactive_rect[name].width + addwidth, self.interactive_rect[name].height + addheight).collidepoint((mx, my)):
			return True
		return False


	def display(self, surface, x, y):
		self.music_if_ended_play_next()
		music_pos = self.music_get_pos()
		self.x, self.y = x, y
		mx, my = pg.mouse.get_pos()
		surface.blit(self.music_player, (x, y))

		# VOLUME
		if self.volume > 2 / 3:
			name = "volume_high"
		elif self.volume > 1 / 3:
			name = "volume_mid"
		elif self.volume > 0:
			name = "volume_low"
		else:
			name = "volume_off"
		if self.hold != "volume" and self.pos_in_interactive("volume", mx, my):
			name += "_a"
		surface.blit(self.surface[name], (x + self.interactive_rect["volume"].x, y + self.interactive_rect["volume"].y))

		# PLAY
		if self.play:
			name = "pause"
		else:
			name = "play"
		if self.hold != "play" and self.pos_in_interactive("play", mx, my):
			name += "_a"
		surface.blit(self.surface[name], (x + self.interactive_rect["play"].x, y + self.interactive_rect["play"].y))

		# PREVIOUS
		if self.hold != "previous" and self.pos_in_interactive("previous", mx, my):
			surface.blit(self.surface["previous_a"], (x + self.interactive_rect["previous"].x, y + self.interactive_rect["previous"].y))
		else:
			surface.blit(self.surface["previous"], (x + self.interactive_rect["previous"].x, y + self.interactive_rect["previous"].y))

		# NEXT
		if self.hold != "next" and self.pos_in_interactive("next", mx, my):
			surface.blit(self.surface["next_a"], (x + self.interactive_rect["next"].x, y + self.interactive_rect["next"].y))
		else:
			surface.blit(self.surface["next"], (x + self.interactive_rect["next"].x, y + self.interactive_rect["next"].y))

		# LOOP
		name = "loop"
		if self.loop:
			name += "_on"
		if self.hold != "loop" and self.pos_in_interactive("loop", mx, my):
			name += "_a"
		surface.blit(self.surface[name], (x + self.interactive_rect["loop"].x, y + self.interactive_rect["loop"].y))

		# RANDOM
		name = "random"
		if self.random:
			name += "_on"
		if self.hold != "random" and self.pos_in_interactive("random", mx, my):
			name += "_a"
		surface.blit(self.surface[name], (x + self.interactive_rect["random"].x, y + self.interactive_rect["random"].y))

		# TIMER
		# display y = 28 x = 206
		# height max = 29 widht max = 74
		i = 18
		amin, asec = int(music_pos / 1000 / 60), int(music_pos / 1000 % 60)
		mmin, msec = int(self.tracklist[self.index][1] / 60), int(self.tracklist[self.index][1] % 60)
		timer_str = f"{' ' if amin < 10 else ''}{amin}:{'0' if asec < 10 else ''}{asec}/{mmin}:{'0' if msec < 10 else ''}{msec}"
		while i >= 0:
			timer_txt = self.fonts[i].render(timer_str, True, WHITE_TXT)
			if timer_txt.get_size()[0] <= 74 and timer_txt.get_size()[1] <= 29:
				break
			i -= 1
		surface.blit(timer_txt, (x + 206 + 74 / 2 - timer_txt.get_size()[0] / 2, y + 28 + 29 / 2 - timer_txt.get_size()[1] / 2))

		# NAME
		# display x = 20 y = 62
		# width max = 279 height max = 38
		name_surface = self.tracklist[self.index][2]
		surface.blit(name_surface, (x + 20 + 279 / 2 - name_surface.get_size()[0] / 2, y + 60 + 38 / 2 - name_surface.get_size()[1] / 2))



		# VOLUMELINE
		tmp_x, tmp_y = x + self.interactive_rect["volumeline"].x, y + self.interactive_rect["volumeline"].y
		tmp_len_line = int(60 * self.volume)
		if self.hold == "volumeline" or self.pos_in_interactive("volumeline", mx, my, addwidth=8, addheight=8):
			color1, color2, color3 = GREEN_LINE, GREEN_LINE_BORDER1, GREEN_LINE_BORDER2
		else:
			color1, color2, color3 = WHITE_LINE, WHITE_LINE_BORDER1, WHITE_LINE_BORDER2
		pg.draw.rect(surface, color1, pg.Rect(tmp_x, tmp_y, tmp_len_line, 4))
		# making the line beautifull
		if tmp_len_line >= 1:
			pg.draw.line(surface, color3, (tmp_x, tmp_y), (tmp_x, tmp_y + 3))
			if tmp_len_line >= 2:
				pg.draw.line(surface, color3, (tmp_x + tmp_len_line - 1, tmp_y), (tmp_x + tmp_len_line - 1, tmp_y + 3))
				if tmp_len_line >= 4:
					pg.draw.line(surface, color2, (tmp_x, tmp_y + 1), (tmp_x, tmp_y + 2))
					pg.draw.line(surface, color2, (tmp_x + 1, tmp_y), (tmp_x + 1, tmp_y))
					pg.draw.line(surface, color2, (tmp_x + 1, tmp_y + 3), (tmp_x + 1, tmp_y + 3))
					pg.draw.line(surface, color2, (tmp_x + tmp_len_line - 1, tmp_y + 1), (tmp_x + tmp_len_line - 1, tmp_y + 2))
					pg.draw.line(surface, color2, (tmp_x + tmp_len_line - 2, tmp_y), (tmp_x + tmp_len_line - 2, tmp_y))
					pg.draw.line(surface, color2, (tmp_x + tmp_len_line - 2, tmp_y + 3), (tmp_x + tmp_len_line - 2, tmp_y + 3))
		name = "point"
		if self.hold == "volumeline":
			name += "_a"
		if color1 == GREEN_LINE:
			surface.blit(self.surface[name], (tmp_x + 50 * self.volume, tmp_y - 4))

		# TRACKLINE
		tmp_x, tmp_y = x + self.interactive_rect["trackline"].x, y + self.interactive_rect["trackline"].y
		tmp_len_line = music_pos / (self.tracklist[self.index][1] * 1000) * 300
		if self.hold == "trackline" or self.pos_in_interactive("trackline", mx, my, addwidth=8, addheight=8):
			color1, color2, color3 = GREEN_LINE, GREEN_LINE_BORDER1, GREEN_LINE_BORDER2
		else:
			color1, color2, color3 = WHITE_LINE, WHITE_LINE_BORDER1, WHITE_LINE_BORDER2
		pg.draw.rect(surface, color1, pg.Rect(tmp_x, tmp_y, tmp_len_line, 4))
		# making the line beautifull
		if tmp_len_line >= 1:
			pg.draw.line(surface, color3, (tmp_x, tmp_y), (tmp_x, tmp_y + 3))
			if tmp_len_line >= 2:
				pg.draw.line(surface, color3, (tmp_x + tmp_len_line - 1, tmp_y), (tmp_x + tmp_len_line - 1, tmp_y + 3))
				if tmp_len_line >= 4:
					pg.draw.line(surface, color2, (tmp_x, tmp_y + 1), (tmp_x, tmp_y + 2))
					pg.draw.line(surface, color2, (tmp_x + 1, tmp_y), (tmp_x + 1, tmp_y))
					pg.draw.line(surface, color2, (tmp_x + 1, tmp_y + 3), (tmp_x + 1, tmp_y + 3))
					pg.draw.line(surface, color2, (tmp_x + tmp_len_line - 1, tmp_y + 1), (tmp_x + tmp_len_line - 1, tmp_y + 2))
					pg.draw.line(surface, color2, (tmp_x + tmp_len_line - 2, tmp_y), (tmp_x + tmp_len_line - 2, tmp_y))
					pg.draw.line(surface, color2, (tmp_x + tmp_len_line - 2, tmp_y + 3), (tmp_x + tmp_len_line - 2, tmp_y + 3))
		name = "point"
		if self.hold == "trackline":
			name += "_a"
		if color1 == GREEN_LINE:
			surface.blit(self.surface[name], (tmp_x + music_pos / (self.tracklist[self.index][1] * 1000) * 290, tmp_y - 4))

	def music_event_volumeline(self, mx, my):
		if mx - self.x < self.interactive_rect["volumeline"].x:
			self.music_set_volume(0, rel=False)
		elif mx - self.x > self.interactive_rect["volumeline"].x + self.interactive_rect["volumeline"].w:
			self.music_set_volume(1, rel=False)
		else:
			self.music_set_volume((mx - self.x - self.interactive_rect["volumeline"].x) * 100 / self.interactive_rect["volumeline"].w / 100, rel=False)

	def music_event_trackline(self, mx, my):
		if mx - self.x < self.interactive_rect["trackline"].x:
			self.music_set_pos(0, rel=False)
		elif mx - self.x > self.interactive_rect["trackline"].x + self.interactive_rect["trackline"].w:
			self.music_set_pos(self.tracklist[self.index][1] * 1000, rel=False)
		else:
			self.music_set_pos((mx - self.x - self.interactive_rect["trackline"].x) * 100 / self.interactive_rect["trackline"].w * self.tracklist[self.index][1] * 10, rel=False)
	
	def event(self, event):
		self.music_if_ended_play_next()
		if event.type == pg.MOUSEMOTION:
			mx, my = pg.mouse.get_pos()
			if self.hold == "volumeline":
				self.music_event_volumeline(mx, my)
			elif self.hold == "trackline":
				self.music_event_trackline(mx, my)
			elif self.hold != "noone" and self.pos_in_interactive(self.hold, mx, my):
				self.hold = "noone"

		elif event.type == pg.MOUSEBUTTONDOWN:
			mx, my = pg.mouse.get_pos()
			if event.button == 1:
				if self.pos_in_interactive("previous", mx, my):
					self.hold = "previous"
				elif self.pos_in_interactive("next", mx, my):
					self.hold = "next"
				elif self.pos_in_interactive("play", mx, my):
					self.hold = "play"
				elif self.pos_in_interactive("loop", mx, my):
					self.hold = "loop"
				elif self.pos_in_interactive("volume", mx, my):
					self.hold = "volume"
				elif self.pos_in_interactive("random", mx, my):
					self.hold = "random"
				elif self.pos_in_interactive("volumeline", mx, my, addwidth=8, addheight=8):
					self.last_volume = self.volume
					self.hold = "volumeline"
					self.music_event_volumeline(mx, my)
				elif self.pos_in_interactive("trackline", mx, my, addwidth=8, addheight=8):
					self.was_playing = False
					if self.play:
						self.was_playing = True
						self.music_pause_play()
					self.hold = "trackline"
					self.music_event_trackline(mx, my)
			if event.button == 4:
				if self.pos_in_interactive("trackline", mx, my, addwidth=8, addheight=8):
					self.music_set_pos(5000)
				else:
					self.music_set_volume(0.05)
			elif event.button == 5:
				if self.pos_in_interactive("trackline", mx, my, addwidth=8, addheight=8):
					self.music_set_pos(-5000)
				else:
					self.music_set_volume(-0.05)

		elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
			if self.hold == "previous":
				if self.music_get_pos() > 5000:
					self.music_rewind()
				else:
					tmp = self.index
					self.music_decrease_index()
					if tmp != self.index:
						self.loop = False
					self.music_load_and_play(self.index)
			elif self.hold == "next":
				tmp = self.index
				self.music_increase_index()
				if tmp != self.index:
					self.loop = False
				self.music_load_and_play(self.index)
			elif self.hold == "play":
				self.music_pause_play()
			elif self.hold == "loop":
				if not self.loop:
					self.loop = True
				else:
					self.loop = False
			elif self.hold == "random":
				if not self.random:
					self.music_random_on()
				else:
					self.music_random_off()
					self.random = False

			elif self.hold == "volume":
				if self.volume > 0:
					self.last_volume = self.volume
					self.music_set_volume(0, rel=False)
				else:
					self.music_set_volume(self.last_volume, rel=False)
			elif self.hold == "trackline":
				if self.was_playing:
					self.music_pause_play()
			if self.hold != "noone":
				self.hold = "noone"

		elif event.type == pg.KEYDOWN:
			if event.key == pg.K_SPACE:
				self.music_pause_play()
