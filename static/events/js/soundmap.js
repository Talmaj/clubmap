/*
 * Clubmaps Javascript core
 * Given a JSON Dataset constructs interconnected map and player
 * 
 * EXAMPLE of dataset
 * 
 * {"name": "Let\u00b4s Stay Awake with Thoma", 
 *  "long": 13.4220073, 
 *  "location": "Promenaden Eck", 
 *  "artists": [1495169], 
 *  "lat": 52.475866, 
 *  "id": 3}
 **/
(function ($) {

    var MAPTYPE_ID = 'gray_style';

    $.widget( "cm.scplayer", {
        
        /* ==================
         * public parameters
         * ==================
         * 
         * client id: 5b3cdaac22afb1d743aed0031918a90f
         * artists are given from django
         */
        options: {
            client_id: 0,
            data:[],
            playlist_container: null,
            control_container:null,
            map_container: this.element,
            event_container: null,
            map_options: {
                zoom: 12,
                center: new google.maps.LatLng(52.52001, 13.40495),
                mapTypeId: MAPTYPE_ID//google.maps.MapTypeId.HYBRID
            }
        },

        _create: function(){
            /*=================
             * Private variables
             * ================
             */
            
            //a list with the current playlist based on artists
            //this.playlist = [];
            //a list of html elements which represent the playlist in the DOM
            //this.playlist_el = []
            //current index of playlist
            this.current = 0;
            //current soundManager object
            this.current_sound = null;
            //img elements with waveform information
            this.timeline = null;
            //waveform object
            this.waveform = null;
            //progress element
            this.progress = null;
            //actual playback position
            this.position = null;
            //total time
            this.end = null;
            //map handler
            this.map = null;
            //helper variable to save current event id
            this.current_party = 0;
            //Loading Overlay shown on pageload while searchng tracks and building map
            this.loadingOverlay = $('#loadingOverlay');
            //number of artists in data
            this.artists_count = 0;
            /*=================
             * Constructor
             * ================
             */
            SC.initialize({client_id:this.options.client_id});
            var me = this;
            var user_tracks = [];
            var def = [];
            var progress = 0;
            $('#info h2.ev_count').text('we found '+ me.options.data.length + ' events for you');

            //search for best tracks for each user
            jQuery.each(me.options.data, function(data_index, party){
                party.tracks = [];
                me.artists_count += party.artists.length;
                jQuery.each(party.artists, function(index, id){
                    var dfd = $.Deferred();
                    //gets all tracks based on user id
                    SC.get("/tracks", {user_id: id}, function (tracks) {
    
                        user_tracks = tracks;
                        try {
                            //sort all tracks
                            user_tracks.sort(function (b, a) {
                                //sort tracks by score
                                var scoreA = a.download_count + a.playback_count + 2 * a.favoritings_count;
                                var scoreB = b.download_count + b.playback_count + 2 * b.favoritings_count;
                                return scoreA - scoreB;
                            });

                            //merge lists faster

                            $.merge(party.tracks, user_tracks.slice(0, 3));
                            console.log("done getting tracks");
                        } catch(err){
                            console.log("error getting some tracks");
                        }
                        dfd.resolve();
                        progress++;
                        me.updateLoadingOverlay(progress);
                    });
                    def.push(dfd.promise());

                });
            });

            $.when.apply($, def).done(function(){
                me.updateLoadingOverlay('initializing map...');
                me.createUI();
                me.createMap();
                me.waveform = new Waveform({
                    container: $(me.progress)[0],   
                    outerColor: "rgba(0,0,0,0)",
                    innerColor:function(x,y){
                        if(1){
                              if (x < me.current_sound.position / me.current_sound.durationEstimate) {
                                return "rgba(255,  30, 102, 0.8)";
                              } else if (x < me.current_sound.bytesLoaded / me.current_sound.bytesTotal) {
                                return "rgba(255, 255, 255, 0.8)";
                              } else {
                                return "rgba(100, 100, 100, 0.4)";
                              }
                      } else {
                        return "rgba(0, 0, 0, 0)"
                      }
                }
                });             
            });
            //me.createUI();
        },
        
        /*
         * ========
         * Goes to previous track in playlist
         * ========
         */
        previous: function () {
            var me = this;
            var next = me.current - 1;
            var next_party = me.current_party;
            
            if (next < 0) {
                //go to previous party
                //next_party = next_party-1;
                do {
                    next_party = next_party - 1;
                    if(next_party < 0){
                        next_party = data.length-1;
                    }
                    
                    if(next_party == me.current_party){
                        break;
                    }
                } while (me.options.data[next_party].tracks.length <= 0 || me.options.data[next_party].visible == false);

                next = me.options.data[next_party].tracks.length-1;
            }
            
            if (me.current_sound !== null) { me.current_sound.destruct(); }
            me.current_sound = null;
           
            
            me.options.data[me.current_party].playlist_el.removeClass("active");
            me.options.data[me.current_party].tracks[me.current].playlist_el.removeClass("active")
            
            //If party changed move into the middle of playlist
            if(me.current_party !== next_party) {
                me.movePlaylistToEvent(next_party,500); 
            }            
            
            me.current = next;
            me.current_party = next_party;
            me.play();
            
            
        },
        /*
         * ========
         * Goes to next track in playlist
         * This method is called at the end of each track automatically
         * ========
         */
        next: function () {
            var me = this;
            var next = me.current + 1;
            var next_party = me.current_party;
            
            if(next >= me.options.data[me.current_party].tracks.length){
                //go to next party
                
                //next_party = next_party+1;
                do{
                    next_party = next_party + 1;
                    if(next_party >= me.options.data.length){
                        next_party = 0;
                    }
                    if (next_party == me.current_party){
                        break;
                    }
                } while (me.options.data[next_party].tracks.length <= 0 || me.options.data[next_party].visible == false);
                next = 0;
            }
            
            if(me.current_sound != null) me.current_sound.destruct();
            me.current_sound = null;
            
            me.options.data[me.current_party].playlist_el.removeClass("active");
            me.options.data[me.current_party].tracks[me.current].playlist_el.removeClass("active")
            
            //If party changed move into the middle of playlist
            if(me.current_party !== next_party) {
                me.movePlaylistToEvent(next_party,500); 
            }
            
            me.current = next;
            me.current_party = next_party;
            me.play();          
        },
        
        goTo:function(pi,ti){
            var me = this;
            
            if( (pi >= 0 && pi < me.options.data.length) && 
                (ti >= 0 && ti < me.options.data[pi].tracks.length) ){
                    
                    if(me.current_sound != null) me.current_sound.destruct();
                    me.current_sound = null;
                                        
                    me.options.data[me.current_party].playlist_el.removeClass("active");
                    me.options.data[me.current_party].tracks[me.current].playlist_el.removeClass("active")
                    
                    //If party changed move into the middle of playlist
                    if(me.current_party !== pi) {
                        me.movePlaylistToEvent(pi,500); 
                    }
                    me.current = ti;
                    me.current_party = pi;
                    
                    me.play();
            
            } else {
                console.log("ERROR: track index is out of bounds "+pi+', '+ti);
            }
        },
        /*
         * ======
         * This funciton is called periodically while a track is playing and updates waveform and times
         * ======
         */
        updateTimeline:function(){
            var me = this;
            /*
            var pos = ((me.current_sound.position/me.current_sound.durationEstimate)*100)+"%";
            console.log(me.current_sound.position);
            me.progress.css("width",pos);
            */
            me.waveform.redraw();
        },
        loadingCallback:function(){
            var me = this;
            me.waveform.redraw();
        },
        /*
         * ======
         * Plays or pauses a track depending of the state the player is in
         * ======
         */
        play: function(){
            
            var me = this;
            console.log(me.options.data);
            if (me.current_sound === null) {
                //nothin is playing so when stream is ready play new sound
                console.log(me.current_party, me.current);
                SC.stream("/tracks/"+me.options.data[me.current_party].tracks[me.current].id,{preferFlash:false, useHTML5Audio:true, whileloading:function(){me.loadingCallback()}, whileplaying:function(){me.updateTimeline();}, onfinish:function(){me.next();}} , function(sound){
                    me.current_sound = sound;   
                    me.current_sound.play();
                    me.playing = true;
                    me.end.text(me.current_sound.durationEstimate);
                    me.updateWaveform();
                });
                me.options.data[me.current_party].playlist_el.addClass("active");
                me.options.data[me.current_party].tracks[me.current].playlist_el.addClass("active");
                //me.playlist_el[me.current].addClass("active");
                me.moveMapToEvent(me.current_party);


            } else {
                me.current_sound.togglePause();
            }
            //this.element.text('playing');
        },
        
        /*
         * =====
         * updates the waveform in both containers to the current track.
         * =====
         */
        updateWaveform: function (){
            
            var me = this;
            me.waveform.dataFromSoundCloudTrack(me.options.data[me.current_party].tracks[me.current]);
            /*
            me.progress.css("width",0);
            var path = me.playlist[me.current].waveform_url;
            me.waveform.attr("src",path);*/
            
        },
        
        /*
         * ======
         * Initialize google map
         * ======
         */
        createMap:function(){
            
            var me = this;
            me.map = new google.maps.Map(document.getElementById('main_map'), me.options.map_options);
            var styledMapOptions = {name: 'Custom Style'};
            var customMapType = new google.maps.StyledMapType(featureOpts, styledMapOptions);
            me.map.mapTypes.set(MAPTYPE_ID, customMapType);
            
            google.maps.event.addListener(me.map, 'bounds_changed',function(){
                me.updatePlaylist();

            } );

            google.maps.event.addListenerOnce(me.map, 'tilesloaded', function(){
                me.removeLoadingOverlay();
            });
            
            //create markers on map
            jQuery.each(this.options.data, function (index, party){
                party.marker = new google.maps.Marker({
                    position: new google.maps.LatLng(party.lat, party.long),
                    map: me.map,
                    title: party.name + ' @ ' + party.location,
                    icon: miniMarker
                });
                
                //add behaviour to marker
                google.maps.event.addListener(party.marker, 'click', function(){
                    me.map.panTo(party.marker.getPosition());
                    me.map.setZoom(17);
                    
                    //TODO call ajax code to display event overlay
                });
            })
            
        },
        
        updateEventVisibility: function(){
            var me = this;
            var bounds = me.map.getBounds();
            jQuery.each(me.options.data, function(data_index, party){
                if(bounds.contains(party.marker.getPosition())){
                    party.visible = true;
                }  else {
                    party.visible = false;
                }
            });
        },
        
        loadEvent:function(id){
            
            var me = this;
            var el = me.options.event_container;
            
            //TODO load event from django to display extended information incl. artwork
            
        },
        
        moveMapToEvent:function(id){
            
            var me = this;
            var coord = new google.maps.LatLng(me.options.data[id].lat, me.options.data[id].long);
            me.map.panTo(coord);
            
        },
        
        movePlaylistToEvent:function(id,delay){
            
          var me = this;
          var el = me.options.data[id].playlist_el;
          var playlist = me.options.playlist_container;
          
          playlist.animate({
              scrollTop: el.position().top
              },delay);
        },
        
        /*
         * =======
         * Creates the user interface
         * =======
         */
        createUI: function(){
            var me = this;
            var el = me.options.playlist_container;
            var ctrl = $('<div></div>', {
                class:'cm_player ctrl'
            });
            
            var prev = $('<div></div>', {
                class:'cm_player btn prev'
            }).appendTo(ctrl).text("<<");
            prev.click(function(){me.previous();});
            
            var play = $('<div></div>', {
                class:'cm_player btn play'
            }).appendTo(ctrl).text(">");
            //bind to play 
            play.click(function(){me.play();});
            
            var next = $('<div></div>', {
                class:'cm_player btn next'
            }).appendTo(ctrl).text(">>");
            next.click(function(){me.next();});
            //info button
            
            me.timeline = $('<div></div>', {
                class:'cm_player timeline'
            }).appendTo(ctrl);
             
            //function to navigate through track
            me.timeline.click(function(e){
                var offset = $(this).offset();
                var percent = (e.pageX - offset.left)/$(this).width();
                console.log("jump to" + Math.floor(percent*me.current_sound.durationEstimate)); 
                me.current_sound.setPosition(Math.floor(percent*me.current_sound.durationEstimate));
            });
            
            me.progress = $('<div></div>', {
                class:'cm_player progress'
            }).appendTo(me.timeline);
            
            //me.waveform = $('<img/>', {class:'cm_player waveform'}).appendTo(timeline)
            
            //TODO
            var position = $('<div></div>', {
                class:'cm_player position'
            }).appendTo(me.timeline);
            
            //TODO
            me.end = $('<div></div>', {
                class:'cm_player end'
            }).appendTo(me.timeline);
            
            //create Plalist
            console.log("creating playlist");
            me.createPlaylist();
            ctrl.appendTo(me.options.control_container);
        },
        
        createPlaylist: function(){
            var me = this;
            console.log('data',me.options.data)
            var playlist_wrapper = $('<div></div>', {
                class:'cm_player playlist'
            });
            
            var party_ul = $('<ul></ul>', {
                class:'cm_player events'
            }).appendTo(playlist_wrapper);
            
            
            //create playlist
            jQuery.each(me.options.data ,function(di, party){
                    me.createEvent(di).appendTo(party_ul);
            });
            playlist_wrapper.appendTo(me.options.playlist_container);
        },
        
        updatePlaylist: function(){
            
            var me = this;
            me.updateEventVisibility();
            
            jQuery.each(me.options.data ,function(di, party){
                var el = party.playlist_el;
                var playing = me.options.data[me.current_party].playlist_el;
                //don't touch active party
                if(!el.hasClass('active')){
                    //check if element is visible and is already shown
                    if(party.visible == false && !el.hasClass('hidden')){
                        el.addClass('hidden');
                    } else Counter
                    if(party.visible == true && el.hasClass('hidden')){
                        el.removeClass('hidden');
                    }
                    me.options.playlist_container.scrollTop(playing.position().top);
                }
                
            
            });
            
            
        },
        
        removeEvent: function(di){
            var me = this;
            me.options.data[di].playlist_el.remove();
            me.options.data[di].playlist_el = null;
        },
        /*
         * creates an Event and saves the element in data
         * WARNING: DANGEROUS saves el into data before inserting into dom
         */
        createEvent: function(di){
            var me = this;
            var ev = me.options.data[di];
            ev.playlist_el = $('<li class = "event" ><div class="event_info"><span class = "cm_player index">' + di + '</span> <span class="cm_player name">'+ ev.name +'</span> <span class="cm_player location">' + ev.location + '</span></div></li>');
            ev.playlist_el.data('id',ev.id);
            ev.playlist_el.hover(function(){
                ev.playlist_el.toggleClass('hovered',250, "swing");
            });
            
            if(ev.tracks.length <= 0){
                ev.playlist_el.addClass('no-tracks');
            } else {
                //create tracklist
                var playlist_ul = $('<ul></ul>', {
                    class:'cm_player playlist'
                }).appendTo(ev.playlist_el);
                
                jQuery.each(ev.tracks, function(ti, track){
                    var shading;
                    if (ti % 2 == 0){ 
                        shading = "even"; 
                    } else { 
                        shading = "odd"; 
                    }
                    var li = $('<li class = "track ' + shading + '" ><span class = "cm_player index">' + (ti+1) + '</span> <span class="cm_player t_title">'+ track.title +'</span> <span class="cm_player artist">' + track.user.username + '</span></li>').appendTo(playlist_ul);
                    li.click(function(){ 
                        me.goTo(di,ti); 
                        //li.addClass("active");
                        });
                    ev.tracks[ti].playlist_el = li;
                });
            }
            
            return ev.playlist_el;
        },

        showLoadingOverlay: function(){
            var me = this;
            //create Overlay
            me.loadingOverlay = $('' +
            '<div id = "loadingOverlay">' +
            '   <div id="info">' +
            '       <h1>Welcome to the Clubmap</h1>' +
            '       <h2> we found ' + me.options.data.length + ' events for you!</h2>' +
            '       <span>collecting sounds <span id = "progress">0%</span> </span>' +
            '   </div>' +
            '</div>').prependTo('#top');


        },
        updateLoadingOverlay: function(di){
            var me = this;
            var el = $('#progress')
            if (!isNaN(di)) {
                var p = Math.round((di / (me.artists_count) ) * 100);
                el.text(p + '%');
            } else {
                el.parent().text(di);
            }

        },
        removeLoadingOverlay: function(){
            if(this.loadingOverlay != null){
                this.loadingOverlay.remove();
                this.loadingOverlay = null;
            }
        }
        

    });
}(jQuery));


/*
 * TODO get data from django

data = [{"name": "Let\u00b4s Stay Awake with Thoma", "long": 13.4220073, "location": "Promenaden Eck", "artists": [1495169], "lat": 52.475866, "id": 3}, {"name": "Manic.Monday mit Igor Westphal", "long": 13.46406, "location": "Minimal Bar", "artists": [], "lat": 52.51639, "id": 5}, {"name": "Berlin Underground", "long": 13.3836406, "location": "Solar", "artists": [402020], "lat": 52.5042808, "id": 6}, {"name": "Montag auf Cr\u00e4ck", "long": 13.4543612, "location": "Crack Bellmer", "artists": [86907032, 56107832], "lat": 52.5076327, "id": 2}, {"name": "Lick my Needle", "long": 13.400785, "location": "Mein Haus Am See", "artists": [17326180], "lat": 52.5302189, "id": 7}, {"name": "Electric Monday", "long": 13.416946, "location": "KitKatClub", "artists": [103, 3713533, 215006, 4605971], "lat": 52.509718, "id": 1}, {"name": "-Closed-", "long": 13.4201002, "location": "Tresor", "artists": [], "lat": 52.5108799, "id": 4}, {"name": "Die Seligen Augenblicke mit Arma", "long": 13.4220073, "location": "Promenaden Eck", "artists": [124535], "lat": 52.475866, "id": 12}, {"name": "go.play\t\t\t\t mit Dizko Raum", "long": 13.46406, "location": "Minimal Bar", "artists": [9559116], "lat": 52.51639, "id": 14}, {"name": "Mittelmeermusik", "long": 13.3836406, "location": "Solar", "artists": [2376, 1710602], "lat": 52.5042808, "id": 17}, {"name": "Dienstags Bellmeria", "long": 13.4543612, "location": "Crack Bellmer", "artists": [15555225], "lat": 52.5076327, "id": 16}, {"name": "all Live", "long": 13.43285, "location": "Loophole", "artists": [2525546], "lat": 52.4806, "id": 18}, {"name": "The Unknown presents Amato Funk & Welpenberg", "long": 13.400785, "location": "Mein Haus Am See", "artists": [11149266, 3704890], "lat": 52.5302189, "id": 15}, {"name": "Encore.une.Fois", "long": 13.4543612, "location": "Suicide Circus", "artists": [2582083, 696579], "lat": 52.5076327, "id": 8}, {"name": "Golden Times (Only Once a Month)", "long": 13.41693, "location": "Golden Gate", "artists": [696579, 1369562, 22954633, 319139, 19138106], "lat": 52.51601, "id": 9}, {"name": "Tuesday Sound Department", "long": 13.4525442, "location": "Hoppetosse", "artists": [30470, 6930215, 258837], "lat": 52.4970479, "id": 10}, {"name": "Between the Lines with Alicia Hush, ana+one and Philipp Wolgast", "long": 13.448507, "location": "Chalet", "artists": [402340, 41455674, 2161], "lat": 52.4976474, "id": 11}, {"name": "Dienstagswelt: Moondawn Memories", "long": 13.4543612, "location": "Cassiopeia", "artists": [1992, 9242927, 20490442], "lat": 52.5076327, "id": 13}, {"name": "10 Jahre HDT! True Afterhour.", "long": 13.41693, "location": "Golden Gate", "artists": [4891323, 72322, 114541030, 90715, 8240552, 2500867, 1255769], "lat": 52.51601, "id": 45}, {"name": "Visitor.Area mit Tolga Top & Steven Moeller", "long": 13.46406, "location": "Minimal Bar", "artists": [], "lat": 52.51639, "id": 37}, {"name": "Cage me if you can", "long": 13.4220073, "location": "Promenaden Eck", "artists": [874409, 180945, 342885, 5702310, 72303], "lat": 52.475866, "id": 39}, {"name": "Kiasmos - Album Release Show", "long": 13.445463, "location": "Watergate", "artists": [1639865], "lat": 52.500914, "id": 41}, {"name": "Monkeytown Fest", "long": 13.3820426, "location": "Tempodrom", "artists": [66131337, 436261, 1128772, 7665634], "lat": 52.501443, "id": 33}, {"name": "Arca with Jesse Kanda", "long": 13.4414345, "location": "Berghain/Panorama Bar", "artists": [10258324, 22618815, 36997953], "lat": 52.5110627, "id": 35}, {"name": "Un_known", "long": 13.4559936, "location": "AVA Club", "artists": [1272688, 52086727, 6075568], "lat": 52.5002114, "id": 26}, {"name": "Assslap", "long": 13.4287614, "location": "Heinz Sch\u00fcftan", "artists": [2040472, 461898, 1129337], "lat": 52.4900331, "id": 29}, {"name": "05 Dezember - 08 Dezember - FR", "long": 13.45724, "location": "Griessmuehle", "artists": [2590355, 90552293, 16605746, 2622393, 73399, 35943989, 18116, 670413, 241263, 52564261, 236170, 2795935], "lat": 52.47473, "id": 34}, {"name": "Halfwayhouse Christmas Block Party", "long": 13.4313729, "location": "Lagari", "artists": [508958, 56714706, 30890193], "lat": 52.4906354, "id": 53}, {"name": "Call it Soulstep", "long": 13.4114447, "location": "An Einem Sonntag Im August", "artists": [], "lat": 52.5401982, "id": 63}, {"name": "A C I D", "long": 13.4242, "location": "Bohnengold", "artists": [99604593, 92071940, 18828073], "lat": 52.49762, "id": 40}, {"name": "Black Magic", "long": 13.440378, "location": "Sameheads", "artists": [46073180, 7403330, 471383, 1923055, 11860036], "lat": 52.477893, "id": 47}, {"name": "Electronicbodymove", "long": 13.4189874, "location": "Paloma Bar", "artists": [90715, 8240552], "lat": 52.4993177, "id": 60}, {"name": "Lustgarten mit Hunee & Dickie Rosewater", "long": 13.43533, "location": "Loftus Hall", "artists": [372, 1621136, 495546, 3979691], "lat": 52.49033, "id": 23}, {"name": "What They Really Want To Play N\u00b06 with Patrice Scott & Hinode", "long": 13.3784562, "location": "Humboldthain Club", "artists": [6453514, 4044989, 746056], "lat": 52.5443814, "id": 27}, {"name": "Dunkel Launch Party", "long": 13.40791, "location": "st.GEORG", "artists": [16516927, 65686362, 637547, 17780552, 13661114], "lat": 52.50291, "id": 30}, {"name": "Danach Kommt DIE Party", "long": 13.4309804, "location": "Basement 8", "artists": [1691500, 27015, 568008], "lat": 52.4985501, "id": 46}, {"name": "dBs Music Berlin Xmas Ho-Ho-Down", "long": 13.4543612, "location": "Urban Spree", "artists": [4801379, 13434410, 1210551], "lat": 52.5076327, "id": 54}, {"name": "Studio Sessions with Marcel Freigeist, Alexander Lorz, Edgar Peng", "long": 13.416297, "location": "Weekend", "artists": [1369562, 911394], "lat": 52.522867, "id": 55}, {"name": "STEAM\u00b0 with Secret Headliner", "long": 13.4543612, "location": "Urban Spree", "artists": [10494188, 226116, 3985359], "lat": 52.5076327, "id": 56}, {"name": "Rare 45's Night with Herr Hobrecht & Friends", "long": 7.011595, "location": "Improkdr", "artists": [3350712, 4868, 15756178], "lat": 50.972759, "id": 57}, {"name": "Keinklub: Initial *Label Showcase", "long": 13.5614974, "location": "Neu West Berlin", "artists": [7303], "lat": 52.501744, "id": 58}, {"name": "Playground", "long": 13.416297, "location": "Sky Club Berlin", "artists": [734983, 78821412], "lat": 52.522867, "id": 59}, {"name": "10 Jahre Club Treibhaus", "long": 12.08274, "location": "Club Treibhaus Gl\u00f6wen", "artists": [412604, 6955090, 87269, 5956182, 14260388, 18271418, 91074258, 16020972, 5982348, 30179430, 4318941, 347219, 85963, 8221100, 1177467, 191876, 2135945, 11715947, 99991115], "lat": 52.91278, "id": 61}, {"name": "Flicker Rhythm is a Dancer", "long": 13.46246, "location": "Rosi's", "artists": [79859363, 87329], "lat": 52.50516, "id": 43}, {"name": "Ostfunk & Friends - der Letzte Tanz", "long": 13.436794, "location": "Dublex", "artists": [57700009, 11837943], "lat": 52.508725, "id": 62}, {"name": "Move.Your.Body", "long": 13.47485, "location": "Kosmonaut", "artists": [876528, 127688, 37436, 152610, 12858806, 9246328, 13559793], "lat": 52.50779, "id": 19}, {"name": "Naive Melodies", "long": 13.37247, "location": "Stattbad", "artists": [686904, 215812, 8505375, 562720, 5787, 50069, 82896, 1753561], "lat": 52.54346, "id": 20}, {"name": "Das House vom Nikolaus with Kris Wadsworth, Dinky, Kevin Reynolds, Leaves, Wittes", "long": 13.461, "location": "://about blank", "artists": [69412708, 298414, 201126, 2335014], "lat": 52.50383, "id": 21}, {"name": "Indoor Ipse Opening Day 1", "long": 13.452179, "location": "[ips\u0259]", "artists": [2821901, 20510324, 8180723, 273667, 1087216, 38825, 425492, 2806, 217097, 72453, 102022, 5302, 184155, 288837, 272, 58696, 460345, 358862, 1185772, 2884015], "lat": 52.49744, "id": 22}, {"name": "Get Perlonized!", "long": 13.4414345, "location": "Berghain/Panorama Bar", "artists": [2152541, 47988677, 11805917, 786, 968], "lat": 52.5110627, "id": 24}, {"name": "Behave Pres. Algo:Rhythm", "long": 13.43533, "location": "Bertrams by Loftus Hall", "artists": [81796165, 2347479], "lat": 52.49033, "id": 25}, {"name": "Cubeplus Night with Sucr\u00e9 Sal\u00e9", "long": 13.4543612, "location": "Suicide Circus", "artists": [714166, 6412641, 265565, 87654, 11654258, 342846], "lat": 52.5076327, "id": 28}, {"name": "Sol Asylum Showcase", "long": 13.4525442, "location": "Hoppetosse", "artists": [63290885, 335948, 1911211], "lat": 52.4970479, "id": 31}, {"name": "Some Kind Of Sign", "long": 13.445463, "location": "Watergate", "artists": [3803, 120571341, 833662], "lat": 52.500914, "id": 32}, {"name": "Liebe - Detail vs IRR", "long": 13.448507, "location": "Chalet", "artists": [2875, 35709, 421873, 312167, 59492943], "lat": 52.4976474, "id": 36}, {"name": "Renates Heimkinder /w. Gorge, Skai, Daniel Shepherd & More", "long": 13.46531, "location": "Salon Zur Wilden Renate", "artists": [96906, 89108, 201507, 6686558, 1373481, 2039198, 44683272, 852574, 272233, 4608669, 4972704, 13679434, 58500], "lat": 52.49744, "id": 38}, {"name": "Knutschen", "long": 13.4543612, "location": "spirograph.berlin", "artists": [6229348, 64796945, 7732714, 125174, 3297079], "lat": 52.5076327, "id": 42}, {"name": "Ritterstrasse Pres. Dogmatik Records", "long": 13.4078173, "location": "Ritter Butzke", "artists": [42018816, 667, 215810, 16306542], "lat": 52.5021746, "id": 44}, {"name": "The Unknown Clubnight", "long": 13.39314, "location": "Cosmic Kaspar", "artists": [86907032, 2603703, 3538322], "lat": 52.5408, "id": 48}, {"name": "District4 - DJ Emerson, Torsten Kanzler, Ixel", "long": 13.4525442, "location": "Arena Club", "artists": [795986, 1256, 3934466], "lat": 52.4970479, "id": 49}, {"name": "Quarant\u00e4ne", "long": 13.475708, "location": "Subland", "artists": [56323838, 70638237, 8237880], "lat": 52.507308, "id": 50}, {"name": "Friedlich Feiern", "long": 13.412215, "location": "M-Bia", "artists": [9177983, 246897], "lat": 52.5212924, "id": 51}, {"name": "-Closed-", "long": 13.4201002, "location": "Tresor", "artists": [], "lat": 52.5108799, "id": 52}];
data = data.slice(0,20);
 */

$(function($) {
    //console.log( "ready!" );
    //SC.initialize({client_id:'5b3cdaac22afb1d743aed0031918a90f'});
    $('div#info').css('top',$('#loadingOverlay').height()/2);

    $.getJSON('http://127.0.0.1:8000/ajax/13/05/2015/',function(data){
        console.log(data);
        sc = $('body').scplayer({ client_id:'5b3cdaac22afb1d743aed0031918a90f',control_container:$('#player'), map_container:$('body'), data:data.data, playlist_container:$('#playlist'), event_container:$('#event_display') });
    });


});

