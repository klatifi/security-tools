Security Tools
==========

A set of tools I use for pentesting. For example the heartbleed-test checks for CVE-2014-0160. 

Usage:

```
$ heartbleed server.com -p 443

```
## Install

* Copy the files into directory  `/usr/bin/`  or `/usr/sbin/`
* Make sure are they executable 

```
sudo chmod +x SCRIPTNAME
```

* For some scripts you will need python2 to run, open your terminal and run 
```
$ which python2
```
* Use the output to replace python2 location at the very beginning of the script. 
For example: heartbleed-test:

```
#!/usr/local/bin/python2
```
