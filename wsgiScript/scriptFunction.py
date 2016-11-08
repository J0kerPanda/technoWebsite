#!/usr/bin/python

from wsgiref.simple_server import make_server
from cgi import parse_qs

def application( env, start_response ):

	data = "This is brand new hello world!\n"

	queryString = parse_qs( env['QUERY_STRING'] )

	for key in queryString.keys():
		data += ( str( key ) + ": " + str( queryString.get( key ) ) + '\n' )

	for key in env.keys():
		if ( key[:5] == 'HTTP_' ):
			data += ( str( key )[5:] + ": " + str( env.get( key ) ) + '\n' )

		if ( key.upper() == 'CONTENT_LENGTH' ) or ( key.upper() == 'CONTENT_TYPE' ):
			data += ( str( key ) + ": " + str( env.get( key ) ) + '\n' )
			
	status = "200 OK"
	content_headers = [

		('Content-type', 'text/plain'),
		('Content-length', str( len(data) ) )
	]
	start_response( status, content_headers )
	return iter( [data] )

if __name__ == "__main__":

	server = make_server(
		'localhost',
		8081,
		application
	)

	server.handle_request()

