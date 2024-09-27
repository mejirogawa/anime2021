!pip install apng
import os, IPython
from PIL import Image, ImageDraw, ImageFont
from apng import APNG

class AStudio(object):
    bodies: list
    frame: int

    def __init__(self, width=400, height=300, background='gray'):
        self.width = width
        self.height = height
        self.background = background
        self.bodies = []
        self.files = []
        self.frame = 0
    
    def append(self, shape):
        self.bodies.append(shape) # 被写体を追加する
        return shape

    def render(self, caption=''):
        # 新しいキャンバスを作る
        canvas = ACanvas(self.width, self.height, self.background)
        # リスト上の形状を順番に描画する
        for body in self.bodies:
            body.render(canvas, self.frame)
        # PNG画像に保存する
        filename = f'frame{self.frame}.png'
        canvas.image.save(filename)
        self.files.append(filename)
        self.frame += 1
    
    def create_anime(self, filename='anime.png', delay=100):
        APNG.from_files(self.files, delay=int(delay)).save(filename)
        for image in self.files:
            os.remove(image) # 不要なファイルは消す
        self.files = []
        return filename

class ACanvas(object):
    width:int    #横幅
    height:int   #高さ
    background: any  #背景色
    image: Image
    draw: ImageDraw
    
    def __init__(self, width=400, height=300, background='white'):
        self.width = width
        self.height = height
        self.background = background
        self.image = Image.new('RGBA', (self.width, self.height), self.background)
        self.draw = ImageDraw.Draw(self.image, 'RGBA')
class AShape(object):    
    width:int  #幅
    height:int #高さ
    cx:int #中心点のx
    cy:int #中心点のy
    scale:float # スケール

    def __init__(self, width, height=None, cx=None, cy=None):
        self.width = width
        self.height = width if height is None else height
        self.cx = self.width / 2 if cx is None else cx
        self.cy = self.height / 2 if cy is None else cy
        self.scale = 1.0

    def bounds(self):  # 左上の座標と幅,高さを計算する
        w = self.width * self.scale
        h = self.height * self.scale
        ox = self.cx - w/2
        oy = self.cy - h/2
        return ox, oy, w, h

    def render(self, canvas: ACanvas, tick: int):
        ox, oy, w, h = self.bounds()
        canvas.draw.rectangle((ox, oy, ox+w, oy+h), fill=(127,127,127))
import math

def test_shape(shape, A=100, B=100, a=1, b=1, delta=0):
    # スタジオを用意
    studio = AStudio(300,300)

    # スタジオに被写体を一つ追加する
    studio.append(shape)

    frames = 60
    for t in range(frames):      
        x = 150 + A*math.cos(a*(2*math.pi*t/frames))
        y = 150 - B*math.sin(b*(2*math.pi*t/frames) + delta)
        # 被写体の中心を移動させる
        shape.cx = x
        shape.cy = y
        # 全ての移動が終わったら、撮影
        studio.render()

    # 動画を編集して表示する
    return studio.create_anime(delay=50)
!wget https://msp.c.yimg.jp/images/v2/FUTi93tXq405grZVGgDqG2AoUavYICofW4nLC9RLaFxLLbdjxiQKsKS-piPBOFVFXe6cXSr-bWRrXvLCliHO9RpmseGXQafStH6wXGhVN263CZNzJSY3L_KgACJZ9neS0jOtlU_sassMNkBLabzYKVGtcR7gIYT1N0890dkkQzI8jXMxCvTME2tPDPYD2uR-RAJVYAHL9T47Hj9jJyD94u9Q6aJPVumiglgvADScermbC9u7_qpyp7FUF3DfNMtJCXKyH9J1lJY77YVa7NswbYiahpiVECs3LhL_kTiVqUFXft967BB1aeEfyS7Dwg31g2TUWon14TQrPwboFlQOaA==/animal_dance.png?errorImage=false
class AImage(AShape):
    color: any

    def __init__(self, width=100, height=None, cx=None, cy=None, image='animal_dance.png?errorImage=false'):
        AShape.__init__(self, width, height, cx, cy)
        if image.startswith('http'):
            # URLから直接読み込む
            self.pic = Image.open(io.BytesIO(requests.get(image).content))
        else:
            self.pic = Image.open(image)

    def render(self, canvas: ACanvas, frame: int):
        ox, oy, w, h = self.bounds()
        pic = self.pic.resize((int(w), int(h)))
        canvas.image.paste(pic, (int(ox), int(oy)), pic)
IPython.display.Image(test_shape(AImage(image='animal_dance.png?errorImage=false')))
