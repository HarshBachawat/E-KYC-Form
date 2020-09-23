import pytesseract
import cv2
import re
import requests

def upscale(img):
	h,w,c = img.shape
	m = min(h,w)
	if m<=300:
		factor = 300//m+1
		img = cv2.resize(img,(w*factor,h*factor),interpolation=cv2.INTER_CUBIC)
	return img

def deskew(img):
	pass

def imgToStr(doctype,filename):
	if doctype=='Aadhar2':
			img = cv2.imread('instance/uploads/'+filename,1)
			img = upscale(img)

			text = pytesseract.image_to_string(img,lang='eng+hin',config='--psm 11')
			pincode = r'\d{6}'
			# add = r'\,\s?([A-Za-z\ \.\-]+)\s?\,\s?[A-Za-z\ \.\-]+\s?\,\s?([A-Za-z\ ]+)\s?(-|,)\s?(\d{6})'
			text = re.sub(r'\n\s?',r' ',text)
			print(text)
			match = re.findall(pincode,text)

			if match:
				print(match)
				match = match[0]
				api = 'https://api.postalpincode.in/pincode/'+match
				region = requests.get(api)
				region = region.json()
				if region[0]['Status']=='Success':
					state = region[0]['PostOffice'][0]['State']
					cities = [k['Block'] for k in region[0]['PostOffice']]
					re_city = '('+'|'.join([r'(\s|\s.*\s)'.join(['('+m+')' for m in l.split()]) if ' ' in l else l for l in cities])+')'
					city = re.findall(re_city,text)
					if city:
						if type(city[0]) is tuple:
							city = ' '.join([o for o in city[0] if o.isalpha()])
						else:
							city = city[0]
					else:
						city = max(cities,key=cities.count)
					return {'status':1,'city':city,'state':state,'pincode':match}
			return {'status':0}

	img = cv2.imread('instance/uploads/'+filename,1)
	img = upscale(img)
	text = pytesseract.image_to_string(img,lang='eng+hin')
	text = re.sub(r'[^A-Za-z0-9\/\s\'\:]','',text)
	text = re.sub(r'(\n\ *)+','\n',text)
	print(text)
	if doctype == 'Pan':
		text = re.sub("[A-Z]?[a-z][a-z\']*",'',text)
		name_and_dob = r'(([A-Z]+ *){1,3})[^A-Z]*(\n\s?\/?\s?)+(([A-Z]+ *){1,3})[^A-Z]*(\n\s?\/?\s?)+(\d{2}\/\d{2}\/\d{4})'
		doc_num = r'[A-Z]{3}[ABCEFGHJLPT][A-Z]\d{4}[A-Z]'

		match1 = re.findall(name_and_dob,text)
		match2 = re.search(doc_num,text)

		if match1 and len(match1[0]) == 7 and match2:
			name = match1[0][0].split()
			father_name = match1[0][3].split()[0]
			fname = name[0]
			lname = name[-1]
			dob = match1[0][-1]
			doc_no = match2.group()

			return {'status':1,'fname':fname,'lname':lname,'fat_name':father_name,'dob':dob,'doc_no':doc_no}

		else:
			return {'status':0}

	elif doctype == 'Aadhar1':
		name = r'([A-Z][a-z]+\ *){2,3}'
		doc_num = r'(\d{4}\ *){3}'
		dob = r':\s*(\d{4}|\d{2}/\d{2}/\d{4})'
		gender = r'(Male|Female)'

		match1 = re.search(name,text)
		match2 = re.search(doc_num,text)
		match3 = re.findall(dob,text)
		match4 = re.search(gender,text)

		if match1 and match2 and match3 and match4:
			name = match1.group().split()
			return {'status':1,'fname':name[0],'lname':name[-1],'dob':match3[0],'doc_no':match2.group(),'gender':match4.group()}
		else:
			return {'status':0}

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
