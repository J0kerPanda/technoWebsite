function getAnswersIDs() {

	var ids = [];

	$("div[id^='answer']").each( function() {

		id = $(this).attr("id").substr( 'answer'.length );
		ids.push( id )
	});

	return ids;
}

function handleNewAnswer() {

	var q_i = $(".ask-bigQuestion").attr( "id" ).substr( "question".length );
	var a_i = $(".ask-answerBottomLine").last().attr( "id" ).substr( "abl".length );
	hideRatingButtons( "answer", a_i );
	hideCorrectCheckbox( q_i, a_i );
}

function getCometAnswers() {

	$.ajax( {

		url: "/get-answers/", 
		type: "GET",
		data: { cid: 5 },

		success: function( json ) {

			var newAnswer = document.createElement( "div" );
			newAnswer.innerHTML = json[ "answer" ];
			$( ".ask-answer" ).last().after( newAnswer );
			handleNewAnswer();

			getCometAnswers();
		},

		error: function() {

			setTimeout( getCometAnswers, 5000 );
		},
	});
}

$(document).ready( getCometAnswers() );