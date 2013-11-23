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
        amplifier.updateKnobs(state);
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
      updateKnobs: function(state) {
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
        // Update Volume Knob Value
        amplifier.volumeKnob.i = parseInt(amplifier.audio.volume);
        amplifier.volumeKnob.$ival.html(amplifier.volumeKnob.i);        
        // Update knob background colours
        // $("#vol-slider").css('background', a);
        // $("#vol-slider a").css('border', '4px solid ' + b).css('background-color', c);
        // $("#vol-slider").slider("value", this.audio.volume);
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
          amplifier.radio.update(json);
          // Mp3
          amplifier.mp3.update(json);
      },
      volumeKnob: {
        v: null,
        up:0,
        down:0,
        i:0,
        $idir: $("div.idir"),
        $ival: $("div.ival"),
        incr: function() {
              if(amplifier.volumeKnob.i<100) {
                amplifier.volumeKnob.i++;
                amplifier.volumeKnob.$idir.show().html("+").fadeOut();
                amplifier.volumeKnob.$ival.html(amplifier.volumeKnob.i);

                amplifier.network.stop();
                $.get(amplifier.network.url + "set/volume/" + amplifier.volumeKnob.i, function(amp) {
                  amplifier.audio.volume = amp.volume
                  amplifier.network.start();
                });
              }
            },
        decr: function() {
            if(amplifier.volumeKnob.i>0) {
              amplifier.volumeKnob.i--;
              amplifier.volumeKnob.$idir.show().html("-").fadeOut();
              amplifier.volumeKnob.$ival.html(amplifier.volumeKnob.i);

              amplifier.network.stop();
              $.get(amplifier.network.url + "set/volume/" + amplifier.volumeKnob.i, function(amp) {
                amplifier.audio.volume = amp.volume
                amplifier.network.start();
              });
            }
        },
        change: function(value) {
          if(amplifier.volumeKnob.v > value) {
                if(amplifier.volumeKnob.up) {
                    amplifier.volumeKnob.decr();
                    amplifier.volumeKnob.up=0;
                } else {
                    amplifier.volumeKnob.up=1;
                    amplifier.volumeKnob.down=0;
                }
            } else {
                if(amplifier.volumeKnob.v < value) {
                    if(amplifier.volumeKnob.down) {
                        amplifier.volumeKnob.incr();
                        amplifier.volumeKnob.down=0;
                    } else { 
                        amplifier.volumeKnob.down=1;
                        amplifier.volumeKnob.up=0;
                    }
                }
            }
            amplifier.volumeKnob.v = value;
        }
      },      
      setupButtonHandlers: function() {
        // Top Nav Button Handlers
        $("#btn-media").click(function(){ amplifier.selectMedia(); });
        $("#btn-mp3").click(function(){ amplifier.selectMp3(); });
        $("#btn-radio").click(function(){ amplifier.selectRadio(); });
        $("#btn-aux").click(function(){ amplifier.selectAux(); });

        // Main Volume Knob
        $("input.infinite").knob({
          min: 0,
          max: 20,
          stopper: false,
          change: function (value) {
            //console.log(el);
            amplifier.volumeKnob.change(value);
          }
        });

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
        // Show overlay
        $("body").mask("<p class='retry-spinner'/><p>Network Error...</p><p class='retry-now'><a class=\"retry-now-a\" href=\"javascript:location.reload();\">retry now</a></p>");        
      },
      selectMedia: function() {
        $.get(amplifier.network.url + "set/selectMedia", function(data) {
          amplifier.updateGui("media"); 
        });
      },
      selectMp3: function() {
        $.get(amplifier.network.url + "set/selectMp3", function(data) {          
          // Show song currently playing
          // mpd/index.php?cmd=getCurrentSong"
          $.getJSON(amplifier.network.url + "get/all", function(data) {
            console.log(data)
            if (typeof data.mp3 === 'object') {
              amplifier.mp3.song.title = data.mp3.title;
              amplifier.mp3.song.artist = data.mp3.artist;                        
            } else {       
              console.log("FALSE!!!!!!!!!!!!!!!");
              console.log(data.mp3); 
              amplifier.mp3.song.title = "server down";
              amplifier.mp3.song.artist = "server down";
              console.log(amplifier.mp3);              
            }
            amplifier.updateGui("mp3");
            }).fail(function() {
              amplifier.mp3.song.title = "network error";
              amplifier.mp3.song.artist = "network error";
            })
        });
      },
      selectRadio: function() {
        $.get(amplifier.network.url + "set/selectRadio", function(data) {            
            amplifier.radio.updatePanel();
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
        delay: 10000,
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
        station: {},        
        prev: function() {
          $.get(amplifier.network.url + "set/prevRadioStation/", function(data) {
            amplifier.radio.station = data.radio;
            amplifier.radio.updatePanel();
          });
        },
        next: function() {          
          $.get(amplifier.network.url + "set/nextRadioStation/", function(data) {
            amplifier.radio.station = data.radio;
            amplifier.radio.updatePanel();
          });
        },
        setByIndex: function(index) {          
          $.get(amplifier.network.url + "set/radioStationIndex/" + index, function(data) {
            amplifier.radio.station = data.radio;
            amplifier.radio.updatePanel();
          });
        },
        updatePanel: function() {
          $("#radio-frequency").text(parseFloat(amplifier.radio.station.frequency) / 10);
          $("#radio-name").text(amplifier.radio.station.name);
         },
        update: function(data) {
          amplifier.radio.station = data.radio;
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
          var title = "Server error";
          var artist = "";
          if (typeof amplifier.mp3.song != 'undefined' && amplifier.mp3.song != false) {
            console.log("song isn't false...");
            title = amplifier.mp3.song.title
            artist = amplifier.mp3.song.artist
          }
          $("#music-playing").html(title);
          $("#music-artist").html(artist);           
        }
      }     
    }

    // Initialise the main amplifier panel
    amplifier.init();
});