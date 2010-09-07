#!/usr/bin/python
import socket,os

def page():
	c="""
<html>
	<head>
	<title>Muzzak! 0.1a</title>
	<style>
	body{
		background-color: #000000;
		color: #FFFFFF;
	}
	.round{
		-moz-border-radius: 15px;
		border-radius: 15px;
	}
	.player{
		width: 500px;
		margin: auto;
		background-color: #A2A2A2;
		padding: 10px;
		text-align: center;
	}
	.details{
		background-color: #525252;
		padding: 3px;
		font-family: Arial;
		font-weight: bolder;
	}
	.foot{
		background-color: #525252;
		padding: 3px;
		font-family: Arial;
		font-size: 0.7em;
	}
	a:link { 
		font-weight: bolder;
		color: #00FF00;
		background-color: #525252;
		text-decoration: none;
	}
	a:visited { 
		font-weight: bolder;
		text-decoration: none;
		color: #00FF00;
		background-color: #525252;
	}
	a:hover { 
		font-weight: bolder;
		text-decoration: none;
		color: #00FF00;
		background-color: #929292;
	}
	a:active { 
		font-weight: bolder;
		text-decoration: none;
		color: #00FF00;
		background-color: #929292;
	}
	</style>
	</head>
	<body>
		<div class='player round'>
			<div class='details round'>
				"%s" - %s <br/> %s
			</div>
			<br/>
			<div class='details'>
			<a href='PREV'>[Prev]</a>&nbsp;
			<a href='STOP'>[Stop]</a>&nbsp;
			<a href='PLAY'>[Play]</a>&nbsp;
			<a href='PAUSE'>[Pause]</a>&nbsp;
			<a href='NEXT'>[Next]</a>&nbsp;
			<a href='/'>[Check]</a>
			</div>
			<br/>
			<div class='details'>
			%s/%s @ %skbps. This is track %s of %s.
			</div>
			<br/>
			<div class='foot round'>
			python DCOP control for amarok by wolfmankurd
			</div>
		</div>
	</body>
</html>
"""
	return c
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port=4444
while 1:
	try:
		sock.bind(('',port))
		print "Bound to port %s"%port
		break
	except socket.error:
		port+=1
sock.listen(1)
while 1:
	try:
		conn, add = sock.accept()
		buff = conn.recv(128)
		get = buff.split()[1]
		print add[0],"sent",get[1:]
		cmd=get[1:]
		if(cmd=='PREV'):
			os.system("dcop amarok player prev")
		elif(cmd=='NEXT'):
			os.system("dcop amarok player next")
		elif(cmd=='PLAY'):
			os.system("dcop amarok player play")
		elif(cmd=='PAUSE'):
			os.system("dcop amarok player pause")
		elif(cmd=='STOP'):
			os.system("dcop amarok player stop")
		elif(cmd==''):
			pass
		else:
			print "Unknown command."
		player=page()
		artist = os.popen("dcop amarok player artist").read()
		title = os.popen("dcop amarok player title").read()
		album = os.popen("dcop amarok player album").read()
		pi = os.popen("dcop amarok playlist getActiveIndex").read()
		p = os.popen("dcop amarok playlist getTotalTrackCount").read()
		len = os.popen("dcop amarok player totalTime").read()
		now = os.popen("dcop amarok player currentTime").read()
		lens = int(os.popen("dcop amarok player trackTotalTime").read())
		nows = int(os.popen("dcop amarok player trackCurrentTime").read())
		per = 400*nows/lens
		print per
		bit = os.popen("dcop amarok player bitrate").read()
		conn.send(player%(title,album,artist,now,len,bit,pi,p))
		conn.close()
	except socket.error:
		pass
