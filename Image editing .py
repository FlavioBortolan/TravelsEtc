#!/usr/bin/env python
# coding: utf-8

# In[2]:


from PIL import Image
#Open image using Image module


def crop_to_3_4(dirname, fname, target_dirfname):

    im = Image.open( dirname + fname + ".jpg")
    #Show actual Image
    im.show()

    width = im.size[0]
    heigth = im.size[1]

    print('width = ' + str(width))
    print('heigth = ' + str(heigth))

    ratio= heigth/width
    print('ratio = ' + str(ratio))

    target_ratio = 0.75

    if(heigth > width*target_ratio):

        cr_width = width
        cr_heigth = width*target_ratio

        cr_col = 0 
        cr_row = (heigth-cr_heigth)/2

    else:

        cr_heigth = heigth
        cr_width = heigth/target_ratio

        cr_col = (width-cr_width)/2 
        cr_row = 0

    #left, upper, right, lowe
    #Crop
    cropped = im.crop((cr_col, cr_row, cr_col + cr_width, cr_row + cr_heigth))

    #Display the cropped portion
    cropped.show()

    crop_fname = target_dirfname + fname + '.jpg'
    #Save the cropped image
    cropped.save(crop_fname)

    im.show()


# In[3]:


def subsample(dirname, fname, target_dirfname, target_width):

    im = Image.open( dirname + fname + ".jpg")
    #Show actual Image
    im.show()
    
    width = im.size[0]
    heigth = im.size[1]
    
    #image size
    size=(target_width, int(heigth * (target_width/width)))
    #resize image
    out = im.resize(size, Image.LANCZOS)
    out_fname = target_dirfname + fname + '.jpg'
    #save resized image
    out.save(out_fname)

    out.show()


# In[5]:


dirname = "C:/tmp/"
fname = 'Risorgive di Bressanvido'
target_dirfname = 'C:/Flavio/Software/Django/MyProjects/TravelsEtc/TravelsApp/static/Images/'

crop_to_3_4(dirname, fname, target_dirfname)

#target_width=800
#subsample(dirname, fname, target_dirfname, target_width)


# In[ ]:




