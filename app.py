from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from pathlib import Path
import glob
from PIL import Image, ExifTags

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'photocollection'

configure_uploads(app, photos)

@app.route('/upload', methods=['GET','POST'])
def upload():
	if request.method == 'POST' and 'thefile' in request.files:
		image_filename = photos.save(request.files['thefile'])
		exif_data = read_exif(image_filename)
		print(exif_data)
		return f'<h1>{image_filename}</h1>'

	return render_template('upload.html')

def read_exif(thefile):
	for filename in glob.glob('photocollection/{}'.format(thefile)):
		im = Image.open(filename)
	return Image.open(im).info['parsed_exif']

if __name__ == '__main__':
	app.run()