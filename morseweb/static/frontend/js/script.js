/* Author:

*/

$('#SCReceiveModal').modal();
$('#SCReceiveModal').modal('hide');
$('#SCSendModal').modal();



function getCookie(c_name)
{
var i,x,y,ARRcookies=document.cookie.split(";");
for (i=0;i<ARRcookies.length;i++)
  {
  x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
  y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
  x=x.replace(/^\s+|\s+$/g,"");
  if (x==c_name)
    {
    return unescape(y);
    }
  }
}

if (self.document.location.hash.substr(0,13)=="#access_token") {
	$("#hiddentoken").val(self.document.location.hash.split("&")[0].split("=")[1]);
	$("#formtext").val(getCookie("text"));
	document.cookie="token="+escape(self.document.location.hash.split("&")[0].split("=")[1]);
}else{
	$('#SCSendModal').modal('hide');
}

var audio = new Audio();

$(document).ready(function(){

	$('#sendnormaltext').val(getCookie("text"))

	// button bindings
	$('#playbtn').bind("click", function (){
		audio.setAttribute("src","http://www.morsecloud.com/api/encode.wave?text="+escape($('#sendnormaltext').val()));
		audio.play();
	});
	$('#micbtn').bind("click", function (){
		activateMic();
	});

	// instant encoding/decoding textareas
	$('#sendnormaltext').bind("propertychange keyup input paste",function() {
		document.cookie="text="+escape($('#sendnormaltext').val());
		$("#sendmorsetext").val(DoMorseEncrypt($('#sendnormaltext').val()));
		$("#downloadbtn").attr({href:"http://www.morsecloud.com/api/encode.wave?text="+escape($('#sendnormaltext').val())});
	});
	$('#receivemorsetext').bind("propertychange keyup input paste",function() {
		$("#receivenormaltext").val(DoMorseDecrypt($('#receivemorsetext').val()));
	});
	$('#myinbox').bind("click", function(){
		ajaxresponse = $.ajax({
			//-- --- .-. ... .
		url: "https://api.soundcloud.com/me/activities/tracks/exclusive.json?tags=morsecloud&oauth_token="+escape(getCookie("token"))+"&filter=downloadable&consumer_key=1548641e2e37a7ae5f432f22118497e9",
		dataType: 'json',
		success: function(){
			$('#publictab').removeClass('active');
			$('#privatetab').addClass('active');
			ajaxresponse = jQuery.parseJSON(ajaxresponse.responseText);
			$("#scmorsetable").empty();
			jQuery.each(ajaxresponse.collection, function (){
				$('#scmorsetable').append('<tr onclick="loadSoundCloudTrack(\''+this.origin.track.id+'&oauth_token='+getCookie('token')+'\');"><td>'+this.origin.track.user.username+'</td><td>'+this.origin.track.title+'</td></a></tr>');
			})},
		error: function(){
			alert("fail!");
			$('#SCReceiveModal').modal('hide');	
		}
		});


	});

	$('#SCReceiveModal').on('show', function () {
		ajaxresponse = $.ajax({
			//-- --- .-. ... .
		url: "https://api.soundcloud.com/tracks.json?tags="+escape("morsecloud")+"&filter=downloadable&consumer_key=1548641e2e37a7ae5f432f22118497e9",
		dataType: 'json',
		success: function(){
			ajaxresponse = jQuery.parseJSON(ajaxresponse.responseText);
			$("#scmorsetable").empty();
			jQuery.each(ajaxresponse, function (){
				$("#scmorsetable").append('<tr onclick="loadSoundCloudTrack("'+this.id+'");"><td>'+this.user.username+'</td><td>'+this.title+'</td></a></tr>');
			})},
		error: function(){
			alert("fail!");
			$('#SCReceiveModal').modal('hide');	
		}
		});
	});

	

	$("#sendnormaltext").keyup();

})

function loadSoundCloudTrack(trackid){
	ajaxresp = $.ajax({url:"http://www.morsecloud.com/api/decode",data:"track_id="+trackid,success: function(){
		$('#SCReceiveModal').modal('hide');	
		$('#receivemorsetext').val(jQuery.parseJSON(ajaxresp.responseText).response.message);
		$('#receivenormaltext').val(DoMorseDecrypt(jQuery.parseJSON(ajaxresp.responseText).response.message));
	},
		error: function(){
			alert("error");
		}
	}
);
}

function activateMic(){
	$("#uploadbtns").append("<a class=\"btn btn-danger\" id=\"recindicator\" style=\"display:none\">REC...</a>");
	$("#recindicator").fadeIn();
	$("#micbtn").addClass("btn-danger");
	$('#micbtn, #recindicator').bind("click", function (){
		$('#micbtn').unbind();
		$("#recindicator").fadeOut();
		$("#recindicator").detach();
		$("#micbtn").removeClass("btn-danger");	
		$('#micbtn').bind("click", function (){
			activateMic();
		});
	});
}

// Morseinput

var MCarr=new Array(
"*","|",".-","-...","-.-.","-..",".","..-.","--.","....","..",".---","-.-",".-..","--","-.","---",
".--.","--.-",".-.","...","-","..-","...-",".--","-..-","-.--","--..","-----",".----","..---","...--","....-",
".....","-....","--...","---..","----."
);
var ABC012arr="*|ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

function DoMorseDecrypt(x)
{mess="";apos=0;bpos=0;
while(bpos<x.length)
{
 bpos=x.indexOf(" ",apos);if(bpos<0){bpos=x.length};
 dits=x.substring(apos,bpos);apos=bpos+1;let="";
 for(j=0;j<MCarr.length;j++){  if(dits==MCarr[j]){let=ABC012arr.charAt(j)}  };
 if(let==""){let="*"};
 mess+=let;
};
return mess;
};

function DoMorseEncrypt(x)
{mess="";
for(i=0;i<x.length;i++)
{
let=x.charAt(i).toUpperCase();
for(j=0;j<MCarr.length;j++){  if(let==ABC012arr.charAt(j)){mess+=MCarr[j]}  };
mess+=" ";
};
mess=mess.substring(0,mess.length-1);
return mess;
};


