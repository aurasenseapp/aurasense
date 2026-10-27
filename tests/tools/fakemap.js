/* Test-only: a stand-in for the map library, so the rest of Aurasense's interface can be walked in a browser that
   cannot reach Mapbox. Every map call is accepted and does nothing; 'load' and 'style.load' fire once. Never shipped. */
(function(){
  try{ localStorage.setItem('as_key','KHtest'); }catch(e){}
  var num={getZoom:3,getPitch:0,getBearing:0,getMaxZoom:22,getMinZoom:0};
  function P(name){
    var f=function(){};
    return new Proxy(f,{
      get:function(t,p){
        if(p===Symbol.toPrimitive) return function(){ return 0; };
        if(p==='then') return undefined;
        if(p==='toString'||p==='valueOf') return function(){ return 0; };
        if(p==='length') return 0;
        if(p==='lng'||p==='lat'||p==='x'||p==='y') return 0;
        return P(String(p));
      },
      apply:function(){ return P(name+'()'); },
      construct:function(){ return P('new '+name); }
    });
  }
  function FakeMap(opts){
    var self=this, ev={};
    this._ev=ev; this._c=(opts&&opts.container)||null;
    this.on=function(n,a,b){ var cb=typeof a==='function'?a:b; (ev[n]=ev[n]||[]).push(cb);
      if(n==='load'||n==='style.load'||n==='idle'){ setTimeout(function(){ try{ cb.call(self,{target:self}); }catch(e){ console.warn('fake load cb', e&&e.message); } }, 50); }
      return self; };
    this.once=this.on; this.off=function(){ return self; };
    this.getCenter=function(){ return {lng:-114.47,lat:51.19,wrap:function(){return this;},toArray:function(){return [-114.47,51.19];}}; };
    this.getBounds=function(){ return {getNorth:function(){return 52;},getSouth:function(){return 50;},getEast:function(){return -113;},getWest:function(){return -116;},contains:function(){return true;},toArray:function(){return [[-116,50],[-113,52]];}}; };
    this.project=function(){ return {x:195,y:400}; };
    this.unproject=function(){ return {lng:-114.47,lat:51.19}; };
    this.getCanvas=function(){ var c=document.createElement('canvas'); return c; };
    this.getCanvasContainer=function(){ return document.body; };
    this.getContainer=function(){ return typeof self._c==='string'?document.getElementById(self._c):self._c||document.body; };
    this.getSource=function(){ return P('source'); };
    this.getLayer=function(){ return null; };
    this.getStyle=function(){ return {layers:[],sources:{}}; };
    this.isStyleLoaded=function(){ return true; }; this.loaded=function(){ return true; };
    this.queryRenderedFeatures=function(){ return []; }; this.querySourceFeatures=function(){ return []; };
    Object.keys(num).forEach(function(k){ self[k]=function(){ return num[k]; }; });
    return new Proxy(this,{ get:function(t,p){ if(p in t) return t[p]; return function(){ return t; }; } });
  }
  function Marker(){ var el=document.createElement('div'); var m=this;
    this.setLngLat=function(){ return m; }; this.addTo=function(){ return m; }; this.remove=function(){ return m; };
    this.getElement=function(){ return el; }; this.setPopup=function(){ return m; }; this.getLngLat=function(){ return {lng:0,lat:0}; };
    return new Proxy(this,{ get:function(t,p){ if(p in t) return t[p]; return function(){ return t; }; } }); }
  function Popup(){ var m=this; return new Proxy(this,{ get:function(t,p){ return function(){ return m; }; } }); }
  window.mapboxgl={Map:FakeMap, Marker:Marker, Popup:Popup, LngLat:function(a,b){ this.lng=a; this.lat=b; }, LngLatBounds:function(){ return P('bounds'); },
    NavigationControl:function(){}, GeolocateControl:function(){ return P('geo'); }, AttributionControl:function(){}, ScaleControl:function(){},
    supported:function(){ return true; }, accessToken:'', setRTLTextPlugin:function(){}, getRTLTextPluginStatus:function(){ return 'loaded'; }, prewarm:function(){} };
})();
