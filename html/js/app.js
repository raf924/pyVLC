var idList = [];
var currentId;
var SEQUENTIAL = 1;
var SHUFFLE = 2;
var NOREPEAT = 4;
var REPEAT = 8;
var REPEATONE = 16;
var playback = SEQUENTIAL | NOREPEAT;
var seeking = false;
var tags = {};

$(function(){
	tags = {"Title":"","Duration":"Length","Artist":"","Album":""};
	$(document).on("expanded.invlc.window", changeIcon);
	$(document).on("restored.invlc.window", changeIcon);
	$(document).on("MediaPlayerLengthChanged.invlc.player",changeLength);
	$(document).on("MediaPlayerTimeChanged.invlc.player",changeTime);
	$(document).on("MediaPlayerPlaying.invlc.player",updateStatus);
	$(document).on("MediaPlayerPaused.invlc.player",updateStatus);
	$(document).on("MediaPlayerStopped.invlc.player",updateStatus);
	$(document).on("MediaPlayerEndReached.invlc.player",updateStatus);
	$(document).on("invlc.player.next",next);
	$(document).on("invlc.player.previous",previous);
	$(document).on("libraryUpdated.invlc.library",updateView);
	$(document).on("MediaPlayerMediaChanged.invlc.player",updateCurrentSong);
	updateView();
	$("#songList tbody").on('click',function(e) {
		$(".metadata").parent().removeClass("active");
		$(e.target).parent().addClass("active")
	}).on("dblclick",function (e) {
		currentId = $(e.target).parent().attr("id");
		invlc.play(currentId);
	});
	$(".playback-action#shuffle").click(function  () {
		if($(this).attr("state")=="on"){
			$(this).attr("state","off");
		}
		else{
			$(this).attr("state","on")
		}
	});
	$(".playback-action#repeat").click(function () {
		if($(this).attr("state")=="no"){
			$(this).attr("state","all");
		}
		else if($(this).attr("state")=="all"){
			$(this).attr("state","one");
		}
		else{
			$(this).attr("state","no");
		}
	});
	$(".playback-action").click(function () {
		if($("#shuffle").attr("state")=="on"){
			playback = SHUFFLE;
		}
		else if($("#shuffle").attr("state")=="off"){
			playback = SEQUENTIAL;
		}
		if ($("#repeat").attr("state")=="no") {
			playback = playback | NOREPEAT;
		}
		else if($("#repeat").attr("state")=="all"){
			playback = playback | REPEAT;
		}
		else  if($("#repeat").attr("state")=="one"){
			playback = playback | REPEATONE;
		}
	});
	var slider = $("#seeker").slider({
		id:"seeker-slider",
		tooltip:'hide',
		handle:"square",
		value:0,
		tooltip_separator:';',
		formatter : function (value) {
			return invlc.timeToString(value);
		}
	});
	slider.on("slideStart",function () {
		seeking = true;
	}).on("slideStop",function () {
		console.log(slider.slider("getValue"))
		invlc.action("seek",slider.slider("getValue"));
		seeking = false;
	});
	slider.slider("disable");
	$(".window-action").each(function (index, item) {
		$(item).click(function () {
			invlc.action($(this).data("action"));
		});
	});
	$(".player-action").each(function (index, item) {
		$(item).click(function () {
			invlc.action($(this).data("action"));
		});
	});
	$
	$.each(tags, function (index, item) {
		var text = index;
		if(item){
			text = item;
		}
		$("<th></th>").attr("id",index).html(text).appendTo("#tags");
		$("#tags").append($("<div></div>").addClass("resize").css("height",$("thead").css("height")));
	});
});

function changeLength (event, length) {
	$("#seeker").slider('setAttribute',"max",length);
	$("#total").html(invlc.timeToString(length));
}

function changeTime (event, time) {
	if(!seeking){
		$("#seeker").slider("setValue",time,false);
		$("#elapsed").html(invlc.timeToString(time));
	}
}

function changeIcon (event) {
	if(event.type=="restored"){
		$(".window-action#restore").css("display","none");
		$(".window-action#expand").css("display","");
	}
	else if(event.type=="expanded"){
		$(".window-action#restore").css("display","");
		$(".window-action#expand").css("display","none");
	}

}

function changeMetaData (event) {
	var metaData = invlc.nowPlaying();
	$(".info").each(function (index,item) {
		var key = $(this).attr("id");
		$(this).html(metaData[key]);
	});
}

function updateView () {
	console.log("updateView");
	songList = invlc.library;
	$(".song-item").remove();
	idList = [];
	$.each(songList,function (index, song) {
		idList.push(parseInt(song.Id));
		$("<tr></tr>").attr("path",song.Path).attr("id",song.Id).addClass("song-item").appendTo("#songList");
		$.each(tags, function (index, item) {
			var text = song[index];
			if(index=="Duration"){
				text = invlc.timeToString(song[index]);
			}
			$("<td></td>").addClass("metadata").html(text).appendTo("#"+song["Id"]);
			$("#"+song["Id"]).append("<div></div>").css("width","1px");
		});
	});
	idList.push(-1);
}

function updateCurrentSong (event, song) {
	$(".info").each(function (index,item) {
		var key = $(item).attr("id");
		$(item).html(song[key]);
	});
	if(id == song.Id){
		currentId = id;
		$(".song-item").removeClass("active");
		$(".song-item#"+id).addClass("active");
		if(playback&SEQUENTIAL&&playback&NOREPEAT){
			if(idList.indexOf(id)==idList.length-1){
				$("#next").attr("disabled","disabled");
			}
			else if(idList.indexOf(id)==0){
				$("#previous").attr("disabled","disabled");
			}
			else
			{
				$("#next").removeAttr("disabled");
				$("#previous").removeAttr("disabled");
			}
		}
		else if(playback&SEQUENTIAL&&playback&REPEAT){
			$("#next").removeAttr("disabled");
			$("#previous").removeAttr("disabled");
		}
		else if(playback&SHUFFLE){
			$("#next").removeAttr("disabled");
			$("#previous").removeAttr("disabled");
		}
		if(playback&REPEATONE){
			$("#next").attr("disabled","disabled");
			$("#previous").attr("disabled","disabled");
		}
	}
	else{
		$("#next").attr("disabled","disabled");
		$("#previous").attr("disabled","disabled");
	}
}

function updateStatus (event, status) {
	switch(status){
		case invlc.PLAYING:
		$(".player-action > .glyphicon-play").removeClass("glyphicon-play").addClass("glyphicon-pause").parent().removeAttr("disabled");
		$("#seeker").slider("enable");
		break;
		case invlc.PAUSED:
		$(".player-action > .glyphicon-pause").removeClass("glyphicon-pause").addClass("glyphicon-play").parent().removeAttr("disabled");
		break;
		case invlc.STOPPED:
		$(".player-action > .glyphicon-pause").removeClass("glyphicon-pause").addClass("glyphicon-play").parent().attr("disabled","disabled");
		$("#seeker").slider("disable");
		invlc.next();
		break;
	}
}

function next () {
	var id = currentId;
	if(playback&SEQUENTIAL&&playback&REPEAT){
		if(idList.indexOf(currentId)==idList.length-1){
			currentId = idList[0];
		}
		else{
			currentId = idList[idList.indexOf(currentId)+1];
		}
	}
	else if(playback&SHUFFLE){
		while(currentId==id)
			currentId = idList[Math.floor(Math.random()*idList.length)];
	}
	else if(playback&SEQUENTIAL&&playback&NOREPEAT){
		if(idList.indexOf(currentId)==idList.length-1){
			currentId = -1;
		}
		else{
			currentId = idList[idList.indexOf(currentId)+1];
		}
	}
	if(playback&REPEATONE){
		currentId = id;

	}
	console.log("Playback : ",playback,", PreviousID : ",id,", Current ID : ",currentId)
	invlc.play(currentId);
}

function previous () {
	if(idList.indexOf(currentId)==0){
		currentId = idList[idList.length-1]
	}
	else{
		currentId = idList[idList.indexOf(currentId)-1];
	}
	invlc.play(currentId);
}
