/*
 * A custom player for clubmap
 * Given a set of artists it searches for their hottest tracks and constructs a playlist
 * 
 */
(function ($) {
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
			artists: [],
			playlist_container: this.element
	    },

		_create: function(){
			/*=================
			 * Private variables
			 * ================
			 */
	    	
	    	//a list with the current playlist based on artists
			this.playlist = [];
			//a list of html elements which represent the playlist ind the DOM
			this.playlist_el = []
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

			/*=================
			 * Constructor
			 * ================
			 */
			SC.initialize({client_id:this.options.client_id});
			var me = this;
            var user_tracks = [];
            var def = [];
            //search for best tracks for each user
	        jQuery.each(this.options.artists,function(index, id){
				var dfd = $.Deferred();
				//gets all tracks based on user id
				SC.get("/tracks", {user_id:id}, function(tracks){

					user_tracks = tracks;
					
					//sort all tracks
					user_tracks.sort(function(b,a){
						//sort tracks by score
						var scoreA = a.download_count + a.playback_count + 2 * a.favoritings_count;
						var scoreB = b.download_count + b.playback_count + 2 * b.favoritings_count;
						return scoreA - scoreB;
					});
					//merge lists faster
					$.merge(me.playlist,user_tracks.slice(0,3));
					dfd.resolve();
				});
				def.push(dfd.promise());
				
	        });
	        $.when.apply($, def).done(function(){
	        	me.createUI();
	        	me.waveform = new Waveform({
	        		container: $(me.progress)[0],	
	        		outerColor: "#000",
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
					  	return "rgba(0, 0, 0, 0.0)"
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
		previous:function(){
			var me = this;
			var next = me.current - 1;
			
            if(next < 0){
            	//wrap arround to end
            	next = me.playlist.length-1;
            }
            
            SC.stream("/tracks/"+me.playlist[next].id,{preferFlash:false, useHTML5Audio:true, whileloading:function(){me.loadingCallback()}, whileplaying:function(){me.updateTimeline();}, onfinish:function(){me.next();}}, function(sound){
            	if(me.current_sound != null) me.current_sound.destruct();
				me.current_sound = sound;
				me.current_sound.play();
				
				me.playlist_el[me.current].removeClass("active");
				
				me.current = next;
				
				me.playlist_el[next].addClass("active");
				me.updateWaveform();
				me.end.text(me.current_sound.durationEstimate);
			});
			
			
		},
		/*
		 * ========
		 * Goes to next track in playlist
		 * This method is called at the end of each track automatically
		 * ========
		 */
		next:function(){
			var me = this;
			var next = me.current + 1;
			
            if(next >= me.playlist.length){
            	//wrap arround to beginning
            	next = 0;
            }
            
            SC.stream("/tracks/"+me.playlist[next].id,{preferFlash:false, useHTML5Audio:true, whileloading:function(){me.loadingCallback()}, whileplaying:function(){me.updateTimeline();}, onfinish:function(){me.next();}}, function(sound){
            	if(me.current_sound != null) me.current_sound.destruct();
				me.current_sound = sound;
				me.current_sound.play();
				
				me.playlist_el[me.current].removeClass("active");
				
				me.current = next;
				
				me.playlist_el[next].addClass("active");
				me.updateWaveform();
				me.end.text(me.current_sound.durationEstimate);
			});
			
			
		},
		
		goTo:function(index){
			var me = this;
			
            if(index < me.playlist.length && index >= 0){
	            //index is in boundaries
            	SC.stream("/tracks/"+me.playlist[index].id,{preferFlash:false, useHTML5Audio:true, whileloading:function(){me.loadingCallback()}, whileplaying:function(){me.updateTimeline();}, onfinish:function(){me.next();}}, function(sound){
            		if(me.current_sound != null) me.current_sound.destruct();
            		
					me.current_sound = sound;
					me.current_sound.play();
					
					me.playlist_el[me.current].removeClass("active");
					
					me.current = index;

					me.playlist_el[index].addClass("active");
					me.updateWaveform();
					me.end.text(me.current_sound.durationEstimate);
				});
			
			} else {
				console.log("ERROR: track index is out of bounds "+index);
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
            console.log(me.playlist);
            if (me.current_sound === null) {
				//nothin is playing so when stream is ready play new sound
				SC.stream("/tracks/"+me.playlist[me.current].id,{preferFlash:false, useHTML5Audio:true, whileloading:function(){me.loadingCallback()}, whileplaying:function(){me.updateTimeline();}, onfinish:function(){me.next();}} , function(sound){
					me.current_sound = sound	
					me.current_sound.play();
					me.playing = true;
				});
				me.playlist_el[me.current].addClass("active");
				me.updateWaveform();
				me.end.text(me.current_sound.durationEstimate);
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
			me.waveform.dataFromSoundCloudTrack(me.playlist[me.current]);
			/*
			me.progress.css("width",0);
			var path = me.playlist[me.current].waveform_url;
			me.waveform.attr("src",path);*/
			
		},
		
		/*
		 * =======
		 * Creates the user interface
		 * =======
		 */
		createUI: function(){
			var me = this;
			var el = this.element;
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
			
			var position = $('<div></div>', {
				class:'cm_player position'
			}).appendTo(me.timeline);
			
			me.end = $('<div></div>', {
				class:'cm_player end'
			}).appendTo(me.timeline);
			
			var playlist_wrapper = $('<div></div>', {
				class:'cm_player playlist'
			});
			
			var playlist_ul = $('<ul></ul>', {
				class:'cm_player playlist'
			}).appendTo(playlist_wrapper);
			
			jQuery.each(me.playlist ,function(index, track){
				var li = $('<li><span class = "cm_player index">' + (index+1) + '</span> <span class="cm_player title">'+ track.title +'</span> <span class="cm_player artist">' + track.user.username + '</span></li>').appendTo(playlist_ul);
				li.click(function(){ 
					me.goTo(index); 
					//li.addClass("active");
					});
				me.playlist_el.push(li);		
			});
			
			ctrl.appendTo(el);
			playlist_wrapper.appendTo(el);
		}
		

	});
}(jQuery));

$(function($) {
    //console.log( "ready!" );
    //SC.initialize({client_id:'5b3cdaac22afb1d743aed0031918a90f'});
    sc = $('#alan').scplayer({client_id:'5b3cdaac22afb1d743aed0031918a90f',artists:[103,56714706,57700009,10258324, 6412641, 2795935, 57700009, 99991115, 2152541]});
    SC.whenStreamingReady(function(){
    	//build interface
    	console.log("ready to stream");
    });
});