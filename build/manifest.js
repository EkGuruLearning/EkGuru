const {load,ROOT}=require('./load.js');
const fs=require('fs'),path=require('path');
const W=load(),S=W.EKGURU_SITE,T=W.EKGURU_TUTORS;
const m={
  id:"/EkGuru/",
  name:"EkGuru — Learn Hindi Online with a Personal Guru",
  short_name:"EkGuru",
  description:"Private one-to-one online Hindi lessons with verified native tutors. Speak, read and write Hindi with confidence.",
  start_url:"./index.html?utm_source=pwa", scope:"./",
  display:"standalone", display_override:["window-controls-overlay","standalone","browser"],
  orientation:"any", background_color:"#ffffff", theme_color:"#5b3df5",
  lang:"en", dir:"ltr", categories:["education","languages","productivity"],
  prefer_related_applications:false,
  icons:[
    {src:"images/logo.svg",sizes:"any",type:"image/svg+xml",purpose:"any"},
    {src:"images/icon-192.png",sizes:"192x192",type:"image/png",purpose:"any"},
    {src:"images/icon-192.png",sizes:"192x192",type:"image/png",purpose:"maskable"},
    {src:"images/icon-512.png",sizes:"512x512",type:"image/png",purpose:"any"},
    {src:"images/icon-512.png",sizes:"512x512",type:"image/png",purpose:"maskable"}],
  screenshots:[{src:"images/og-cover.jpg",sizes:"1200x630",type:"image/jpeg",form_factor:"wide",label:"EkGuru home page"}],
  shortcuts:[
    {name:"Find a tutor",short_name:"Tutors",description:"Search verified Hindi tutors",
     url:"./find-tutors.html?utm_source=pwa_shortcut",icons:[{src:"images/icon-192.png",sizes:"192x192"}]},
    {name:"Become a tutor",short_name:"Teach",description:"Apply to teach Hindi on EkGuru",
     url:"./join.html?utm_source=pwa_shortcut",icons:[{src:"images/icon-192.png",sizes:"192x192"}]}
  ].concat(T.slice(0,2).map(t=>({name:"Book with "+t.name,short_name:t.name.split(" ")[0],
     description:t.headline,url:"./tutor.html?id="+encodeURIComponent(t.id)+"&utm_source=pwa_shortcut",
     icons:[{src:"images/icon-192.png",sizes:"192x192"}]}))),
  related_applications:[], launch_handler:{client_mode:"navigate-existing"}
};
fs.writeFileSync(path.join(ROOT,'manifest.webmanifest'),JSON.stringify(m,null,2));
console.log('manifest ✓',m.shortcuts.length,'shortcuts');
