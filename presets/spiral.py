import colorsys
import random
import math

from lib.raw_preset import RawPreset
from lib.parameters import FloatParameter, HLSParameter
from lib.color_fade import ColorFade

class SpiralGradient(RawPreset):
    """Spiral gradient that responds to onsets"""
       
    _fader = None
    _fader_resolution = 256
    
    def setup(self):
        self.add_parameter(FloatParameter('speed', 0.3))
        self.add_parameter(FloatParameter('angle-hue-width', 2.0))
        self.add_parameter(FloatParameter('radius-hue-width', 1.5))        
        self.add_parameter(FloatParameter('wave-hue-width', 0.1))        
        self.add_parameter(FloatParameter('wave-hue-period', 0.1))        
        self.add_parameter(FloatParameter('wave-speed', 0.1))        
        self.add_parameter(FloatParameter('hue-step', 0.1))    
        self.add_parameter(HLSParameter('color-start', (0.0, 0.5, 1.0)))
        self.add_parameter(HLSParameter('color-end', (1.0, 0.5, 1.0)))
        self.hue_inner = random.random() + 100
        self.wave_offset = random.random()

        self.pixels = self.scene().get_all_pixels()
        cx, cy = self.scene().get_centroid()

        # Find radius to each pixel
        self.pixel_distances = {}
        self.pixel_angles = {}
        for pixel in self.pixels:
            x, y = self.scene().get_pixel_location(pixel)
            dx = x - cx
            dy = y - cy
            d = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
            self.pixel_distances[pixel] = d
            self.pixel_angles[pixel] = (math.pi + math.atan2(dy, dx)) / (2.0 * math.pi)

        # Normalize
        max_distance = max(self.pixel_distances.values())
        for pixel in self.pixels:
            self.pixel_distances[pixel] /= max_distance
            
        self.parameter_changed(None)

    def parameter_changed(self, parameter):
        fade_colors = [self.parameter('color-start').get(), self.parameter('color-end').get(), self.parameter('color-start').get()]
   
        self._fader = ColorFade(fade_colors, self._fader_resolution)
    
    def reset(self):
        pass

    def draw(self, dt):
        if self._mixer.is_onset():
            self.hue_inner = self.hue_inner + self.parameter('hue-step').get()

        start = self.hue_inner + (dt * self.parameter('speed').get())
        self.wave_offset = self.parameter('wave-speed').get() * dt

        for pixel in self.pixels:
            angle = math.fmod(1.0 + self.pixel_angles[pixel] + math.sin(self.wave_offset + self.pixel_distances[pixel] * 2 * math.pi * self.parameter('wave-hue-period').get()) * self.parameter('wave-hue-width').get(), 1.0)
            hue = start + (self.parameter('radius-hue-width').get() * self.pixel_distances[pixel]) + (angle * self.parameter('angle-hue-width').get())
            hue = math.fmod(math.floor(hue * self._fader_resolution) / self._fader_resolution, 1.0)
            self.setPixelHLS(pixel, self._fader.get_color(hue))