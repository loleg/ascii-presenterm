#!/usr/bin/python

import os
import curses


class PresenTerm:

	def __init__(self, screen):
		self.screen = screen
		self.height, self.width = screen.getmaxyx()
		self.offsety, self.offsetx = -self.height / 2, -self.width / 2
		self.cur = 0
		self.slides = []
		self.dirname = '.'  # TODO: from arg

	def readSlides(self):
		for dirname, dirnames, filenames in os.walk(self.dirname):
			for filename in filenames:
				if filename.count('.slide'):
					with open(filename) as f:
						self.slides.append(f.read())
					f.close()

	def showCounter(self):
		if self.cur < 1:
			self.cur = 1
		if self.cur > len(self.slides):
			self.cur = len(self.slides)
		self.screen.addstr(0, 0, 'presenterm: %(dir)s: %(cur)s of %(count)s' %
			{ 'dir': self.dirname, 'cur': self.cur, 'count': len(self.slides) },
			curses.A_REVERSE)

	def showSlide(self):
		self.screen.addstr(3, 0,
			'%(slide)s' % { 'slide': self.slides[self.cur - 1] },
			curses.A_NORMAL)

	def moveSlide(self, moveTo):
		self.cur = self.cur + moveTo
		self.refresh()

	def refresh(self):
		self.screen.clear()
		self.showCounter()
		self.showSlide()

	def main(self):
		self.readSlides()
		self.refresh()
		while 1:
			key = self.screen.getch()
			if key == ord('q'):
				break
			elif key == curses.KEY_LEFT or key == ord('a'):
				self.moveSlide(-1)
			elif key == curses.KEY_RIGHT or key == ord('d'):
				self.moveSlide(1)


def main(stdscr):
	screen = PresenTerm(stdscr)
	screen.main()

curses.wrapper(main)
