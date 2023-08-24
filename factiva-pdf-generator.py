import sys
import os
import re
from datetime import timezone, datetime
import fpdf
from fpdf import FPDF
import PyPDF2
#fpdf.set_global("SYSTEM_TTFONTS", os.path.join(os.path.dirname(__file__),'fonts'))


class PDF(FPDF):

	col = 0
	y0 = 0
	three_col = True
	publisher = "Dow Jones"

	def header(self):
		self.y0 = self.get_y()
		
	def set_col(self, col):
		self.col = col
		x = 10 + col * 65
		self.set_left_margin(x)
		self.set_x(x)
		
	def accept_page_break(self):
		if(not self.three_col):
			return True
		if(self.col < 2):
			self.set_col(self.col + 1)
			self.set_y(self.y0)
			return False
		else:
			self.set_col(0)
			return True
			
	def footer(self):
		self.set_y(-15)
		self.set_font('Helvetica', 'B', 11)
		self.cell(0,10,u'\u00A9'+" "+ str(datetime.now().year)+" "+self.publisher,0,0,'R')
			
def remove_non_ascii(text):
	return ''.join([i if ord(i) < 128 else "'" for i in text])


# @DEV: Builds PDF from factiva article data and writes it to the FS
# @PARAM: record - dictionary of article data
# @PARAM: cos_apikey - Cloud Object Storage apikey
# @RET: Boolean of success or failure of PDF building
def build_pdf(magazine, title, text):
	article = re.sub(r"no title\s*\n*", "", re.sub(r"'''","'",remove_non_ascii(text)))
	if(len(article)<10):
		return ""
	wm_logo = "wm-logo"
	mag_logo = re.sub(r'[^\w\.\-]','',magazine).lower()
	pdf = PDF()
	pdf.add_font("NotoSans", style="", fname="./fonts/NotoSans-Regular.ttf", uni=True)
	pdf.add_font("NotoSans", style="B", fname="./fonts/NotoSans-Bold.ttf", uni=True)
	pdf.add_font("NotoSans", style="I", fname="./fonts/NotoSans-Italic.ttf", uni=True)
	pdf.add_font("NotoSans", style="BI", fname="./fonts/NotoSans-BoldItalic.ttf", uni=True)
	pdf.add_page()
	pdf.image(mag_logo+".png",h=15)
	pdf.set_font('NotoSans', 'B', 18)
	pdf.ln(10)
	pdf.multi_cell(0,10, title, align='C')
	pdf.ln(5)
	pdf.y0 = pdf.get_y()
	pdf.set_font("NotoSans", size=10)
	if(len(article) > 3250):
		pdf.multi_cell(60,5,article)
	else:
		pdf.three_col = False
		pdf.multi_cell(0,5,article)
	pdf_name = remove_non_ascii(str(title[:50]))+'_base.pdf'
	pdf.output(pdf_name)
	return pdf_name
	

# @DEV: Adds watermark to PDF by merging with a watermark PDF
# @PARAM: pdf_file - file name of base PDF file
def merge_pdf(pdf_file):
	watermark = "sample1.pdf"
	input_file = open(pdf_file,'rb')
	input_pdf = PyPDF2.PdfFileReader(pdf_file)
	watermark_file = open(watermark,'rb')
	watermark_pdf = PyPDF2.PdfFileReader(watermark_file)
	
	watermark_page = watermark_pdf.getPage(0)
	output_pdf = PyPDF2.PdfFileWriter()
	
	for i in range(input_pdf.getNumPages()):
		pdf_page = input_pdf.getPage(i)
		pdf_page.mergePage(watermark_page)
		output_pdf.addPage(pdf_page)
	
	output_filename = re.sub(r'_base','',pdf_file)
	file = open("pdf/" + output_filename, 'wb')
	output_pdf.write(file)
	
	
def get_article_text(file_name_base):
	with open(file_name_base+'.txt','r') as f:
		return f.read()
	

file_name_base = remove_non_ascii(str(sys.argv[2])[:50])
article_text = get_article_text(file_name_base)
pdf_name = build_pdf(sys.argv[1],sys.argv[2],article_text)
merge_pdf(pdf_name)
os.remove(pdf_name)