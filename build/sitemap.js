const {load,ROOT}=require('./load.js');
const fs=require('fs'),path=require('path');
const W=load(),S=W.EKGURU_SITE,M=W.EKGURU_MARKETS,T=W.EKGURU_TUTORS;
const BASE=S.baseUrl.replace(/\/?$/,'/'),today=new Date().toISOString().slice(0,10);
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const LANGPAGES=['index.html','find-tutors.html','join.html'];

function imagesFor(p){
  const out=[];
  const m=/tutor\/([a-z0-9-]+)\//.exec(p)||/id=([a-z0-9-]+)/.exec(p);
  if(m){
    const t=T.find(x=>x.id===m[1]);
    if(t){
      out.push([BASE+t.photo,t.name+' — online Hindi tutor',t.name]);
      if(t.banner) out.push([BASE+t.banner,t.name+' — '+t.headline,t.name+' banner']);
    }
  }else{
    out.push([BASE+'images/og-cover.jpg','EkGuru — learn Hindi online with a personal Guru','EkGuru']);
    T.forEach(t=>out.push([BASE+t.photo,t.name+' — online Hindi tutor',t.name]));
  }
  return out;
}

const pages=[
  ['','1.0','daily',true],
  ['find-tutors.html','0.9','weekly',true],
  ['join.html','0.7','monthly',true],
  ['tutor/','0.6','weekly',false]
];
/* Only the pre-rendered page is listed. The interactive tutor.html?id=
   shows the same tutor but is nearly empty without JavaScript, and it now
   declares tutor/<id>/ as its canonical — so submitting both would ask
   Google to choose between duplicates. We submit the strong one. */
T.forEach(t=>{
  pages.push(['tutor/'+t.id+'/','0.9','weekly',false]);
});

let o=['<?xml version="1.0" encoding="UTF-8"?>',
'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">'];

for(const [p,prio,freq,hl] of pages){
  const loc=esc(BASE+p),sep=p.includes('?')?'&amp;':'?';
  o.push('  <url>','    <loc>'+loc+'</loc>');
  if(hl){
    const file=p.includes('?')?p:(p===''?'':p);
    M.forEach(m=>{
      const href = (['','find-tutors.html','join.html'].includes(p) && m.code!=='en')
        ? esc(BASE+m.code+'/'+(p===''?'':p))
        : loc+sep+'lang='+m.code;
      o.push(`    <xhtml:link rel="alternate" hreflang="${m.locale}" href="${href}"/>`);
    });
    o.push(`    <xhtml:link rel="alternate" hreflang="x-default" href="${loc}"/>`);
  }
  imagesFor(p).forEach(([l,c,t2])=>o.push('    <image:image>',
    '      <image:loc>'+esc(l)+'</image:loc>',
    '      <image:caption>'+esc(c)+'</image:caption>',
    '      <image:title>'+esc(t2)+'</image:title>','    </image:image>'));
  o.push(`    <lastmod>${today}</lastmod>`,`    <changefreq>${freq}</changefreq>`,`    <priority>${prio}</priority>`,'  </url>');
}

for(const m of M.filter(x=>x.code!=='en')){
  for(const f of LANGPAGES){
    const rel=m.code+'/'+(f==='index.html'?'':f), loc=esc(BASE+rel);
    o.push('  <url>','    <loc>'+loc+'</loc>');
    o.push(`    <xhtml:link rel="alternate" hreflang="en" href="${esc(BASE+(f==='index.html'?'':f))}"/>`);
    M.filter(x=>x.code!=='en').forEach(m2=>
      o.push(`    <xhtml:link rel="alternate" hreflang="${m2.locale}" href="${esc(BASE+m2.code+'/'+(f==='index.html'?'':f))}"/>`));
    o.push(`    <xhtml:link rel="alternate" hreflang="x-default" href="${esc(BASE+(f==='index.html'?'':f))}"/>`);
    imagesFor(rel).forEach(([l,c,t2])=>o.push('    <image:image>',
      '      <image:loc>'+esc(l)+'</image:loc>',
      '      <image:caption>'+esc(c)+'</image:caption>',
      '      <image:title>'+esc(t2)+'</image:title>','    </image:image>'));
    o.push('    <lastmod>'+today+'</lastmod>','    <changefreq>weekly</changefreq>','    <priority>0.8</priority>','  </url>');
  }
}
o.push('</urlset>');
fs.writeFileSync(path.join(ROOT,'sitemap.xml'),o.join('\n'));
console.log('sitemap:',pages.length+ (M.length-1)*3,'URLs');
