# -*- coding: utf-8 -*-
import os
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import matplotlib as plt
def get_text_dic(text):
    text_dic={}
    im = Image.new("RGB", (40, 40), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(os.path.join("fonts", "simhei.ttf"), 28)
    dr.text((10, 5), text, font=font, fill="#000000")
    a=np.array(im)[:,:,0].mean()
    Max=0
    Min=255
    for i in text:
        im = Image.new("RGB", (40, 40), (255, 255, 255))
        dr = ImageDraw.Draw(im)
        dr.text((10, 5), i, font=font, fill="#000000")
        Mean=np.array(im)[:,:,0].mean()
        text_dic[i]=Mean
        if Mean>Max:
            Max=Mean
        if Mean<Min:
            Min=Mean
    for i in text_dic.keys():
        text_dic[i]=(text_dic[i]-Min)/(Max-Min)*255 #归一化
    return text_dic


def get_image_dic(img_dir):
    img_dic={}
    Max=0
    Min=255
    img_list=os.listdir(img_dir)
    for img_name in img_list:
        img_path=os.path.join(img_dir,img_name)
        im=Image.open(img_path)
        im = im.resize((64, 64))
        Mean=np.array(im)[:,:,0].mean()
        img_dic[img_path]=Mean
        if Mean>Max:
            Max=Mean
        if Mean<Min:
            Min=Mean
    for i in img_dic.keys():
        img_dic[i]=(img_dic[i]-Min)/(Max-Min)*255 #归一化
        
        
    return img_dic














 
source_image_path='a.jpg'
text = "床前明月光，疑是地上霜。举头望明月，低头思故乡 从前有座山 山上有座庙 庙里有个老和尚"
img_dir="./pic_res"
text_resolution=100
image_resolution=64
small_pic_res=32
re=""
dic=get_text_dic(text)
min_err=1000
min_key=""
source_im=Image.open(source_image_path)
im1 = source_im.convert('L') 
x=text_resolution
im1 = np.array(im1.resize((x, int(x*3/4))))
imax=im1.max()
imin=im1.min()

for i in np.array(im1):
    for j in i:
        j=int((j-imin)/(imax-imin)*255)
        for key in dic.keys():
            err=abs(dic[key]-j)
            if err<min_err:
                min_err=err
                min_key=key
        re+=min_key
        min_err=1000
        min_key=""
    re+="\r\n"
with open("re.txt","w") as f:
        f.write(re)
x=image_resolution    
im_re=np.zeros( (x*small_pic_res,x*small_pic_res,3) )
source_im=Image.open(source_image_path)
im1 = source_im.convert('L') 
im1 = np.array(im1.resize((x, x)))
imax=im1.max()
imin=im1.min()
dic=get_image_dic(img_dir)
ii=0
jj=0
for i in np.array(im1):
    for j in i:
        j=int((j-imin)/(imax-imin)*255)
        for key in dic.keys():
            err=abs(dic[key]-j)
            if err<min_err:
                min_err=err
                min_key=key
        b=Image.open(min_key)
        b=b.resize((small_pic_res,small_pic_res))
        xxxx=np.array(b)
        im_re[ii*small_pic_res:ii*small_pic_res+small_pic_res,jj*small_pic_res:jj*small_pic_res+small_pic_res]=xxxx
        jj+=1
        min_err=1000
        min_key=""
    ii+=1
    jj=0
        
plt.image.imsave('im_re.jpg', im_re/255)
Image.open('im_re.jpg').show()    
            