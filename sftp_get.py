import paramiko    
import os    
import datetime   
import stat 
hostname='10.0.2.15'
username='haoren'
password='123456'
port=22
local_dir='C:\Users\Hallam\Desktop\hello\\'
remote_dir='\hello\\'

print os.path.isfile(local_dir+"Test.py")


def sftp_connect(hostname,port,username,password):
    try:    
            t=paramiko.Transport((hostname,port))    
            t.connect(username=username,password=password)    
            sftp=paramiko.SFTPClient.from_transport(t) 
            return sftp
                            
    except Exception:    
        print "error!"           
    # t.close()

def is_dir(local_dir,remote_dir,f,sftp):
    if stat.S_ISDIR(f.st_mode):
        # print '1'+local_dir 
        local_path = local_dir+f.filename+"\\"        
        mkdir(local_path)
        # print '2'+local_path
        remote_path = remote_dir+f.filename+"\\"
        # print '3'+remote_path
        files = sftp.listdir_attr(remote_path)
        for f in files:
            is_dir(local_path,remote_path,f,sftp)
    else:
        get_file(local_dir,remote_dir,f,sftp)
        print local_dir+f.filename
        return True

def index(hostname,port,username,password,local_dir,remote_dir):
    sftp = sftp_connect(hostname,port,username,password)
    mkdir(local_dir)   
    # last_get(local_dir,remote_dir,sftp)
    files=sftp.listdir_attr(remote_dir) 
    for f in files: 
         is_dir(local_dir,remote_dir,f,sftp)

def get_file(local_dir,remote_dir,f,sftp):          
    print ''    
    print '#########################################'
    print 'Beginning to download file  from %s  %s ' % (hostname,datetime.datetime.now())    
    print 'Downloading file:',os.path.join(remote_dir,f.filename)    

    sftp.get(os.path.join(remote_dir,f.filename),os.path.join(local_dir,f.filename))    
   # sftp.put(os.path.join(local_dir,f),os.path.join(remote_dir,f))    

    print 'Download file success %s ' % datetime.datetime.now()    
    print ''    
    print '##########################################'
    print "success for getfile"


def mkdir (local_dir):
    local_dir = local_dir.strip()
    local_dir = local_dir.rstrip("\\")

    isExists = os.path.exists(local_dir)

    if not isExists:
        os.makedirs(local_dir)
        print local_dir+" is success build"
        return True
    else:
        print local_dir+" is exists"
        return False



index(hostname,port,username,password,local_dir,remote_dir)
