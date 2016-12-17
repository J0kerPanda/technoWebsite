function getAnswersIDs() {

	var ids = [];

	$("div[id^='answer']").each( function() {

		id = $(this).attr("id").substr( 'answer'.length );
		ids.push( id )
	});

	return ids;
}

function getComet_Answers() {

	$.ajax( {

		url: '/get-answers/', 
		type: 'GET',
		data: { cid: 5 },

		success: function( response ) {

			console.log( 'success ');
			console.log( response );
			getComet_Answers()
		},

		error: function() {

			console.log( 'failure' );
			setTimeout( getComet_Answers, 5000 );
		},
	});
}

$(document).ready( getComet_Answers() );