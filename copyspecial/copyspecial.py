import sys
import re
import os
import shutil
import commands

def get_special_paths(dname):
	result = []
	paths = os.listdir(dname)
	for i in paths:
		match = re.search(r'__(\w+)__',i)
		if match:
			result.append(os.path.abspath(os.path.join(dname, i)))
	return result

def copy_to(paths, to_dir):
	if not os.path.exists(to_dir):
		os.mkdir(to_dir)
	for path in paths:
		fname = os.path.basename(path)
		#print 'Fname: ', fname,'\n'
		shutil.copy(path, os.path.join(to_dir, fname))

def zip_to(paths, to_zip):
	cmd = 'zip -j ' + to_zip + ' ' + ' '.join(paths)
	print 'Command I Am going to do : '+cmd
	(status, output) = commands.getstatusoutput(cmd)
	if status:
		sys.stderr.write(output)
		sys.exit(1)

def main():
	arg = sys.argv[1:]
	if not arg:
		print 'Usage : [--todir dir][--tozip dir] dir [dir.....]';
		sys.exit(1)
	todir = ''
	#print 'Args[0] : ',arg[0],'\n'
	if arg[0] == '--todir':
		todir = arg[1]
		del arg[0:2]

	tozip = ''
	if arg[0] == '--tozip':
		tozip = arg[1]
		del arg[0:2]

	#print 'Todir : ', todir,'\n'
	#print arg,'\n'
	if len(arg) == 0:
		print 'Error : Must specify one or more Dirs'
		sys.exit(1)
	paths = []
	for dirname in arg:
		#print 'Dirname : ', dirname,'\n'
		paths.extend(get_special_paths(dirname))
	if todir:
		copy_to(paths, todir)
	elif tozip:
		zip_to(paths, tozip)
	else:
		print '\n'.join(paths)
	
if __name__ == "__main__":
	main()
#https://github.com/Nikhildevadas/google_python_solved/blob/master/copyspecial/copyspecial.py
