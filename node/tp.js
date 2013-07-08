var sys = require("sys"),  
url = require("url"),
amp = new Amplifier(),
netRequest = require("request"),
my_http = require("http");  

var AMP_URL = "http://192.168.1.7:8241/";

my_http.createServer(function(request,response){
    response.writeHeader(200, {"Content-Type": "text/plain"});
    if(request.url != "/favicon.ico") {
     sys.puts("request: " + request.url);
     processText(decodeGet(request));
    }
    response.end();
}).listen(8080);
sys.puts("Server Running on 8080");

function decodeGet(request) {
 var url_parts = url.parse(request.url, true);
 var query = url_parts.query;
 //sys.puts(query.q);
 return query.q;
}

function processText(text) {
 if(text == "")
  return;

 sys.puts("Received text: " + text);

 // Match exact phrase ?

 // Match 1st word to route command

 // First split text into an array
 var tArray = text.toLowerCase().split(" ");

 // Send all commands to the amp
 amp.command(text, tArray);

 // Match the 1st word?
/*
 switch(tArray[0]) {
  case "volume":
  case "mute":
  case "turn":
    amp.command(text, tArray);
    break;
  default:
    // Match two words?
    switch(tArray[0] + " " + tArray[1]) {
     case "everything off":
      sys.puts("Everything off command");
      break;
     default:
      sys.puts("Command not recognised!");
   }  
 } 
 */
}

// Amplifier Class
function Amplifier() {
}
Amplifier.prototype.command = function (cmd, cmdSplit) {
 sys.puts("Amplifier command");
 switch(cmd) {
 case "volume of":
 case "volume off":
 case "volume mute":
 case "mute":
 case "mute audio":
 case "mute sound":
  sys.puts("mute!");
  this.sendHttpCmd("set/muteOn");
  break;
 case "volume down":
 case "turn down":
 case "turn it down":
 case "turn it down now":
 case "keep it down":
  sys.puts("volume down");
  this.volumeDown();
  break;
 case "volume up":
 case "turn up":
 case "turn it up":
 case "turn it up now":
  sys.puts("volume up");
  this.volumeUp();
  break;
 case "play music":
 case "play mp3":
 case "select music":
 case "select mp3":
 case "switch to mp3":
 case "switch to music":
  this.sendHttpCmd("set/selectMp3");
  break;
 case "play tv":
 case "play television":
 case "play media":
 case "select tv":
 case "select television":
 case "select media":
 case "switch to tv":
 case "switch to media":
 case "switch to television":
  this.sendHttpCmd("set/selectMedia");
  break;
 default:
  sys.puts("not recognised!");
 }
}
Amplifier.prototype.sendHttpCmd = function(cmd) {
 netRequest(AMP_URL + cmd, function(error, response, body) {
  sys.puts(body);
 });
}
Amplifier.prototype.volumeUp = function() {
 // Get current volume level
 netRequest(AMP_URL + "get/all", function(error, response, body) {
  //sys.puts("json response: " + body);
  var res = JSON.parse(body);
  
  // Increase by 15
  var vol = res.volume + 13
  netRequest(AMP_URL + "set/volume/" + vol);
  netRequest(AMP_URL + "set/muteOff");
 });
}
Amplifier.prototype.volumeDown = function() {
 // Get current volume level
 netRequest(AMP_URL + "get/all", function(error, response, body) {
  //sys.puts("json response: " + body);
  var res = JSON.parse(body);
  
  // Decrease by 15
  var vol = parseInt(res.volume) - parseInt(13);
  netRequest(AMP_URL + "set/volume/" + vol);
  netRequest(AMP_URL + "set/muteOff");
 });
}
