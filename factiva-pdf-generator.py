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
	magazine = ""

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
		self.line(10,282,200,282)
		self.set_font('Times', 'B', 8)
		self.set_y(-18)
		self.set_x(10)
		self.cell(0,10,"The Publisher's Sale Of This Reprint Does Not Constitute or imply any endorsement or sponsorship of any product, service, company or organization",0,0,'C')
		self.set_y(-15)
		self.set_x(10)
		self.cell(0,10,"Custom Reprints (800) 803-9100  www.djreprints.com. Do not edit or alter reprints, reproductions not permitted",0,0,'C')
		self.line(10,289,200,289)
		self.set_y(-10)
		self.set_x(10)
		self.cell(0,10,u'\u00A9'+" "+ str(datetime.now().year)+" "+self.publisher,0,0,'C')
			
def remove_non_ascii(text):
	return ''.join([i if ord(i) < 128 else "'" for i in text])


# @DEV: Builds PDF from factiva article data and writes it to the FS
# @PARAM: record - dictionary of article data
# @PARAM: cos_apikey - Cloud Object Storage apikey
# @RET: Boolean of success or failure of PDF building
def build_pdf(magazine, title, date, author, text, subtitle):
	article_date = datetime.strptime(date, '%Y%m%d').date()
	article = re.sub(r"no title\s*\n*", "", re.sub(r"'''","'",remove_non_ascii(text)))
	wm_logo = "wm-logo"
	mag_logo = re.sub(r'[^\w\.\-]','',magazine).lower()
	pdf = PDF(format="Letter")
	pdf.magazine = mag_logo
	pdf.add_font("NotoSans", style="", fname="./fonts/NotoSans-Regular.ttf", uni=True)
	pdf.add_font("NotoSans", style="B", fname="./fonts/NotoSans-Bold.ttf", uni=True)
	pdf.add_font("NotoSans", style="I", fname="./fonts/NotoSans-Italic.ttf", uni=True)
	pdf.add_font("NotoSans", style="BI", fname="./fonts/NotoSans-BoldItalic.ttf", uni=True)
	pdf.add_page()
	
	if "thewallstreetjournal" in mag_logo:
		pdf.image("thewallstreetjournal.png",x=15,h=24)
		pdf.set_font('Times', 'B', 10)
		pdf.line(10,33,200,33)
		pdf.set_y(30)
		pdf.cell(0,10,article_date.strftime('%B %e, %Y').upper(),0,0,'L')
		pdf.line(10,37,200,37)
		pdf.set_font('NotoSans', 'B', 18)
		pdf.ln(10)
		pdf.multi_cell(0,9, title, align='C')
		if len(subtitle)>0:
			pdf.ln(2)
			pdf.set_font('NotoSans', 'B', 12)
			pdf.multi_cell(0,7, subtitle, align='C')
		pdf.ln(5)
		article = "By " + author + "\n\n" + article
		
	if "barrons" in mag_logo:
		pdf.image("barrons.png",x=58,h=24)
		pdf.set_font('Times', 'B', 10)
		pdf.line(10,37,200,37)
		pdf.set_y(34)
		pdf.cell(0,10,article_date.strftime('%B %e, %Y').upper(),0,0,'L')
		pdf.line(10,41,200,41)
		pdf.set_font('NotoSans', 'B', size=18)
		pdf.ln(10)
		pdf.multi_cell(0,9, title, align='C')
		if len(subtitle)>0:
			pdf.ln(2)
			pdf.set_font('NotoSans', 'B', 12)
			pdf.multi_cell(0,7, subtitle, align='C')
		pdf.ln(2)
		pdf.set_font('Times', 'B', 10)
		pdf.multi_cell(0,9, "BY " + author.upper(), align='C')
		
	if mag_logo == "financialnews":
		pdf.image(mag_logo+".png",x=12)
		pdf.set_font('Times', 'B', 10)
		pdf.line(10,37,200,37)
		pdf.set_y(34)
		pdf.cell(0,10,article_date.strftime('%B %e, %Y').upper(),0,0,'L')
		pdf.line(10,41,200,41)
		pdf.set_font('NotoSans', 'B', 18)
		pdf.ln(10)
		pdf.multi_cell(0,9, title, align='C')
		if len(subtitle)>0:
			pdf.ln(2)
			pdf.set_font('NotoSans', 'B', 12)
			pdf.multi_cell(0,7, subtitle, align='C')
		pdf.ln(2)
		pdf.set_font('Times', 'B', 10)
		pdf.multi_cell(0,9, "By " + author, align='C')
		
	if ("newswire" in mag_logo or mag_logo == "dowjonesinstitutionalnews") and "german" not in mag_logo:
		pdf.image("newswire.jpg",w=190)
		pdf.set_font('Times', 'B', 10)
		pdf.line(10,30,200,30)
		pdf.set_y(27)
		pdf.cell(0,10,article_date.strftime('%B %e, %Y').upper(),0,0,'L')
		pdf.line(10,34,200,34)
		pdf.set_font('NotoSans', 'B', 18)
		pdf.ln(10)
		pdf.multi_cell(0,9, title, align='C')
		if len(subtitle)>0:
			pdf.ln(2)
			pdf.set_font('NotoSans', 'B', 12)
			pdf.multi_cell(0,7, subtitle, align='C')
		pdf.ln(5)
		article = "By " + author + "\n\n" + article
		
	if "newswire" in mag_logo and "german" in mag_logo:
		pdf.image("newswire.jpg",w=190)
		pdf.set_font('Times', 'B', 10)
		pdf.line(10,30,200,30)
		pdf.set_y(27)
		pdf.cell(0,10,article_date.strftime('%B %e, %Y').upper(),0,0,'L')
		pdf.line(10,34,200,34)
		pdf.set_font('NotoSans', 'B', 18)
		pdf.ln(10)
		pdf.multi_cell(0,9, title, align='C')
		if len(subtitle)>0:
			pdf.ln(2)
			pdf.set_font('NotoSans', 'B', 12)
			pdf.multi_cell(0,7, subtitle, align='C')
		pdf.ln(5)
		
	if mag_logo == "marketwatch":
		pdf.image(mag_logo+".png",w=190)
		pdf.set_font('Times', 'B', 10)
		pdf.line(10,41,200,41)
		pdf.set_y(38)
		pdf.cell(0,10,article_date.strftime('%B %e, %Y').upper(),0,0,'L')
		pdf.line(10,45,200,45)
		pdf.set_font('NotoSans', 'B', 18)
		pdf.ln(10)
		pdf.multi_cell(0,9, title, align='C')
		if len(subtitle)>0:
			pdf.ln(2)
			pdf.set_font('NotoSans', 'B', 12)
			pdf.multi_cell(0,7, subtitle, align='C')
		pdf.ln(5)
		if "marketwatch" not in author.lower():
			article = "By " + author + "\n\n" + article
		
	if mag_logo == "privateequitynews":
		pdf.image(mag_logo+".png",x=60, h=22)
		pdf.set_font('Times', 'B', 10)
		pdf.line(10,33,200,33)
		pdf.set_y(30)
		pdf.cell(0,10,article_date.strftime('%B %e, %Y').upper(),0,0,'L')
		pdf.line(10,37,200,37)
		pdf.set_font('NotoSans', 'B', 18)
		pdf.ln(10)
		pdf.multi_cell(0,9, title, align='C')
		if len(subtitle)>0:
			pdf.ln(2)
			pdf.set_font('NotoSans', 'B', 12)
			pdf.multi_cell(0,7, subtitle, align='C')
		pdf.ln(2)
		pdf.set_font('Times', 'B', 10)
		pdf.multi_cell(0,9, "			By " + author, align='L')
	
	pdf.y0 = pdf.get_y()
	if "thewallstreetjournal" in mag_logo:
		pdf.set_font("NotoSans", size=8)
	else:
		pdf.set_font("NotoSans", size=10)
	if(len(article) > 3250):
		pdf.multi_cell(60,5,article,align='L')
	else:
		pdf.three_col = False
		pdf.multi_cell(0,5,article)
		
	pdf_name = re.sub(r"[^A-Za-z0-9 ]",'',remove_non_ascii(str(title)))[:50]+'_base.pdf'
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
	

file_name_base = re.sub(r"[^A-Za-z0-9 ]",'',remove_non_ascii(str(sys.argv[2])))[:50]
article_text = get_article_text(file_name_base)
pdf_name = build_pdf(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],article_text, sys.argv[5] if len(sys.argv) > 5 else "")
merge_pdf(pdf_name)
os.remove(pdf_name)
os.remove(file_name_base+'.txt')
