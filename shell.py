"""
Authors: Ishi and Coco
Date: 03/17/21


Hi Mr. Redmond,
We want to give you a heads up that our shell is not fully completed. We ran into some issues at the end that
we could not overcome despite extensive research and many variations of our code in an attempt to get the
shell to run as we wanted it to. There are some shell commands that are not currently able to run (or we didn't have
time to write them), and for these we have tried our best to show our thinking/attempts in our code below.
I think what ultimately prevented us from being able to get more done was just a lack of knowledge of shells and
their systems because we really did try to make it work.

Best,
Coco and Ishi

"""



import os
import subprocess
import signal
import glob


def execute_commands(command):
    try:
    	if "(" and ")" in command:
        	index1 = command.find("(")
        	index2 = command.find(")")

        	sub_command = command[index1 + 1:index2]
        	
			# run subcommand then get that output and put back in first command
        	r, w = os.pipe()

        	# pipe result of sub_command to the pipe (I know this code doesn't work but this is the general idea of what we were going for)
        	r = subprocess.run(subprocess.run(sub_command.split(" ")) | w)
        	
        	# replace sub_command with pipe address
        	command[index1:index2 + 1] = r

        	# run OG command connected to the pipe
        	subprocess.run(command.split(" "))  
    	# piping
    	elif "|" in command:
        	s_in, s_out = (0, 0)
        	s_in = os.dup(0)
        	s_out = os.dup(1)

        	# first command takes commandut from stdin
        	fdin = os.dup(s_in)

        	for cmd in command.split("|"):
        		# fdin will be stdin if it's the first iteration
        		os.dup2(fdin, 0)
        		os.close(fdin)

				# restore stdout if this is the last command
        		if cmd == command.split("|")[-1]:
        			fdout = os.dup(s_out)
        		else:
        			fdin, fdout = os.pipe()

        		# redirect to pipe
        		os.dup2(fdout, 1)
        		os.close(fdout)

        		try:
        			subprocess.run(cmd.strip().split())
        		except Exception:
        			print("command not found: {}".format(cmd.strip()))

        	# restore
        	os.dup2(s_in, 0)
        	os.dup2(s_out, 1)
        	os.close(s_in)
        	os.close(s_out)


    	elif ">" in command:
        	split_command = command.split(" > ")
        	cmd = split_command[0] # this is the command
        	file_redirect = split_command[1] # the file redirect
        	try:
        		with open(file_redirect, "w") as f:
        			subprocess.run(cmd.split(" "), stdout = f)
        			f.close()

        	except Exception:
        		print("command not found: {}".format(cmd.strip()))

    	elif "<" in command:
        	split_command = command.split(" < ")
        	cmd = split_command[0] # this is the command
        	input_file = split_command[1] # the file where you should get the input
        	try:
        		with open(input_file, "r") as f:
        			#input_lines = f.readlines()
        			subprocess.run(cmd.split(" "), stdin = f)
        			f.close()
        	except Exception:
        		print("command not found: {}".format(cmd.strip()))	
    	
    	else:
    		subprocess.run(command.split(" "))
		

    except Exception:
    	print("command not found: {}".format(command))

def help():
	print("figure it out yourself")

def cd(path):
	try:
		os.chdir(os.path.abspath(path))
	except Exception:
		print("cd: no such file or directory: {}".format(path))

def pwd():
	print(os.fspath(path))

def bg():
	try:
		cmd = command.split(" ") + "&"
		subprocess.run(cmd)
	except:
		print("nope")

def jobs():
	pass

def control_c():
    pid = os.getpgrp()
    os.kill(pid, signal.CTRL_C_EVENTS) 

def control_z():
    pid = os.getpgrp()
    os.kill(pid, signal.SIGSTOP) 

def print_method(input_string):
    if "\"" in input_string:
    	split_input = input_string.split("\\")
    	new_string = "".join(split_input)
    	print(new_string)
    else:
    	print(input_string)


def main():
	while True:
		user_command = input("$ ")
		if user_command == "exit":
			break
		elif "*" in user_command:
			glob.glob(user_command) # not sure about this code
		elif user_command[:3] == "cd ":
			cd(user_command[3:])
		elif user_command == "bg":
			bg(user_command[3:])
		elif user_command == "help":
			help()
		elif user_command == "pwd":
			pwd()
		elif user_command[:6] == "print(":
			print_method(user_command[6:-1])
		else:
			execute_commands(user_command)



if __name__ == "__main__":
    main()
