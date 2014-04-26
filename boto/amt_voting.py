#robert

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,Binary

ACCESS_ID  = ''
SECRET_KEY = ''
HOST       = 'mechanicalturk.amazonaws.com'
INFILE     = 'jason_input.txt'
IMGSIZE    = 'm'
IMGTYPE    = 'png'
HIT_REWARD = 0.01   #Cost of hit, in cents.
HIT_TIME   = 240    #Time for each hit (minuets)

def boto_injector(img_links):
# Extending boto to Binary datatype in SelectionAnswer
# Generates radiobutton option per link
	inject_thumb_size = IMGSIZE # from http://api.imgur.com/models/image
	inject_img_type   = IMGTYPE
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
		flush    = False;
		first_ln = True
		letter   = ''
		img_file = open(link_file, "r" )
		img_links = []
		img_dict  = {}
		
		for line in img_file:
			if line[0] == '#':
				if first_ln:
					letter   = line[1]
					first_ln = False
				if flush:
					img_dict[letter] = img_links
					letter = line[1]
					img_links = []
				flush=False
			else:
				img_links.append( line.rstrip() )
				flush=True
		img_file.close()
		return img_dict
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
		print "Connection to amt established."
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
	title      = 'Select the Best Character'
	description= ('Of the available options below, please select the best representation of the following chracter: '+letter+'\n Your vote will help determine which character gets selected to be used in a collaborative typeface.')
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
	try:
		mturk_conn.create_hit(questions=question_form,max_assignments=1,title=title,description=description,keywords=keywords,duration = 60*HIT_TIME,reward=0.01)
		print "Hit issued for item:",letter
	except Exception as e1:
		print "Could not issue hit",e1
		

def approve_all_hits(mturk_conn):
    print 'Approving all revieable hits.'
    page_size = 50
    hits = mturk_conn.get_reviewable_hits(page_size=page_size)
    print "Total results to fetch %s " % hits.TotalNumResults
    print "Request hits page %i" % 1
    total_pages = float(hits.TotalNumResults)/page_size
    int_total= int(total_pages)
    if(total_pages-int_total>0):
        total_pages = int_total+1
    else:
        total_pages = int_total
    pn = 1
    while pn < total_pages:
        pn = pn + 1
        print "Request hits page %i" % pn
        temp_hits = mturk_conn.get_reviewable_hits(page_size=page_size,page_number=pn)
        hits.extend(temp_hits)
    for hit in hits:
		assignments = mturk_conn.get_assignments(hit.HITId)
		print '-'*60
		print "HIT"
		print "Hit ID     :",str(hit.HITId)
		print "Assignments:",len(assignments)
		for assignment in assignments:
			print "Worker ID  :",assignment.WorkerId
			print "Aproving HIT"
			mturk_conn.approve_assignment(assignment.AssignmentId)
		
def list_awaiting_review(mturk_conn):
    page_size = 50
    hits = mturk_conn.get_reviewable_hits(page_size=page_size)
    print "Total results to fetch %s " % hits.TotalNumResults
    print "Request hits page %i" % 1
    total_pages = float(hits.TotalNumResults)/page_size
    int_total= int(total_pages)
    if(total_pages-int_total>0):
        total_pages = int_total+1
    else:
        total_pages = int_total
    pn = 1
    while pn < total_pages:
        pn = pn + 1
        print "Request hits page %i" % pn
        temp_hits = mturk_conn.get_reviewable_hits(page_size=page_size,page_number=pn)
        hits.extend(temp_hits)
	for hit in hits:
		print "HIT----------------------------------------"
		assignments = mturk_conn.get_assignments(hit.HITId)
		print '-'*60
		print "Hit ID     :",str(hit.HITId)
		print "Assignments:",len(assignments)
		for assignment in assignments:
			print "Status     :",assignment.AssignmentStatus
			print "Worker ID  :",assignment.WorkerId
					
def list_all_hits(mturk_conn):
    print 'Available Hits'
    hits = mturk_conn.get_all_hits()
    for hit in hits:
		assignments = mturk_conn.get_assignments(hit.HITId)
		print "HIT----------------------------------------"
		print hit.Title
		print hit.Description
		print "Hit ID     :",str(hit.HITId)
		print "Assignments:",len(assignments)
		for assignment in assignments:
			print "Worker ID  :",assignment.WorkerId
			#print "Aproving HIT"
			#mturk_conn.approve_assignment(assignment.AssignmentId)
		#print "DELETED"
		#mturk_conn.disable_hit(hit.HITId)

def turk():
	mturk_conn = connect_AMT()
	print '-'*60
	print 'HOST         ',HOST   
	print 'INFILE       ',INFILE     
	print 'IMGSIZE      ',IMGSIZE   
	print 'IMGTYPE      ',IMGTYPE    
	print 'HIT_REWARD(c)',HIT_REWARD
	print 'HIT_TIME(min)',HIT_TIME 
	while(True):
		print '-'*60
		print "Choose task"
		print "[1] Issue hits from file"
		print "[2] List all hits"
		print "[3] List hits awaiting approval"
		print "[4] Approve all hits"
		print "[5] Get Balance"
		print "[6] Exit"
		choice = raw_input('#').lower()
		if choice == "1":
			print "Using file:",INFILE
			img_dict = load_links(INFILE)
			for letter,images in img_dict.items():
				create_HIT(mturk_conn,letter,images)
		elif choice == "2":
			list_all_hits(mturk_conn)
			
			
		elif choice == "3":
			list_awaiting_review(mturk_conn)
			
		
		elif choice == "4":
			approve_all_hits(mturk_conn)
		
		elif choice == "5":
			print "Balance:",mturk_conn.get_account_balance()
		
		elif choice == "6":
			exit(0)
		else:
			print "unknown input"

	#img_dict = load_links("jason_input.txt")
	#mturk_conn = connect_AMT()
	#RM_all_hits(mturk_conn)
	#for letter,images in img_dict.items():
	#		create_HIT(mturk_conn,letter,images)

	
def main():
	turk()
			
		
if __name__ == "__main__":
    main()
