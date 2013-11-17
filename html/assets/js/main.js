$( document ).ready(function() {

    amplifier={
      audio: {
        power: true,
        mute: false,
        volume: 0,
        bass: 0,
        treble: 0,
        state: 0,
        states: ["media", "mp3", "radio", "aux"],
        tones: [-14, -12, -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10, 12, 14],
        update: function(json) {
          this.power = json.power;
          this.mute = json.mute;
          this.volume = json.volume;
          this.mute = json.mute;
          this.bass = json.bass;
          this.treble = json.treble;
          this.state = json.state;
        },
        toneToPercent: function(tone) {
          var coeff = parseFloat(1 / 0.28); // graduations
          var tone = tone + 14; // offset
          var value = parseFloat(tone) * parseFloat(coeff)
          return parseInt(Math.ceil(value));
        },
        percentToTone: function(percent) {
          var index = parseInt(Math.floor(parseFloat(percent) * 0.14));
          return amplifier.audio.tones[index];
        }
      },
      setState: function (state) {
        this.state = state;
      },
      updateGui: function (state) {
        //console.log(amplifier);
        amplifier.updateNav(state);
        amplifier.updatePanel(state);
        amplifier.updateSliders(state);
        amplifier.showPanel(state);
      },
      updateNav: function(state) {
        //console.log(state);
        switch(state) {
          case "media":
            $("#btn-media").css('background-image', 'url(/assets/images/menu-tv-press.png)');
            $("#btn-menu").css('background-image', 'url(/assets/images/menu.png)');
            $("#btn-mp3").css('background-image', 'url(/assets/images/menu-mp3.png)');
            $("#btn-radio").css('background-image', 'url(/assets/images/menu-radio.png)'); 
            break;
          case "mp3":
            $("#btn-mp3").css('background-image', 'url(/assets/images/menu-mp3-press.png)');
            $("#btn-menu").css('background-image', 'url(/assets/images/menu.png)');
            $("#btn-media").css('background-image', 'url(/assets/images/menu-tv.png)');
            $("#btn-radio").css('background-image', 'url(/assets/images/menu-radio.png)');  
            break;
          case "radio":
            $("#btn-radio").css('background-image', 'url(/assets/images/menu-radio-press.png)');
            $("#btn-menu").css('background-image', 'url(/assets/images/menu.png)');
            $("#btn-media").css('background-image', 'url(/assets/images/menu-tv.png)');
            $("#btn-mp3").css('background-image', 'url(/assets/images/menu-mp3.png)');
            break;
          case "aux":
            $("#btn-aux").css("background: url('/assets/images/menu-press.png') no-repeat center");
            $("#btn-radio").css('background-image', 'url(/assets/images/menu-radio.png)');       
            $("#btn-media").css('background-image', 'url(/assets/images/menu-tv.png)');
            $("#btn-mp3").css('background-image', 'url(/assets/images/menu-mp3.png)');
            break;
        }
      },
      updatePanel: function(state) {
        //console.log(state);
        switch(state) {
          case "media":
            amplifier.media.updatePanel();       
            break;
          case "mp3":
            amplifier.mp3.updatePanel();  
            break;
          case "radio":
            amplifier.radio.updatePanel();
            break;
          case "aux":
            amplifier.aux.updatePanel();
            break;
          // case "off":
          //   amplifier.updatePanel("off");
        }
      },
      showPanel: function(state) {
        //console.log(state);
        switch(state) {
          case "media":
            $("#panel-tv").show();
            $("#panel-mp3").hide();
            $("#panel-menu").hide();
            $("#panel-radio").hide();            
            break;
          case "mp3":
            $("#panel-tv").hide();
            $("#panel-mp3").show();
            $("#panel-menu").hide();
            $("#panel-radio").hide();   
            break;
          case "radio":
            $("#panel-tv").hide();
            $("#panel-mp3").hide();
            $("#panel-menu").hide();
            $("#panel-radio").show();
            break;
          case "aux":
            $("#panel-tv").hide();
            $("#panel-mp3").hide();
            $("#panel-menu").show();
            $("#panel-radio").hide();
            break;
        }
      },
      updateSliders: function(state) {
        //console.log(select);
        switch(state) {
          case "media":
            var a = "#12aab2";
            var b = "#0bb";
            var c = "#055";
            break;
          case "mp3":
            var a = "#24ed24";
            var b = "#0b0";
            var c = "#050";
            break;
          case "radio":
            var a = "#d1ef22";
            var b = "#bb0";    
            var c = "#550";
            break;
          case "aux":
            var a = "#efefef";
            var b = "#bbb";    
            var c = "#555";
            break;
        }
        // Update slider background colours
        $("#vol-slider").css('background', a);
        $("#vol-slider a").css('border', '4px solid ' + b).css('background-color', c);
        $("#vol-slider").slider("value", this.audio.volume);        
        $("#bass-slider").css('background', a);
        $("#bass-slider a").css('border', '4px solid ' + b).css('background-color', c);
        $("#bass-slider").slider("value", this.audio.toneToPercent(this.audio.bass));
        $("#treble-slider").css('background', a);
        $("#treble-slider a").css('border', '4px solid ' + b).css('background-color', c);
        $("#treble-slider").slider("value", this.audio.toneToPercent(this.audio.treble));
      },
      init: function() {
          // Get current state of amp...
          // Show spinner while network connection is established
          // websocket connection?
          $.getJSON(amplifier.network.url + "get/all", function(json) {
            
            // Set button handlers
            amplifier.setupButtonHandlers();

            // Update State From Device
            amplifier.updateStateFromDevice(json);

            // Update the GUI
            amplifier.updateGui(json.state);

            // Start device refresh
            amplifier.network.init();
            amplifier.network.start();

          }).done(function(json) {
              //alert("success");
          }).fail(function(json) {
              amplifier.showNetworkFailed();
          }).always(function(json) {
              //alert("complete");
          });
      },
      updateStateFromDevice: function(json) {
          //console.log("current state of amp"); console.log(json); console.log(amplifier);
          // Aux
          amplifier.aux.update(json);
          // Audio
          amplifier.audio.update(json);
          // Radio
          amplifier.radio.station = json.radio.station;
          // Mp3
          amplifier.mp3.update(json);
      },
      setupButtonHandlers: function() {
        // Top Nav Button Handlers
        $("#btn-media").click(function(){ amplifier.selectMedia(); });
        $("#btn-mp3").click(function(){ amplifier.selectMp3(); });
        $("#btn-radio").click(function(){ amplifier.selectRadio(); });
        $("#btn-aux").click(function(){ amplifier.selectAux(); });

        // Main Control Sliders
        $("#vol-slider").slider({
          change: function(event, ui) {
            if(event.originalEvent) {
              amplifier.network.stop();
              $.get(amplifier.network.url + "set/volume/" + ui.value, function(amp) {
                amplifier.audio.volume = amp.volume                
                amplifier.network.start();
              }); 
            } else {
             // console.log("PGM Change - do not call network");
            }
          } 
        });
        $("#bass-slider").slider({ 
          change: function(event, ui) {         
            if(event.originalEvent) {
              amplifier.network.stop();
              $.get(amplifier.network.url + "set/bass/" + amplifier.audio.percentToTone(ui.value), function(amp) {
                amplifier.bass = amp.bass //amplifier.audio.toneToPercent(amp.bass)             
                amplifier.network.start();
              }); 
            } else {
              //console.log("PGM Change - do not call network");
            }
          }
        });
        $("#treble-slider").slider({ 
          change: function(event, ui) {
            if(event.originalEvent) {
              amplifier.network.stop();
              $.get(amplifier.network.url + "set/treble/" + amplifier.audio.percentToTone(ui.value), function(amp) {
                amplifier.treble = amp.treble //amplifier.audio.toneToPercent(amp.treble)            
                amplifier.network.start();
              }); 
            } else {
              //console.log("PGM Change - do not call network");
            }
          }
        });
        
        // Radio Control
        $("#radio-prev").click(function(){ amplifier.radio.prev(); });
        $("#radio-next").click(function(){ amplifier.radio.next(); });

        // MP3 Control
        $("#mp3-list").click(function(){ amplifier.mp3.list(); });
        $("#mp3-repeat").click(function(){ amplifier.mp3.repeat(); });
        $("#mp3-prev").click(function(){ amplifier.mp3.prev(); });
        $("#mp3-play").click(function(){ amplifier.mp3.play(); });
        $("#mp3-next").click(function(){ amplifier.mp3.next(); });
        $("#mp3-shuffle").click(function(){ amplifier.mp3.shuffle(); });
        $("#mp3-playing").click(function(){ amplifier.mp3.playing(); });
      },
      showNetworkFailed: function () {
        alert("server connection failed");
      },
      selectMedia: function() {
        $.get(amplifier.network.url + "set/selectMedia", function(data) {
          amplifier.updateGui("media"); 
        });
      },
      selectMp3: function() {
        $.get(amplifier.network.url + "set/selectMp3", function(data) {          
          // Show song currently playing
          $.getJSON(amplifier.network.url + "mpd/index.php?cmd=getCurrentSong", function(data) {
              amplifier.mp3.song.title = data.Title;
              amplifier.mp3.song.artist = data.Artist;
              amplifier.updateGui("mp3");
            }).fail(function() {
              amplifier.mp3.song.title = "network"
              amplifier.mp3.song.artist = "error";
            })
        });
      },
      selectRadio: function() {
        $.get(amplifier.network.url + "set/selectRadio", function(data) {            
            amplifier.radio.updatePanel(amplifier.radio.stations, data);
            amplifier.updateGui("radio");
        });
      },
      selectAux: function() {
        $.get(amplifier.network.url + "set/selectAux", function(data) {       
            amplifier.updateGui("aux");
        });
      },

      /**
       * Aux Object
       */
      aux: {
        update: function(json) {
        },
        updatePanel: function() {
          $("#info-volume").html("Volume: " + amplifier.audio.volume);
          $("#info-mute").html("Mute: " + amplifier.audio.mute);
          $("#info-treble").html("Treble: " + amplifier.audio.treble);
          $("#info-bass").html("Bass: " + amplifier.audio.bass);   
        }
      },

      /**
       * Network Object
       */
      network: {
        url: "http://192.168.1.7/",
        timer: null,
        delay: 5000,
        init: function() {
          window.clearTimeout(amplifier.network.timer);
        },
        start: function() {      
            //console.log("starting network timer");
            // Refresh Device Settings            
            $.getJSON(amplifier.network.url + "get/all", function(json) {                            
              amplifier.updateStateFromDevice(json);
              amplifier.updateGui(json.state);
              //if(amplifier.network.timer == null) {
                amplifier.network.timer = setTimeout(function() {
                  amplifier.network.start()
                }, amplifier.network.delay);
              //}
            }).fail(function(json) {
              amplifier.showNetworkFailed();              
            });           
          },
        stop: function() {
            //console.log("stopping network timer");
            window.clearTimeout(amplifier.network.timer);
            this.timer = null;
          }
      },

      /**
       * Media Object
       */
      media: {
        updatePanel: function() {
          this.clock.start();          
        },
        clock: {
          months: ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"],
          timer: null,     
          getTime: function (){
            var d = new Date();
            var month = d.getMonth();
            var day = d.getDate();
            return (day<10 ? '0' : '') + day + " " + this.months[d.getMonth()];
          },
          start: function(){
            this.show();          
            this.timer = setTimeout(function(){
              amplifier.media.clock.start()},
              500);
          },
          stop: function(){
            window.clearTimeout(this.timer);
          },
          show: function(){
            var d = new Date();
            $("#media-date").text(d.toDateString());
            $("#media-clock").text(d.toLocaleTimeString());
          }
        }
      },

      /**
       * Radio Object
       */
      radio: {
        volume:0, // set a default volume
        station:876, // set a default station,
        stationIdx:0,
        data:"",
        stations:[
                  {"name":"Vision FM",// Mhz/87.8 Mhz/88.0 Mhz (Various suburbs) Vision FM
                   "freq":"876"}, //"88.0 Mhz (Brisbane CBD and Moreton Island)                 
                  {"name":"SBS Radio",
                   "freq":"933"}, // Mhz SBS Radio (international languages)
                  {"name":"River",
                   "freq":"949"},// Mhz River 94.9
                  {"name":"Family FM",
                   "freq":"965"}, // Mhz 96five Family FM
                  {"name":"FM Mix",
                   "freq":"973"}, // Mhz 97.3 FM MIX
                  {"name":"Ethnic",
                   "freq":"981"}, // Mhz 4EB (ethnic community radio)
                  {"name":"Indigenous",
                   "freq":"989"}, // Mhz 98.9 FM (indigenous community radio)
                  {"name":"Bay FM",
                   "freq":"1003"}, // Mhz Bay FM
                  {"name":"101.1 FM",
                   "freq":"1011"}, // Mhz 101.1 FM
                  {"name":"4ZZZ",
                   "freq":"1021"}, // Mhz 4ZZZ
                  {"name":"4MBS",
                   "freq":"1037"}, // Mhz 4MBS
                  {"name": "Triple M",
                   "freq":"1045"}, // Mhz Triple M
                  {"name":"B105 FM",
                   "freq":"1053"}, // Mhz B105 FM
                  {"name":"Classic FM",
                   "freq":"1061"}, // Mhz ABC Classic FM
                  {"name":"Nova FM",
                   "freq":"1069"}, // Mhz Nova 106.9
                  {"name":"Triple J",
                   "freq":"1077"} // Mhz Triple J
                ],
        getNameFromFrequency: function(freq) {
          for(var i=0; i<this.stations.length; i++) {
            if(this.stations[i].freq == freq) {
              return this.stations[i].name;
            }
          }
        },
        getIdxFromFrequency: function(freq) {
          for(var i=0; i<this.stations.length; i++) {
            if(this.stations[i].freq == freq) {
              return i;
            }
          }
        },
        prev: function(){
          // negate counter
          this.stationIdx--;
          if(this.stationIdx<0){
            this.stationIdx=this.stations.length-1;
          }
          return this.setByIndex(this.stationIdx);
        },
        next: function(){
          // increment counter
          this.stationIdx++;
          if(this.stationIdx>=this.stations.length){
            this.stationIdx=0;
          }
          return this.setByIndex(this.stationIdx);
        },
        setByFrequency: function(freq){
          amplifier.radio.stationIdx = amplifier.radio.set
          $.get(amplifier.network.url + "set/radioStation/" + freq, function(data) {
            amplifier.radio.station = data.radio.station;
            amplifier.radio.updatePanel();
          });   
        },
        setByIndex: function(index){
          amplifier.radio.stationIdx = index;
          $.get(amplifier.network.url + "set/radioStation/" + amplifier.radio.stations[index].freq, function(data){
            amplifier.radio.station = data.radio.station;
            amplifier.radio.updatePanel();
          });
        },
        updatePanel: function() {
          $("#radio-frequency").text(parseFloat(amplifier.radio.station) / 10);
          // Reverse lookup name of station from frequency
          for(var i=0; i< amplifier.radio.stations.length; i++) {
            if(amplifier.radio.stations[i].freq == amplifier.radio.station) {
              $("#radio-name").text(amplifier.radio.stations[i].name);
              break;
            }
          }
          // rbds scrolling text
        }
      },

      /**
       * MP3 Object
       */
      mp3: {
        volume:"0",
        playState: false,
        repeatState: false,
        shuffleState: false,
        playingState: false,
        currentlyPlaying: {},
        song: {
          "title": "",
          "artist": ""
        },
        update: function(json) {
          this.song = json.mp3;
        },
        list: function() {

        },
        repeat: function() {
          amplifier.mp3.repeatState = !amplifier.mp3.repeatState;
          $.get(amplifier.network.url + "mpd/index.php?cmd=repeat&on=" + amplifier.mp3.repeatState, function(data) {
            amplifier.mp3.updatePanel(data);
          });
        },
        prev: function() {
          $.get(amplifier.network.url + "mpd/index.php?cmd=prevSong", function(data) {
            amplifier.mp3.updatePanel(data);
          });
        },
        play: function() {
          $.get(amplifier.network.url + "mpd/index.php?cmd=play", function(data) {
            amplifier.mp3.updatePanel(data);
          });
        },
        next: function() {
          $.get(amplifier.network.url + "mpd/index.php?cmd=nextSong", function(data) {
            amplifier.mp3.updatePanel(data);
          });
        },
        shuffle: function() {
          amplifier.mp3.shuffleState = !amplifier.mp3.shuffleState;
          $.get(amplifier.network.url + "mpd/index.php?cmd=shuffle&on=" + amplifier.mp3.shuffleState, function(data) {
            amplifier.mp3.updatePanel(data);
          });
        },
        playing: function() {
          // Switch between playlist view and currently playing view
        },
        updatePanel: function() {
          if (typeof amplifier.mp3.song != 'undefined') {
              $("#music-playing").html(amplifier.mp3.song.title);
          }
          if (typeof amplifier.mp3.song != 'undefined') {
              $("#music-artist").html(amplifier.mp3.song.artist); 
          }          
          //console.log("updating mp3 panel");
          //console.log(amplifier);
        }
      }     
    }

    // Initialise the main amplifier panel
    amplifier.init();
});