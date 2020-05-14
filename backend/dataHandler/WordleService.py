class NresWordle:
    def __init__(self, outer_data, inner_data, spec, width=1960, height=1080, font_path='data/msyh.ttf',
                 scale=1, outer_max_words=30, outer_max_font_size=512,
                 outer_min_font_size=150, inner_max_font_size=30,
                 inner_min_font_size=8, ppi=200, background_color="white"):
        self.width = width
        self.height = height
        self.outer_data = outer_data
        self.inner_data = inner_data
        self.dilate_size = outer_max_font_size / 30
        self.erode_size = 10
        self.inner_max_font_size = inner_max_font_size
        self.inner_min_font_size = inner_min_font_size
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
                                   blend_alpha=0.3)
        self.wordcloud.generate_from_frequencies(outer_data, max_font_size=outer_max_font_size,
                                                 min_font_size=outer_min_font_size)
        self.outer_img = self.wordcloud.to_image()
        self.wordle = self.wordcloud.layout_
        self.inner_img = self.tmpTiny()
        self.blendWordle()
        return self


def tmpTiny(self):
    img_arr = np.array(self.outer_image.convert('L'))
    dilate_image_arr = ndimage.minimum_filter(img_arr, size=self.dilate_size)
    erode_image_arr = ndimage.maximum_filter(img_arr, size=self.erode_size)
    self.context_wordcloud = WordCloud(
        width=self.width,
        height=self.height,
        max_font_size=self.inner_max_font_size,
        min_font_size=self.inner_min_font_size,
        max_words=800,
        background_color=self.background_color,
        font_path=self.font_path,
        prefer_horizontal=1,
        repeat=True,
        mask=np.uint8(dilate_image_arr),
        scale=1)
    self.context_wordcloud.generate_from_frequencies(data, max_font_size=30, min_font_size=4)
    return self.context_wordcloud.to_image()


def generateTinyWordle(self):
    return


def tinyWordle(self, rpos, box, corpus, basicColor, word, patch):
    width, height = box
    rx, ry = rpos
    canvas = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(canvas)

    return canvas


def blendWordle(self):
    overview = self.outer_img.convert("RGBA")
    detail = self.inner_img.convert("RGBA")
    result = Image.blend(overview, detail, alpha=self.blend_alpha)
    return result