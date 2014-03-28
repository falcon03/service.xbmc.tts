# -*- coding: utf-8 -*-
import os, subprocess
from base import WavFileTTSBackendBase, WavPlayer,UnixExternalPlayerHandler

class Pico2WaveTTSBackend(WavFileTTSBackendBase):
	provider = 'pico2wave'
	displayName = 'pico2wave'
	
	extras = (('use_sox',False),)
	
	def __init__(self):
		preferred = None
		if self.userExtra('use_sox',False): preferred = 'sox'
		player = WavPlayer(UnixExternalPlayerHandler,preferred)
		WavFileTTSBackendBase.__init__(self,player)

		self.language = self.userVoice()
		self.setSpeed(self.userSpeed() * 0.01)
		
	def runCommand(self,text,outFile):
		args = ['pico2wave']
		if self.language: args.extend(['-l',self.language])
		args.extend(['-w', '{0}'.format(outFile), '{0}'.format(text)])
		subprocess.call(args)
		
	def voices(self):
		try:
			out = subprocess.check_output(['pico2wave','-l','NONE','-w','/dev/null','X'],stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError, e:
			out = e.output
		if not 'languages:' in out: return None
		
		return out.split('languages:',1)[-1].split('\n\n')[0].strip('\n').split('\n')

	def update(self,voice_name,speed):
		if voice_name: self.language = voice_name
		self.setSox()
		speed = speed or self.userSpeed()
		self.setSpeed(speed * 0.01)
		
	def setSox(self):
		preferred = None
		if self.userExtra('use_sox',False): preferred = 'sox'
		self.setPlayer(preferred)
		
	@staticmethod
	def available():
		try:
			subprocess.call(['pico2wave', '--help'], stdout=(open(os.path.devnull, 'w')), stderr=subprocess.STDOUT)
		except (OSError, IOError):
			return False
		return True