import paramiko    
import os    
import datetime   
import stat 
import re
hostname='192.168.1.68'
username='haoren'
password='123456'
port=22
local_dir='C:\Users\Hallam\Desktop\hello\\'
remote_dir='\\hello\\'

def sftp_connect(hostname,port,username,password):
    try:    
            t=paramiko.Transport((hostname,port))    
            t.connect(username=username,password=password)    
            sftp=paramiko.SFTPClient.from_transport(t) 
            return sftp,t
                            
    except Exception:

        return False           
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

def sftp_start(hostname,port,username,password,local_dir,remote_dir):
    sftp,t = sftp_connect(hostname,port,username,password)
    if not sftp:
        print "connect fail"
    else:
        del_mkdir(local_dir)
        mkdir(local_dir) 
        try:
                sftp.stat(remote_dir)
                print "the remote_dir is exist"     
                files=sftp.listdir_attr(remote_dir)
                for f in files: 
                        version = mat_ch(f)
                        is_dir(local_dir,remote_dir,f,sftp)
                t.close()
                return version
        except Exception:
                print "the remote_dir is not exist"

def get_file(local_dir,remote_dir,f,sftp):          
    print ''    
    print '#########################################'
    print 'Beginning to download file  from %s  %s ' % (hostname,datetime.datetime.now())    
    print 'Downloading file:',os.path.join(remote_dir,f.filename)    

    sftp.get(os.path.join(remote_dir,f.filename),os.path.join(local_dir,f.filename))    
    # sftp.put(os.path.join(local_dir,f.filename),os.path.join(remote_dir,f.filename))    

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

def del_mkdir(local_dir):
    os.system("del /F /S /Q "+local_dir)
    print("delete success")


def mat_ch(f):
    pattern = re.compile(r'(?<=RLHost_X798_Flex_)(\d+\.\d+\.\d+)')
    match = pattern.search(f.filename)
    if match:
        # print f.filename
        return match.group()
    else:
        return False

# for i in xrange(1,3):
    # path = local_dir+'hello'+str(i)+'\\'
    # print path
    # mkdir(path)
version = sftp_start(hostname,port,username,password,local_dir,remote_dir)
    # print version
# os.system("C:\Users\Hallam\Desktop\TMUpdateTool\WinSCP\WinSCP.com sftp://macbook:123456@172.15.1.77")
