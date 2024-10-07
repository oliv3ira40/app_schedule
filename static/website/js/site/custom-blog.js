$(function() {
	function Selector_Cache() {
		var collection = {};
	
		function get_from_cache( selector ) {
			if ( undefined === collection[ selector ] ) {
				collection[ selector ] = $( selector );
			}
	
			return collection[ selector ];
		}
	
		return { get: get_from_cache };
	}
	
	var selectors = new Selector_Cache();
	
	

	
	
	//Parallax fade on scroll	
	
	function scrollBanner() {
	  $(document).scroll(function(){
		var scrollPos = $(this).scrollTop();
		$('.parallax-fade-top').css({
		  'top' : (scrollPos/3)+'px',
		  'opacity' : 1-(scrollPos/350)
		});
	  });    
	}
	scrollBanner();	
	
	
	/* Scroll Animation */
	
	window.scrollReveal = new scrollReveal();
	
	
	jQuery(document).ready(function(){	
	
	
		//Fade on portfolio item hover
	
		$('#projects-grid').children().hover(function() {
		$(this).siblings().stop().fadeTo(400,0.2);
		}, function() {
			$(this).siblings().stop().fadeTo(400,1);
		});
	
		
		//Menu accordion
		
		var accordionsMenu = $('.cd-accordion-menu');
	
		if( accordionsMenu.length > 0 ) {
			
			accordionsMenu.each(function(){
				var accordion = $(this);
				//detect change in the input[type="checkbox"] value
				accordion.on('change', 'input[type="checkbox"]', function(){
					var checkbox = $(this);
					console.log(checkbox.prop('checked'));
					( checkbox.prop('checked') ) ? checkbox.siblings('ul').attr('style', 'display:none;').slideDown(300) : checkbox.siblings('ul').attr('style', 'display:block;').slideUp(300);
				});
			});
		}
	
		
		//Scroll back to top
	
		var offset = 300;
		var duration = 300;
		jQuery(window).scroll(function() {
			if (jQuery(this).scrollTop() > offset) {
				jQuery('.scroll-to-top').fadeIn(duration);
			} else {
				jQuery('.scroll-to-top').fadeOut(duration);
			}
		});
				
		jQuery('.scroll-to-top').on('click', function(event) {
			event.preventDefault();
			jQuery('html, body').animate({scrollTop: 0}, duration);
			return false;
		})
		
				
		//Tooltip
	
		$(".tipped").tipper();
		
		
		/* Video */
		
		$(".container").fitVids();
						
		$('.vimeo a,.youtube a').on('click', function (e) {
			e.preventDefault();
			var videoLink = $(this).attr('href');
			var classeV = $(this).parent();
			var PlaceV = $(this).parent();
			if ($(this).parent().hasClass('youtube')) {
				$(this).parent().wrapAll('<div class="video-wrapper">');
				$(PlaceV).html('<iframe frameborder="0" height="333" src="' + videoLink + '?autoplay=1&showinfo=0" title="YouTube video player" width="547"></iframe>');
			} else {
				$(this).parent().wrapAll('<div class="video-wrapper">');
				$(PlaceV).html('<iframe src="' + videoLink + '?title=0&amp;byline=0&amp;portrait=0&amp;autoplay=1&amp;color=6dc234" width="500" height="281" frameborder="0"></iframe>');
			}
		});	
		
	});
})
