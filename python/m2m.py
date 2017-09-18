import sys
import os
import os.path
import boto3
from pathlib import Path
from botocore.client import Config

# CONSTATNS ####################################################
M2M_CONFIG_FILE='m2m_config.txt'

# GLOBALS ####################################################
#read from m2m-config.txt
ACCESS_KEY_ID = ''
ACCESS_SECRET_KEY = ''
BUCKET_NAME = ''
ANDROID_MIDDLE_PATH=''
#found from command line
PY_EXE_LOCATION =''
OP_CHOICE = ''
OS_CHOICE = ''
ARCH_CHOICE = ''
CWD=''

# FUNCTIONS ####################################################
def print_valid_commands(commingfrom=None):
	print ('Invalid command type - ', commingfrom)
	print ('valid commands are:')
	print ('---------------------')
	print ('m2m upload android')	
	print ('m2m upload android x86')
	print ('m2m upload android arm')
	print ('m2m list')		
	sys.exit()
	
def print_keylists_as_text(desc=None):
	print('print_keylists()-------start-------', desc)
	print("ACCESS_KEY_ID- ", ACCESS_KEY_ID)
	print("ACCESS_SECRET_KEY- " , ACCESS_SECRET_KEY)
	print("BUCKET_NAME- " , BUCKET_NAME)	
	print("ANDROID_MIDDLE_PATH- " , ANDROID_MIDDLE_PATH)	
	
def print_globals():
	print ('print_globals()')
	print ('PY_EXE_LOCATION-',PY_EXE_LOCATION)
	print ('OP_CHOICE-',OP_CHOICE)
	print ('OS_CHOICE-',OS_CHOICE)
	print ('ARCH_CHOICE-',ARCH_CHOICE)
	print ('CWD-',CWD)
	
	
def m2m_config_sample_print():
	print('ACCESS_KEY_ID:AKIAJE7URAUUUOZI4A')
	print('ACCESS_SECRET_KEY:XKdpY+y4DKlfcaIlgxZVhNDYM3gfOojnNSD97N')
	print('BUCKET_NAME:trut-bucket')
	print('ANDROID_MIDDLE_PATH:platforms,android,build,outputs,apk')
	
	
def read_m2mconfig_assign_global(m2m_config_filepath):	
	global ACCESS_KEY_ID,ACCESS_SECRET_KEY,BUCKET_NAME,ANDROID_MIDDLE_PATH
	my_file = Path(m2m_config_filepath)	
	if my_file.is_file():
		#print('file exist')
		with open(m2m_config_filepath) as filereader:
			filecontents = filereader.read().splitlines()
			#print ("filecontents- " , filecontents)				
			for eachline in filecontents:
				#print ('eachline-',eachline)					
				if (eachline.find('ACCESS_KEY_ID:')!=-1)		:ACCESS_KEY_ID=eachline.replace('ACCESS_KEY_ID:', '')						
				if (eachline.find('ACCESS_SECRET_KEY:')!=-1)	:ACCESS_SECRET_KEY=eachline.replace('ACCESS_SECRET_KEY:', '')							
				if (eachline.find('BUCKET_NAME:')!=-1)			:BUCKET_NAME=eachline.replace('BUCKET_NAME:', '')	
				if (eachline.find('ANDROID_MIDDLE_PATH:')!=-1)	:ANDROID_MIDDLE_PATH=eachline.replace('ANDROID_MIDDLE_PATH:', '')	
			#print_keylists_as_text()
	else:
		print ('Error: File(m2m_config.txt) does not exist here - ', m2m_config_filepath)
		print ('The file must have following information and located where the m2m command get executed')
		m2m_config_sample_print()


def find_android_app_base_path():
	_android_middle_path_formatted = ANDROID_MIDDLE_PATH.split(",")
	androidapk_middle=os.path.join(CWD,*_android_middle_path_formatted)
	#print('find_android_app_base_path() - ',androidapk_middle)
	APK_PATH= os.path.join(CWD, androidapk_middle)
	return APK_PATH
	
def loop_all_apps_and_return_app_pathlist(APP_PATH):	
	listofapps = [x for x in os.listdir(APP_PATH) ]	
	return listofapps

def find_abs_path(apppath):
	basepath=find_android_app_base_path()
	fullpath= os.path.join(basepath,apppath)
	return fullpath
		
		
def upload_to_s3(filepath, filename):
	print ('upload_to_s3 started : ', filepath )			
	data = open(filepath, 'rb')
	s3 = boto3.resource('s3',aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_SECRET_KEY,config=Config(signature_version='s3v4'))
	s3.Bucket(BUCKET_NAME).put_object(Key=filename, Body=data)
	print ('upload_to_s3 ended : ', filepath )	
	
def prepare_for_upload(listofapps): 
	for app in listofapps:
		abspath = find_abs_path(app)
		if(ARCH_CHOICE == 'x86'):
			if (app.find('-x86') != -1):				                
				upload_to_s3(abspath, app)
				
		if(ARCH_CHOICE == 'arm'):
			if (app.find('-arm') != -1):				                
				upload_to_s3(abspath, app)
				
		if(ARCH_CHOICE == ''):		
			upload_to_s3(abspath, app)
				
	print('******************* all upload completed ************* ')

def list_from_s3():
	print ('***************list_from_s3 ********************' )		
	s3 = boto3.resource('s3',aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_SECRET_KEY,config=Config(signature_version='s3v4'))
	bucket = s3.Bucket(BUCKET_NAME)
	for s3_file in bucket.objects.all():
		print(s3_file.key)
	print('******************* list completed ************* ')
	

def fill_globals_from_commands(args):
	global PY_EXE_LOCATION, OP_CHOICE,OS_CHOICE,ARCH_CHOICE	
	argslen = len(args)
	if (argslen == 1): 
		PY_EXE_LOCATION = args[0]	
	if (argslen == 2): 
		PY_EXE_LOCATION = args[0]	
		OP_CHOICE = args[1]	
	if (argslen == 3): 
		PY_EXE_LOCATION = args[0]	
		OP_CHOICE = args[1]	
		OS_CHOICE = args[2]	
	if (argslen == 4): 
		PY_EXE_LOCATION = args[0]	
		OP_CHOICE = args[1]	
		OS_CHOICE = args[2]	
		ARCH_CHOICE = args[3]
	

		
def show_valid_commands():
	_arch_choice = False
	
	if (OP_CHOICE == '' ) : print_valid_commands('1')
		
	if (OP_CHOICE == 'list'):return
						
	if (OP_CHOICE == 'upload' ): True
	else:	print_valid_commands('2')
				
	if (OP_CHOICE == 'upload' ) and  (OS_CHOICE == 'android') : True
	else:	print_valid_commands('3')
			
	if ((ARCH_CHOICE == 'x86' ) or (ARCH_CHOICE == 'arm' ) or (ARCH_CHOICE == '' ) ) : 	_arch_choice = True
	else:	print_valid_commands('4')
		


def handle_param_issues(args):
	#print('sys.argv-',args)
	#print('sys.argv.length-',len(args))
	fill_globals_from_commands(args)	
	show_valid_commands()
	
		
# MAIN PROGRAM ####################################################
		
handle_param_issues(sys.argv)
CWD = os.getcwd()
#print('CWD-',CWD)
#print_globals()
m2m_config_filepath= os.path.join(CWD, M2M_CONFIG_FILE)
#print('m2m_config_filepath-',m2m_config_filepath)	
read_m2mconfig_assign_global(m2m_config_filepath)
#print_keylists_as_text()

if OP_CHOICE=='upload':	
	if OS_CHOICE=='android':
		#print ('option_os==android')
		APP_BASEPATH = find_android_app_base_path()
		listofapps = loop_all_apps_and_return_app_pathlist(APP_BASEPATH)
		#print ('listofapps', listofapps)
		prepare_for_upload(listofapps)						
elif OP_CHOICE=='list':
	list_from_s3()


