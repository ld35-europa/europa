#!/usr/bin/env python2

import pygame

_cache = dict()

def load_cached_asset(fn):
	surface = None

	try:
		surface = _cache[fn]
	except KeyError as e:
		print "loading", fn
		_cache[fn] = surface = pygame.image.load(fn)

	return surface
