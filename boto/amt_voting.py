#robert

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,Binary

ACCESS_ID  = 'secret'
SECRET_KEY = 'secret'
HOST       = 'mechanicalturk.sandbox.amazonaws.com'



def boto_injector(img_links):
# Extending boto to Binary datatype in SelectionAnswer
# Generates radiobutton option per link
	inject_thumb_size = 'l' # from http://api.imgur.com/models/image
	inject_img_type   = 'png'
	inject_pre  = '<MimeType><Type>image</Type><SubType>'+\
		inject_img_type+'</SubType></MimeType><DataURL>'
	inject_post = '</DataURL><AltText>Letter Image</AltText>'
	radio_options = []
	for index, item in enumerate(img_links):
		link = inject_pre+item+inject_thumb_size+"."+\
			inject_img_type+inject_post
		radio_options.append( (link,index) )
	# SelectionAnswer(...selections=radio_options...)
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
	#-HIT Properties
	title      = 'Vote on the best letter'
	description= ('View the images and choose the letter which looks the best')
	keywords   = 'image, voting, opinions'	
	
	#-Question Overview
	overview = Overview()
	overview.append_field('Title', 'Choose the best looking letter')
	
	#-Question
	qc1 = QuestionContent()
	qc1.append_field('Title','Select Letter')
	
	# Generate Awnsers 1 per imgur_links[]
	choices = boto_injector(imgur_links)
	
	#-Awnser Choices
	fta1 = SelectionAnswer(min=1, max=1,style='radiobutton',\
		selections=choices,type='binary',other=False)
	
	q1 = Question(identifier='design',content=qc1,\
		answer_spec=AnswerSpecification(fta1),is_required=True)
	
	#-Question Form
	question_form = QuestionForm()
	question_form.append(overview)
	question_form.append(q1)
	
	#Put the HIT up
	#mturk_conn.create_hit(questions=question_form,max_assignments=1,title=title,description=description,keywords=keywords,duration = 60*1,reward=0.00)

def main():
	mturk_conn = connect_AMT()
	
	# todo
	# Load each letter from file
	# parse each letter file into HIT's of some # (5)
	# issue HITS
	img_dict = load_links("A.imgur")
	create_HIT(mturk_conn,'A',img_dict['A'])

if __name__ == "__main__":
    main()
