!function(e,i,s,t){"use strict";function o(i,s){this.options=e.extend({},r,i),this.init()}var n="heroFaderGallery",r={$target:null,intervalInitial:5e3,intervalNext:7e3,heroImages:[]};o.prototype={init:function(){this.$heroSlides=this.options.$target.find(".js-hero-slide"),this.$heroSlideDesc=this.options.$target.find(".js-hero-slide-desc"),this.slidePos=0,this.i=0,this.faderTimer="",this.isPlaying=!0,this.preloadHeroImages()},preloadHeroImages:function(){var i=this,s=[];e.each(i.options.heroImages,function(e,i){s.push(i.url)});var t=function(s){e.each(s,function(e,s){i.options.heroImages[e].image=s}),i.startFader()};Fiverr._deferredLoadImages(s,t)},showNextSlide:function(){var e=this;_.delay(function(){e.options.heroImages[e.i]||(e.i=0),e.slidePos^=1;var i=e.$heroSlides.eq(e.slidePos),s=e.$heroSlideDesc.eq(e.slidePos);i.find("img").attr("src",e.options.heroImages[e.i].image.src),i.css({"background-image":"url("+e.options.heroImages[e.i].image.src+")"}),s.length&&(s.find("small").attr("class",e.options.heroImages[e.i].iconClass).html(e.options.heroImages[e.i].heroDesc||""),s.find("p").html(e.options.heroImages[e.i].heroDescSub||"")),_.delay(function(){e.$heroSlides.toggleClass("sel"),e.$heroSlideDesc.length&&(e.$heroSlideDesc.toggleClass("sel").addClass("pos-fixed"),_.delay(function(){e.$heroSlideDesc.removeClass("pos-fixed")},1e3))},100)},1e3),e.i++},startFader:function(){var e=this;_.delay(function(){e.showNextSlide(),e.faderTimer=setInterval(function(){e.isPlaying&&e.showNextSlide()},e.options.intervalNext)},e.options.intervalInitial)},pauseFader:function(){this.isPlaying=!1},unpauseFader:function(){this.isPlaying=!0},stopFader:function(){clearInterval(this.faderTimer)},getImages:function(){return this.options.heroImages},getCurrentImage:function(){return this.options.heroImages[this.i]}},e.fn[n]=function(i){var s,t=Array.prototype.slice.call(arguments,1);return this.each(function(){var r=e.data(this,"plugin_"+n);r?"string"==typeof i&&(s=r[i].apply(r,t)):e.data(this,"plugin_"+n,new o(this,i))}),s?s:this},i.fHeroFader=o}(jQuery,window,document);