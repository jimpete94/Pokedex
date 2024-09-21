from PIL import Image
# Skeleton script to process images into the Pokédex format

inPath = ''
outPath = ''
newSize = (500, 300)

image = Image.open(inPath + '', 'r')

new_image = Image.new('RGBA', (0, 0), "WHITE")
new_image.paste(image, (0,0), image)
new_image = new_image.resize(newSize)
new_image = new_image.convert('RGB').save('', "JPEG")

