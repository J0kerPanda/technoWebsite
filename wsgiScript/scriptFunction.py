def application( env, start_response ):

	data = "This is brand new hello world!\n"

	for key in env.keys():
		if ( key[:5] == 'HTTP_' ):
			data += ( str( key )[5:] + ": " + str( env.get( key ) ) + '\n' )

		if ( key.upper() == 'CONTENT_LENGTH' ):
			data += ( str( key ) + ": " + str( env.get( key ) ) + '\n' )

	status = "200_OK"
	content_headers = [

		('Content-type', 'text/plain'),
		('Content-length', str( len(data) ) )
	]
	start_response( status, content_headers )
	return iter( [data] )
