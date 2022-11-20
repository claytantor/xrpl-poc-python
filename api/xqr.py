# import modules
import qrcode
from PIL import Image
import os

def generate_qr_code(data):

	print('File name :    ', os.path.basename(__file__))
	print('Directory Name:     ', os.path.dirname(__file__))

	# taking image which user wants
	# in the QR code center
	Logo_link = f'{os.path.dirname(__file__)}/assets/xicon_mobile.png'

	logo = Image.open(Logo_link)

	# taking base width
	basewidth = 100

	# adjust image size
	wpercent = (basewidth/float(logo.size[0]))
	hsize = int((float(logo.size[1])*float(wpercent)))
	logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)

	# qr = qrcode.QRCode(
	# 	version=1,
	# 	error_correction=qrcode.constants.ERROR_CORRECT_L,
	# 	box_size=10,
	# 	border=4,
	# )

	QRcode = qrcode.QRCode(
		error_correction=qrcode.constants.ERROR_CORRECT_H,
		box_size=10,
		border=1,
	)

	# taking url or text
	url = data['url']

	# adding URL or text to QRcode
	QRcode.add_data(url)

	# generating QR code
	QRcode.make()

	# taking color name from user
	QRcolor = 'Black'

	# adding color to QR code
	QRimg = QRcode.make_image(
		fill_color=QRcolor, back_color="white").convert('RGB')

	# set size of QR code
	pos = ((QRimg.size[0] - logo.size[0]) // 2,
		(QRimg.size[1] - logo.size[1]) // 2)
	QRimg.paste(logo, pos)

	# is a PilImage
	return QRimg

