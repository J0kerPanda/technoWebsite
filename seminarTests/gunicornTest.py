def application( env, start_response ):
	start_response('200_OK', [('Content-Type', 'text/plain')])
	return ['Hello, world!']
