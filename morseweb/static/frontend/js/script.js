/* Author:

*/

$('#SCReceiveModal').modal({show:false});


$(document).ready(function(){

$('#sendnormaltext').bind("propertychange keyup input paste",function() {
  $("#sendmorsetext").val(DoMorseEncrypt($('#sendnormaltext').val()));
	$("#downloadbtn").attr({href:"http://www.morsecloud.com/api/encode.aiff?text="+escape($('#sendnormaltext').val())})
});

$('#receivemorsetext').bind("propertychange keyup input paste",function() {
  $("#receivenormaltext").val(DoMorseDecrypt($('#receivemorsetext').val()));
});

$('#SCReceiveModal').on('show', function () {
  ajaxresponse = $.ajax({
		//-- --- .-. ... .
  url: "https://api.soundcloud.com/tracks.json?tags="+escape("morse")+"&filter=downloadable&consumer_key=1548641e2e37a7ae5f432f22118497e9",
  dataType: 'json',
	success: function(){
		ajaxresponse = jQuery.parseJSON(ajaxresponse.responseText);
		jQuery.each(ajaxresponse, function (){
			$("#scmorsetable").append('<tr onclick="loadSoundCloudTrack('+this.id+');"><td>'+this.user.username+'</td><td>'+this.title+'</td></a></tr>');
		})},
	error: function(){
		alert("fail!");
		$('#SCReceiveModal').modal('hide');	
	}
	});
});
})

function loadSoundCloudTrack(trackid){
	$.ajax({url:"http://www.morsecloud.com/api/decode",data:"trackid="+trackid,success: function(){
		$('#SCReceiveModal').modal('hide');	
		$('#receivemorsetext').val(data.text);
		$('#receivenormaltext').val(DoMorseDecrypt(data.text));
	},
		error: function(){
			alert("error");
		}
	}
);
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


