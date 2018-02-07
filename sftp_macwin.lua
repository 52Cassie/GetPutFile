require("lfs")

local executor 			= "WinSCP\\WinSCP.com"   --打开用来连接
local script_put_path 	= "WinSCP\\winscp_put"   --打开用来放文件
local script_get_path 	= "WinSCP\\winscp_get"   --打开用来取文件

local script_header = [[
	open sftp://USERNAME:PASSWORD@HOSTADDRESS
]]

local put_script_ori = [[
	put "SOURCE_FILE" "TARGET_FILE"
	close
	exit
]]

local ls_script = [[
	ls "TARGET_FILE"
	close
	exit
]]

script_execute = script_header
--需修改的参数
username = "mac"
password = "123456"
hostaddress = "172.15.2.210"
target_file = "/Users/mac/Desktop/test"
source_file = "C:\\Users\\cassie\\Desktop\\lua"

function connect( username,password,hostaddress )
	if username and password and hostaddress then
		script_execute = string.gsub(script_execute, "USERNAME", tostring(username))
		script_execute = string.gsub(script_execute, "PASSWORD", tostring(password))
		script_execute = string.gsub(script_execute, "HOSTADDRESS", tostring(hostaddress))
		print(script_execute)
		return true
	end
	return false
end

function put_file( target_file,source_file )
	if target_file and source_file then
		put_script_ori = string.gsub(put_script_ori,"TARGET_FILE",tostring(target_file))
		put_script_ori = string.gsub(put_script_ori,"SOURCE_FILE",tostring(source_file))
	end
end

function ls_file( target_file,source_file )
	if target_file then
		ls_script = string.gsub(ls_script,"TARGET_FILE",tostring(target_file))
	end
end

function scriptconnect( mode )
	--获取当前文件夹
	-- folder = lfs.currentdir()
	connect(username,password,hostaddress)
	if mode=='put' then
		put_file(target_file,source_file)
		script_execute = script_execute..put_script_ori
	elseif mode=='ls' then
		ls_file(target_file)
		script_execute = script_execute..ls_script
	end
	savefile(script_execute,mode)
end

function savefile(script,mode)
	if mode=='put' then
		path = lfs.currentdir().."\\"..script_put_path
	elseif mode=='ls' then
		path = lfs.currentdir().."\\"..script_get_path
	end
	-- print(path)
	local f = io.open(path,"w+")
	if f then
		f:write(script)
		f:close()
	end
end

--WinSCP\\WinSCP.com /console /script=WinSCP\\winscp_get > WinSCP\\tmp.log
function execute( mode )
	scriptconnect(mode)
	-- savefile(script_execute,mode)
	if mode=='put' then
		cmd = executor.." /console /script="..script_put_path
	elseif mode=='ls' then
		cmd = executor.." /console /script="..script_get_path
	end
	-- cmd = executor.." /console /script="..script_put_path
	-- os.execute(cmd)
	f = io.popen(cmd)
	return f
end

function match_version(  )
	f = execute('ls')
	max_version = "0.0.0"
	-- f = io.popen("ls "..local_dir)
	if f then
		for line in f:lines() do
			str = string.match(line,"RLHost_X798_Flex_(%d+\.%d+\.%d+)")
			if str then
				if str>max_version then
					max_version = str
				end
			end
		end
		f:close()
	end
	return max_version
end

-- scriptconnect('get')
execute('put')
-- print(match_version())