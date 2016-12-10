// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready( function() {

	$("div[id*='rbg']").each( function() {

		var o_t;
		if ( $(this).attr("id")[ 0 ] == 'q' ) {
			o_t = "question";
		} else {
			o_t = "answer";
		}

		var o_i = $(this).attr( "id" ).substr(4);
		var flag = false;

		$.ajax({

			url: "/votes/",
			type: "GET",
			data : { object_type: o_t, object_id: o_i },

			success: function( json ) {

				if ( json[ "error" ] != "200" ) {
					
					$("#" + o_t[0] + "rbg" + o_i).hide();
				}
			}
		});
	});

	$(".ask-ratingButton").on( 'click', function() {

		var v_t;
		if ( $(this).hasClass( "ask-ratingUpButton" ) ) {
			v_t = "like";
		} else {
			v_t = "dislike";
		}

		var o_t;
		if ( $(this).parents(".ask-questionRatingButtonsGroup").length == 1 ) {
			o_t = "question";
		} else {
			o_t = "answer";
		}

		var o_i = $(this).parent().attr('id').substr(4);

		$.ajax({

			url: "/votes/",
			type : "POST",
			data : { object_type: o_t, object_id : o_i, vote_type : v_t },

			success: function( json ) {

				if ( json[ "error" ] == "200" ) {
					var new_rating = json[ "new_rating" ];
					$("#" + o_t[0] + "rf" + o_i).html( new_rating );
					$("#" + o_t[0] + "rbg" + o_i).hide();

				} else {

					console.log( json[ "error" ] );
				}
			}
		});
	});

	$(".ask-answerBottomLine").each( function() {

		var q_i = $(".ask-bigQuestion").attr('id').substr(8);
		var a_i = $(this).attr( "id" ).substr(3);

		$.ajax({

			url: "/correct/",
			type: "GET",
			data : { question_id: q_i },

			success: function( json ) {

				if ( json[ "error" ] != "200" ) {
					
					$("#abl" + a_i).hide();
					console.log( json[ 'error' ] );
				}
			}
		});
	});

	$("[id^='cacb']").click( function() {

		var q_i = $(".ask-bigQuestion").attr('id').substr(8);
		var a_i = $(this).attr( "id" ).substr(4);

		$.ajax({

			url: "/correct/",
			type: "POST",
			data : { question_id: q_i, answer_id: a_i },

			success: function( json ) {

				console.log( json[ 'error '] );
			}
		});
	});
});



