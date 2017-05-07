import socket
import subprocess
import shlex
import os
import re

def fetch_std_out(cmd):
    cmd1,cmd2=cmd.split('|')
    proc1 = subprocess.Popen(shlex.split(cmd1), stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(shlex.split(cmd2), stdin=proc1.stdout,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    proc1.stdout.close()  # Allow proc1 to receive a SIGPIPE if proc2 exits.
    out, err = proc2.communicate()
    # print('out: {0}'.format(out))
    # print('err: {0}'.format(err))
    return out
import pprint
def get_pid(strs,shield=()):
    strs=strs.split("\n")
    pprint.pprint(strs)
    pids=[int(re.findall("xlwang\s+(\d+)\s+",str)[0])
           for str in strs
           if len(re.findall("xlwang\s+(\d+)\s+",str) )>0 and "python" in str]
    pids=set(pids)-set(shield)
    pids=list(pids)
    return sorted(pids)

out_str=fetch_std_out("ps aux | grep test.py")

out_pids=get_pid(out_str ,[os.getpid()])
print out_pids

for pid in out_pids:
    cmd="kill -9 "+str(pid)
    subprocess.call(cmd.split(" "))


HOST = '10.214.211.205'
PORT = 8888
s = socket.socket(socket.AF_INET,              
                       socket.SOCK_STREAM)
s.settimeout(None)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
import  time
time.sleep(1)
s.bind((HOST,PORT))
s.listen(5)

i=1
while True:#i<10:
    i+=1

exit(-1)

