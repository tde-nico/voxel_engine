from settings import *
import moderngl as mgl
import pygame as pg
import sys
from shader_program import ShaderProgram
from scene import Scene
from player import Player
from textures import Textures

def fullscreen():
	global FULLSCREEN
	FULLSCREEN = not FULLSCREEN
	if FULLSCREEN:
		pg.display.set_mode(MONITOR_SIZE, pg.FULLSCREEN | pg.OPENGL | pg.DOUBLEBUF)
	else:
		pg.display.toggle_fullscreen()
		pg.display.set_mode(WIN_RES, pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)


class VoxelEngine:
	def __init__(self):
		pg.init()
		pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, MAJOR_VER)
		pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, MINOR_VER)
		pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
		pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, DEPTH_SIZE)
		pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, NUM_SAMPLES)

		pg.display.set_mode(WIN_RES, flags=pg.OPENGL | pg.DOUBLEBUF)
		self.ctx = mgl.create_context()

		self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
		self.ctx.gc_mode = 'auto'

		MONITOR_SIZE = (pg.display.Info().current_w, pg.display.Info().current_h)

		self.clock = pg.time.Clock()
		self.delta_time = 0
		self.time = 0

		pg.event.set_grab(True)
		pg.mouse.set_visible(False)

		self.is_running = True
		self.on_init()

	def on_init(self):
		self.textures = Textures(self)
		self.player = Player(self)
		self.shader_program = ShaderProgram(self)
		self.scene = Scene(self)

	def update(self):
		self.player.update()
		self.shader_program.update()
		self.scene.update()

		self.delta_time = self.clock.tick(60)
		self.time = pg.time.get_ticks() * 0.001
		pg.display.set_caption(f'{self.clock.get_fps() :.0f}')

	def render(self):
		self.ctx.clear(color=BG_COLOR)
		self.scene.render()
		pg.display.flip()

	def handle_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.is_running = False
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.is_running = False
				if event.key == pg.K_F11:
					fullscreen()
			self.player.handle_event(event=event)

	def run(self):
		while self.is_running:
			self.handle_events()
			self.update()
			self.render()
		pg.quit()
		sys.exit()


if __name__ == '__main__':
	app = VoxelEngine()
	app.run()
