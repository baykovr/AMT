#robert

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,Binary

ACCESS_ID  = 'SECRET'
SECRET_KEY = 'SECRET'
HOST       = 'mechanicalturk.sandbox.amazonaws.com'


#"Does not yet implement Binary selection options" Yeah ok -Robert.
def boto_injector(img_links):
# A HIT is just xml, so boto is just an xml generator really.

	inject_thumb_size = 'l' # from http://api.imgur.com/models/image
	inject_img_type   = 'png'
	inject_pre  = '<MimeType><Type>image</Type><SubType>'+inject_img_type+'</SubType></MimeType><DataURL>'
	inject_post = '</DataURL><AltText>Letter Image</AltText>'
	
	radio_options = []
	for index, item in enumerate(img_links):
		#of form (link,0) 
		link = inject_pre+item+inject_thumb_size+"."+inject_img_type+inject_post
		radio_options.append( (link,index) )
	return radio_options
		

def load_links(link_file):
# Load file w/ imgur links
# first line '#Letter'
# followed by links
# returns dict [Letter:Links[]]
	try:
		frmt_chk = True;
		letter   = ''
		img_file = open(link_file, "r" )
		img_links = []
		
		for line in img_file:
			#Verify first line is of form #A
			if frmt_chk:
				if line[0] == '#':
					letter = line[1]
					frmt_chk = False
				else:
					raise "First line must be of form #[Letter], ie #A"
			else:
				img_links.append( line.rstrip() )
		img_file.close()
		return {letter:img_links}
	except Exception as e1:
		print "[Error reading imgur file]",e1
		exit(1)

def connect_AMT():
# Open connections to HOST
# using ACCESS_ID,SECRET_KEY
# obtain from https://portal.aws.amazon.com/gp/aws/securityCredentials#access_credentials
	mturk_conn = None
	try:
		mturk_conn    = MTurkConnection(aws_access_key_id=ACCESS_ID,aws_secret_access_key=SECRET_KEY,host=HOST)
		#will throw if not connected
		canary = mturk_conn.get_account_balance()
	except Exception as e1:
		print "[Error Connecting]",e1
		print "[Exiting]"
		exit(1)
	return mturk_conn

def create_HIT(mturk_conn,letter,imgur_links):
# Given a char and set of links
# create and push HIT
	try:
		canary = mturk_conn.get_account_balance()
	except Exception as e1:
		print "[Error Connecting]",e1
		print "[Exiting]"
		exit(1)
	
	hit = None
	return hit

def main():
	mturk_conn = connect_AMT()
	img_dict = load_links("A.imgur")

	# -- HIT Properties
	title       = 'Vote on the best letter'
	description = ('View the images and choose the letter which looks the best')
	keywords    = 'image, voting, opinions'
	#ratings =[('Very Bad','0'),('Bad','1'),('Not bad','2'),('Good','3'),('Very Good','4')]
	
	#ratings = [('<MimeType><Type>image</Type><SubType>png</SubType></MimeType><DataURL>http://i.imgur.com/y3kU3ffl.png</DataURL><AltText>The game board, with X to move.</AltText>','0')]
	
	ratings = boto_injector(img_dict['A'])
	print ratings
	#---------------  BUILD OVERVIEW ------------------- 
	overview = Overview()
	overview.append_field('Title', 'Choose the best looking letter')
	#---------------  BUILD QUESTION 1 -------------------
 
	qc1 = QuestionContent()
	qc1.append_field('Title','Select Letter')
	#qc1.append(Binary(type='image',subtype='png',url='http://i.imgur.com/y3kU3ff.png',alt_text='X'))
	
	fta1 = SelectionAnswer(min=1, max=1,style='radiobutton',selections=ratings,type='binary',other=False)
	print fta1.get_as_xml()
	q1   = Question(identifier='design',content=qc1,answer_spec=AnswerSpecification(fta1),is_required=True)
 
	#--------------- BUILD THE QUESTION FORM -------------------
	question_form = QuestionForm()
	question_form.append(overview)
	question_form.append(q1)
	#--------------- CREATE THE HIT -------------------
	mturk_conn.create_hit(questions=question_form,max_assignments=1,title=title,description=description,keywords=keywords,duration = 60*1,reward=0.00)

if __name__ == "__main__":
    main()
