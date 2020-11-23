from .util import *
from scipy import ndimage, misc
from .wordcloud import WordCloud
from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont
import textwrap

class NresWordle:
    def __init__(self, data, spec={}, width=1960, height=1080, font_path='data/msyh.ttf',
                 inner_font_path='data/msyh.ttf',
                 scale=1, outer_max_words=30, outer_max_font_size=300,
                 outer_min_font_size=150, inner_max_font_size=30,
                 inner_min_font_size=8, ppi=200, background_color="white", blend_alpha=0.3, radius=20,
                 en=False, dilate_size = 10, erode_size=10, inner_repeat=False):
        self.width = width
        self.height = height
        self.outer_data = data['keyword_list']
        self.inner_data = data['context_list']
        self.lookup = wordToid(self.outer_data)
        self.dilate_size = outer_max_font_size / 30 if dilate_size == 10 else dilate_size
        self.erode_size = 15 if erode_size==10 else erode_size
        self.inner_max_font_size = inner_max_font_size
        self.inner_min_font_size = inner_min_font_size
        self.outer_max_font_size = outer_max_font_size
        self.outer_min_font_size = outer_min_font_size
        self.background_color = background_color
        self.font_path = font_path
        self.inner_font_path = inner_font_path
        self.blend_alpha = blend_alpha
        self.inner_repeat = inner_repeat
        self.scale = 1
        self.en = en
        self.radius = radius
        self.wordcloud = WordCloud(width=width,
                                   height=height,
                                   max_font_size=outer_max_font_size,
                                   min_font_size=outer_min_font_size,
                                   max_words=outer_max_words,
                                   background_color=background_color,
                                   font_path=font_path,
                                   prefer_horizontal=1,
                                   scale=1,
                                   colormap='winter',
                                   en=self.en)
        self.tinywordledict = {}
        self.canvas = Image.new('RGB', (width, height), background_color)
        self.outer_canvas=Image.new('RGB', (width, height), background_color)
        return


    def generate(self):
        self.generateLargeWordle()
        self.generateTinyWordle()
        final = self.blendWordle()
        return final

    def generateTinyWordle(self):
        outer_image = self.outer_img.convert('L')
        smallcanvas = Image.new('RGB', (self.width, self.height), self.background_color)
        draw = ImageDraw.Draw(smallcanvas)
        inner = self.inner_data
        outer = self.outer_data
        lookup = self.lookup
        for (word, count), font_size, (y,x), (w,h), orientation, color in self.wordle:
            xx, yy, ww, hh = orientation
            datalist = dict([(inner[idx]['context'], inner[idx]['weight']) for idx in outer[lookup[word]]['ref']])
            region = outer_image.crop((xx, yy, ww+xx, hh+yy))
            background = getBackground(region, self.dilate_size)
            foreground = getForeGround(region, self.erode_size) if not self.en else np.array(region)
            tinylayout = self.parallelTinyWordle(foreground, background, datalist, xx, yy, ww, hh, color)
            self.tinywordledict[word] = tinylayout
            self.plotSonLayout(smallcanvas, tinylayout, xx, yy, False)
        self.inner_img=smallcanvas
        return

    def generateLargeWordle(self):
        data_dict = dict([(w['word'], w['weight']) for w in self.outer_data])
        self.wordcloud.generate_from_frequencies_small(
            data_dict,
            max_font_size=self.outer_max_font_size,
            min_font_size=self.outer_min_font_size)
        colorCorrect = colorAdjust(self.wordcloud.layout_)
        self.wordle = constructBox(colorCorrect, self.width, self.height)
        self.outer_img =  self.plotLayoutToCanvas(self.wordle, self.outer_canvas, plotBox=False)
        return self.wordle

    def parallelTinyWordle(self, mask, background, datalist, x, y, w, h, color):
        if not self.en:
            tinywordle = WordCloud(width=w,
                                        height=h,
                                        max_font_size=self.inner_max_font_size,
                                        min_font_size=self.inner_min_font_size,
                                        max_words=1000,
                                        background_color=self.background_color,
                                        font_path=self.inner_font_path,
                                        prefer_horizontal=1,
                                        mask = mask,
                                        scale=1,
                                        repeat=self.inner_repeat,
                                        en=self.en)
            tinywordle.generate_from_frequencies_small(datalist, max_font_size=self.inner_max_font_size,
                    min_font_size=self.inner_min_font_size)
            if not self.inner_repeat and not len(tinywordle.layout_)==len(datalist):
                for item in tinywordle.layout_:
                    key = item[0][0]
                    try:
                        del datalist[key]
                    except KeyError:
                        pass
        if self.en:
            background
        bgwordle = WordCloud(width=w,
                                height=h,
                                max_font_size=self.inner_max_font_size,
                                min_font_size=self.inner_min_font_size,
                                max_words=1000,
                                background_color=self.background_color,
                                font_path=self.inner_font_path,
                                prefer_horizontal=1,
                                mask = background,
                                scale=1,
                                repeat=self.inner_repeat,
                                en=self.en)
        if not len(datalist)==0:
            bgwordle.generate_from_frequencies_small(datalist, max_font_size=self.inner_max_font_size,
                min_font_size=self.inner_min_font_size)
        tinyl = colorAdjust(tinywordle.layout_, 1, color) if not self.en else []
        bgl = colorAdjust(bgwordle.layout_, 2, color) if not len(datalist)==0 else []
        alltiny = tinyl+bgl
        return alltiny

    def plotLayoutToCanvas(self, layout, canvas, plotBox=False):
        draw = ImageDraw.Draw(canvas)
        for (word, count), font_size, position, box, orientation, color in layout:
            font = ImageFont.truetype(self.font_path,
                                      int(font_size * self.scale))
            y, x = position
            yy = y - font_size*0.2
            w, h = box
            h = (1+word.count('\n')) * font_size
            if self.en:
                draw.multiline_text((x*self.scale, yy*self.scale), word, fill=color, font=font)
            else:
                draw.multiline_text((x*self.scale, y*self.scale), word, fill=color, font=font)
            if plotBox:
                draw.rectangle(xy=[x,y,x+w*self.scale,y+h*self.scale], outline=color, width=1)
        return canvas

    def plotSonLayout(self, canvas, layout, xx, yy, drawBox=False):
        draw = ImageDraw.Draw(canvas)
        for (word, count), font_size, (y,x), (w,h), orientation, color in layout:
            font = ImageFont.truetype(self.inner_font_path, int(font_size))
            if not self.en:
                draw.multiline_text((xx+x, yy+y-font_size*0.2), word, fill=color, font=font)
            else:
                draw.multiline_text((xx+x, yy+y), word, fill=color, font=font)
            if drawBox:
                draw.rectangle(xy=[xx+x,yy+y,xx+x+w,yy+y+h], outline=color, width=1)
        return canvas

    def blendWordle(self, blend_alpha=None):
        if blend_alpha== None:
            blend_alpha = self.blend_alpha
        filtered_image = self.outer_img.filter(ImageFilter.GaussianBlur(radius=self.radius))
        overview = filtered_image.convert("RGBA")
        detail = self.inner_img.convert("RGBA")
        result = Image.blend(overview, detail, alpha=blend_alpha)
        return result
