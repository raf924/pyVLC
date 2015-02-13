/*interface.restoreChanged.connect(function (restore) {
	$(document).trigger("invlc.window.restoreChanged",restore);
	console.log("restore changed");
});
interface.lengthChanged.connect(function (length) {
	$(document).trigger("invlc.player.lengthChanged",length);
});
interface.timeChanged.connect(function (time) {
	$(document).trigger("invlc.player.timeChanged",time);
});
interface.metaDataChanged.connect(function () {
	$(document).trigger("invlc.media.metaDataChanged");
});
interface.play.connect(function (id) {
	$(document).trigger("invlc.player.play",id);
});
interface.next.connect(function () {
	$(document).trigger("invlc.player.next");
});
interface.previous.connect(function () {
	$(document).trigger("invlc.player.previous");
});
interface.paused.connect(function (isPaused) {
	console.log(isPaused);
	$(document).trigger("invlc.player.pause",isPaused);
});
interface.songListUpdated.connect(function (songList) {
	console.log("songListUpdated");
	var sl = new Array(songList.length);
	sl = {"songList":songList};
	$(document).trigger("invlc.view.songListUpdated",sl);
});
*/
interface.libraryUpdated.connect(function(){
	$(document).trigger("libraryUpdated.invlc.library");
});
interface.expanded.connect(function(){
    $(document).trigger("expanded.invlc.window");
});
interface.restored.connect(function(){
    $(document).trigger("restored.invlc.window");
});
interface.events.connect(function () {
	var eventName = arguments[0];
	var args = Array.prototype.slice.call(arguments,1);
	$(document).trigger(eventName,args);
});


var invlc = {};

invlc.tags = interface.tags;

invlc.nowPlaying = interface.nowPlaying;

invlc.library = interface.library;

invlc.play = interface.play;
invlc.next = interface.next;
invlc.previous = interface.previous;
invlc.close = interface.close;

invlc = interface;

invlc.NOTHINGSPECIAL = 0
invlc.OPENING = 1;
invlc.BUFFERING = 2;
invlc.PLAYING = 3;
invlc.PAUSED = 4;
invlc.STOPPED = 5;
invlc.ENDED = 6
invlc.ERROR = 7;

invlc.action = function (action, data) {
	interface.action({action: action, data: data});
};

invlc.timeToString = function (value) {
	var d = new Date(value);
	var str = d.getHours()-1>0?(d.getHours()-1<10?"0":"")+d.getHours()-1+":":"";
	str += (d.getMinutes()<10?"0":"")+d.getMinutes()+":";
	str += (d.getSeconds()<10?"0":"")+d.getSeconds();
	return str;
};
