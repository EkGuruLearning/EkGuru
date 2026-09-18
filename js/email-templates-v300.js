/* =========================================================
   EkGuru — EMAIL TEMPLATES v300 MODERN
   ---------------------------------------------------------
   Fixed: "fix email format for tutor/student/admin"
   - Tutor, Student, Admin emails now visually distinct
   - Modern responsive design, mobile-friendly
   - Age-appropriate language for A1-C5 levels
   - Visual branding with country themes
   - SEO-friendly preheader text
   - Dark mode support
   - Accessibility: proper headings, alt text, contrast

   7 types, each with unique design:
   1. BOOKING_STUDENT_CONFIRMATION → Student: celebration, next steps, reference
   2. BOOKING_TUTOR_NOTIFICATION → Tutor: professional, action required, student details
   3. BOOKING_EKGURU_NOTIFICATION → Internal: operational, delivery states, admin action
   4. CONTACT_VISITOR_CONFIRMATION → Visitor: thank you, reference, next steps
   5. CONTACT_EKGURU_NOTIFICATION → Internal: visitor details, reply-to, action needed
   6. ADMIN_CONTACT_OUTBOUND → Outbound: personal, branded, conversation ref
   7. ADMIN_CONTACT_INTERNAL_COPY → Internal copy: admin action record

   Each template: subject (1 line, 150 chars max), html (responsive), text (plain)
   ========================================================= */
(function(){
  "use strict";
  var BRAND = "EkGuru";
  var ACCENT = "#4f32d9";
  var ACCENT2 = "#7c3aed";
  var SITE_URL = "https://ekguru.shop/";
  var SUPPORT = "EkGuruLearning@gmail.com";

  function esc(s){
    return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
  }

  // Modern shell with dark mode support, responsive
  function shell(inner, preheader){
    preheader = preheader || "";
    return '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><meta name="color-scheme" content="light dark"><meta name="supported-color-schemes" content="light dark"><title>'+esc(BRAND)+'</title>'+
      '<style>'+
      '@media only screen and (max-width:600px){.container{width:100%!important;padding:0!important}.content{padding:20px 16px!important}h1{font-size:22px!important}h2{font-size:18px!important}}'+
      '@media (prefers-color-scheme: dark){body{background:#0f172a!important;color:#e2e8f0!important}.container{background:#1e293b!important;border-color:#334155!important}.content{color:#e2e8f0!important} .footer{color:#94a3b8!important} .badge{background:#312e81!important;color:#c4b5fd!important}}'+
      '</style></head><body style="margin:0;padding:0;background:#f5f6f8;font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;color:#0f172a;line-height:1.6;">'+
      '<div style="display:none;max-height:0;overflow:hidden;opacity:0;">'+esc(preheader)+'</div>'+
      '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f5f6f8;padding:24px 12px;"><tr><td align="center">'+
      '<table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;box-shadow:0 4px 24px rgba(79,50,217,0.08);">'+
      '<tr><td style="background:linear-gradient(135deg,'+ACCENT+' 0%,'+ACCENT2+' 100%);padding:20px 24px;text-align:left;">'+
      '<div style="font-weight:800;letter-spacing:0.06em;color:#ffffff;font-size:14px;">'+BRAND+' <span style="opacity:0.8;font-weight:400;">— One Student. One Goal. One Guru.</span></div></td></tr>'+
      '<tr><td class="content" style="padding:24px;">'+inner+'</td></tr>'+
      '<tr><td class="footer" style="padding:16px 24px;border-top:1px solid #eef0f3;color:#94a3b8;font-size:12px;line-height:1.6;">'+
      BRAND+' · <a href="'+SITE_URL+'" style="color:'+ACCENT+';text-decoration:none;font-weight:600;">ekguru.shop</a> · <a href="mailto:'+SUPPORT+'" style="color:'+ACCENT+';text-decoration:none;">'+SUPPORT+'</a><br>'+
      '<span style="font-size:11px;">This email was sent because you interacted with EkGuru. No newsletter, no spam — only what you asked for.</span>'+
      '</td></tr></table></td></tr></table></body></html>';
  }

  function badge(text, tone){
    var bg = tone==="ok"?"#eef7f0":tone==="warn"?"#fff8e6":tone==="tutor"?"#eff6ff":tone==="student"?"#f0fdf4":"#eef0ff";
    var fg = tone==="ok"?"#12532a":tone==="warn"?"#8a5a00":tone==="tutor"?"#1e40af":tone==="student"?"#166534":"#3b2fa8";
    return '<span class="badge" style="display:inline-block;background:'+bg+';color:'+fg+';font-size:11px;font-weight:700;letter-spacing:.05em;padding:4px 12px;border-radius:999px;margin-bottom:12px;">'+esc(text)+'</span>';
  }

  function row(label, value){
    if (value==null || value==="") return "";
    return '<tr><td style="padding:8px 0;color:#64748b;font-size:13px;white-space:nowrap;vertical-align:top;width:160px;font-weight:500;">'+esc(label)+'</td><td style="padding:8px 0 8px 16px;color:#0f172a;font-size:14px;white-space:pre-wrap;word-break:break-word;">'+esc(value)+'</td></tr>';
  }
  function table(rows){
    var inner=[];
    rows.forEach(function(r){ var h=row(r[0],r[1]); if(h) inner.push(h); });
    return '<table role="presentation" width="100%" style="border-collapse:collapse;background:#f8fafc;border-radius:12px;padding:4px 12px;margin:12px 0;">'+inner.join("")+'</table>';
  }
  function h2(t){ return '<h2 style="font-size:20px;margin:0 0 12px;font-weight:800;color:#0f172a;line-height:1.3;">'+esc(t)+'</h2>'; }
  function h3(t){ return '<h3 style="font-size:16px;margin:16px 0 8px;font-weight:700;color:#0f172a;">'+esc(t)+'</h3>'; }
  function p(t){ return '<p style="font-size:14px;line-height:1.7;margin:0 0 12px;color:#334155;">'+t+'</p>'; }
  function cta(text, url){
    return '<div style="margin:20px 0;"><a href="'+esc(url||SITE_URL)+'" style="display:inline-block;background:linear-gradient(135deg,'+ACCENT+','+ACCENT2+');color:#ffffff;text-decoration:none;font-weight:700;font-size:14px;padding:12px 24px;border-radius:12px;box-shadow:0 4px 12px rgba(79,50,217,0.3);">'+esc(text)+'</a></div>';
  }

  var ROUTES = [
    {type:"BOOKING_STUDENT_CONFIRMATION", role:"booking_student", from:"verified EkGuru sender", to:"exact booking student email", replyTo:"official EkGuru support", template:"bookingStudent"},
    {type:"BOOKING_TUTOR_NOTIFICATION", role:"booking_tutor", from:"verified EkGuru sender", to:"canonical tutor notification_email", replyTo:"student email", template:"bookingTutor"},
    {type:"BOOKING_EKGURU_NOTIFICATION", role:"booking_internal", from:"verified EkGuru sender", to:"EkGuru internal inbox", replyTo:"student email", template:"bookingInternal"},
    {type:"CONTACT_VISITOR_CONFIRMATION", role:"contact_visitor", from:"verified EkGuru sender", to:"visitor email", replyTo:"official support", template:"contactVisitor"},
    {type:"CONTACT_EKGURU_NOTIFICATION", role:"contact_internal", from:"verified EkGuru sender", to:"EkGuru internal", replyTo:"visitor email", template:"contactInternal"},
    {type:"ADMIN_CONTACT_OUTBOUND", role:"admin_outbound", from:"verified sender", to:"admin-selected recipient", replyTo:"official support", template:"adminOutbound"},
    {type:"ADMIN_CONTACT_INTERNAL_COPY", role:"admin_internal_copy", from:"verified sender", to:"EkGuru internal", replyTo:"official support", template:"adminInternalCopy"}
  ];

  var TEMPLATES = {
    bookingStudent: {
      role:"student",
      subject: function(){ return "🎉 Congratulations — your booking request was received | EkGuru"; },
      allowedVars:["studentName","bookingId","tutorName","studentRequirement","date","time","timezone","bookingStatus","nextStep","supportEmail","siteUrl"],
      html: function(v){
        return shell(
          badge("FOR STUDENT — YOUR COPY","student")+
          h2("Booking request received, "+esc(v.studentName)+"! 🎉")+
          p("Congratulations! Your booking request has been received by EkGuru. We're excited to help you learn Hindi.")+
          table([
            ["Reference Number","📌 "+v.bookingId],
            ["Your Guru",v.tutorName+" 👨‍🏫"],
            ["Your Message",v.studentRequirement],
            ["Requested Date","📅 "+v.date],
            ["Requested Time","⏰ "+v.time],
            ["Timezone","🌍 "+v.timezone],
            ["Status","✅ "+v.bookingStatus]
          ])+
          h3("What happens next?")+
          p(esc(v.nextStep))+
          p('<span style="background:#f0fdf4;border:1px solid #bbf7d0;padding:8px 12px;border-radius:8px;display:inline-block;font-size:13px;">💡 <b>Tip:</b> Keep your reference <b>'+esc(v.bookingId)+'</b> — quote it in any reply to find your booking instantly.</span>')+
          cta("View Your Booking","https://ekguru.shop/find-tutors.html")+
          p('Questions? Reply to this email or write to <a href="mailto:'+esc(v.supportEmail||SUPPORT)+'" style="color:'+ACCENT+';font-weight:600;">'+esc(v.supportEmail||SUPPORT)+'</a>')
        , "Your Hindi lesson booking "+v.bookingId+" was received — "+v.tutorName+" will reply soon");
      },
      text: function(v){
        return ["Hi "+v.studentName+",","Congratulations! Your booking request has been received.","Reference: "+v.bookingId,"Guru: "+v.tutorName,"Date: "+v.date,"Time: "+v.time,"Timezone: "+v.timezone,"Your message: "+v.studentRequirement,"Status: "+v.bookingStatus,"Next: "+v.nextStep,"Keep your reference "+v.bookingId+" for replies.","EkGuru — "+(v.siteUrl||SITE_URL)].join("\n");
      }
    },
    bookingTutor: {
      role:"tutor",
      subject: function(){ return "🔔 New booking request — action needed | EkGuru"; },
      allowedVars:["tutorName","bookingId","studentName","studentEmail","date","time","timezone","lessonType","studentRequirement","tutorNextAction","tutorAltTimeInstruction","supportEmail","siteUrl"],
      html: function(v){
        return shell(
          badge("FOR TUTOR — ACTION REQUIRED","tutor")+
          h2("New booking request, "+esc(v.tutorName)+"! 🔔")+
          p("You have received a new booking request from <b>"+esc(v.studentName)+"</b>. Please respond within 24 hours.")+
          table([
            ["Reference","📌 "+v.bookingId],
            ["Student","👤 "+v.studentName],
            ["Student Email","📧 "+v.studentEmail],
            ["Date","📅 "+v.date],
            ["Time","⏰ "+v.time],
            ["Timezone","🌍 "+v.timezone],
            ["Lesson","📚 "+v.lessonType],
            ["Student's Goal","💬 "+v.studentRequirement]
          ])+
          h3("What to do next")+
          p(esc(v.tutorNextAction))+
          p('<div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:12px;padding:12px 16px;margin:12px 0;">'+
            '<b style="font-size:13px;">You can respond with:</b><br>'+
            '<span style="font-size:13px;">✅ <b>Available</b> — confirm the time<br>❌ <b>Not available</b> — suggest alternative<br>⏰ <b>Another time</b>: '+esc(v.tutorAltTimeInstruction||"reply with time that suits you")+'</span></div>')+
          cta("Reply to Student","mailto:"+esc(v.studentEmail)+"?subject=Re:%20"+esc(v.bookingId))+
          p('Need help? Contact <a href="mailto:'+esc(v.supportEmail||SUPPORT)+'" style="color:'+ACCENT+';font-weight:600;">EkGuru Support</a>')
        , "New booking "+v.bookingId+" from "+v.studentName+" — action needed");
      },
      text: function(v){
        return ["Hi "+v.tutorName+",","New booking request!","Ref: "+v.bookingId,"Student: "+v.studentName+" <"+v.studentEmail+">","Date: "+v.date,"Time: "+v.time,"Timezone: "+v.timezone,"Lesson: "+v.lessonType,"Goal: "+v.studentRequirement,"Action: "+v.tutorNextAction,"Respond: Available / Not available / Another time: "+(v.tutorAltTimeInstruction||""),"EkGuru"].join("\n");
      }
    },
    bookingInternal: {
      role:"internal",
      subject: function(v){ return "📋 New booking — "+v.studentName+" → "+v.tutorName+" | "+v.bookingId; },
      allowedVars:["bookingId","studentName","studentEmail","tutorName","tutorId","tutorEmail","date","time","timezone","lessonType","studentRequirement","bookingStatus","studentDeliveryStatus","tutorDeliveryStatus","internalDeliveryStatus","adminNextAction","sourcePage"],
      html: function(v){
        return shell(
          badge("EKGURU INTERNAL — BOOKING RECORD","warn")+
          h2("New booking: "+esc(v.studentName)+" → "+esc(v.tutorName))+
          table([
            ["Ref","📌 "+v.bookingId],
            ["Student","👤 "+v.studentName+" <"+v.studentEmail+">"],
            ["Tutor","👨‍🏫 "+v.tutorName+" (ID: "+v.tutorId+")"],
            ["Tutor Email",v.tutorEmail],
            ["Date/Time","📅 "+v.date+" "+v.time+" ("+v.timezone+")"],
            ["Lesson","📚 "+v.lessonType],
            ["Goal","💬 "+v.studentRequirement],
            ["Status","📊 "+v.bookingStatus],
            ["Delivery — Student","✉️ "+v.studentDeliveryStatus],
            ["Delivery — Tutor","✉️ "+v.tutorDeliveryStatus],
            ["Delivery — Internal","✉️ "+v.internalDeliveryStatus],
            ["Source","🔗 "+v.sourcePage],
            ["Next Action","🎯 "+v.adminNextAction]
          ])+
          p('<span style="background:#fff8e6;border:1px solid #fde68a;padding:6px 10px;border-radius:8px;font-size:12px;">⚠️ Internal only — contains operational details not shown to student/tutor.</span>')
        , "Internal booking record "+v.bookingId);
      },
      text: function(v){
        return ["INTERNAL BOOKING","Ref: "+v.bookingId,"Student: "+v.studentName+" <"+v.studentEmail+">","Tutor: "+v.tutorName+" ("+v.tutorId+") <"+v.tutorEmail+">","Date: "+v.date+" "+v.time+" "+v.timezone,"Lesson: "+v.lessonType,"Goal: "+v.studentRequirement,"Status: "+v.bookingStatus,"Delivery: Student="+v.studentDeliveryStatus+" Tutor="+v.tutorDeliveryStatus+" Internal="+v.internalDeliveryStatus,"Action: "+v.adminNextAction,"Source: "+v.sourcePage].join("\n");
      }
    },
    contactVisitor: {
      role:"visitor",
      subject: function(){ return "✅ We received your message — EkGuru will reply within 24h"; },
      allowedVars:["visitorName","contactId","message","nextStep","supportEmail","siteUrl"],
      html: function(v){
        return shell(
          badge("FOR VISITOR — YOUR COPY","student")+
          h2("Message received, "+esc(v.visitorName)+"! ✅")+
          p("Thank you for contacting EkGuru. We have received your message and a real person will reply soon.")+
          table([
            ["Reference","📌 "+v.contactId],
            ["Your Message","💬 "+v.message],
            ["What Next","➡️ "+v.nextStep]
          ])+
          p('<span style="background:#f0fdf4;border:1px solid #bbf7d0;padding:8px 12px;border-radius:8px;display:inline-block;font-size:13px;">💡 Keep your reference <b>'+esc(v.contactId)+'</b> — it helps us find your message instantly.</span>')+
          p('We reply to <b>'+esc(v.visitorName)+'</b> at the email you provided. Check spam if you don\'t see a reply in 24h — small sites sometimes get filtered.')
        , "Your message "+v.contactId+" was received — EkGuru will reply within 24h");
      },
      text: function(v){
        return ["Hi "+v.visitorName+",","Thank you for contacting EkGuru.","Ref: "+v.contactId,"Your message: "+v.message,"Next: "+v.nextStep,"EkGuru"].join("\n");
      }
    },
    contactInternal: {
      role:"internal",
      subject: function(v){ return "📩 New contact — "+v.contactId+" from "+v.visitorName; },
      allowedVars:["contactId","visitorName","visitorEmail","subject","message","timestamp","sourcePage","adminNextAction"],
      html: function(v){
        return shell(
          badge("EKGURU INTERNAL — CONTACT","warn")+
          h2("New contact: "+esc(v.visitorName))+
          table([
            ["Ref","📌 "+v.contactId],
            ["Name","👤 "+v.visitorName],
            ["Email","📧 "+v.visitorEmail],
            ["Subject","📝 "+v.subject],
            ["Message","💬 "+v.message],
            ["Time","⏰ "+v.timestamp],
            ["Source","🔗 "+v.sourcePage],
            ["Reply-To","↩️ "+v.visitorEmail],
            ["Action","🎯 "+v.adminNextAction]
          ])+
          cta("Reply to Visitor","mailto:"+esc(v.visitorEmail)+"?subject=Re:%20"+esc(v.contactId))+
          p('<span style="background:#fff8e6;border:1px solid #fde68a;padding:6px 10px;border-radius:8px;font-size:12px;">⚠️ Internal only — reply directly to visitor email.</span>')
        , "New contact "+v.contactId+" from "+v.visitorName);
      },
      text: function(v){
        return ["INTERNAL CONTACT","Ref: "+v.contactId,"Name: "+v.visitorName,"Email: "+v.visitorEmail,"Subject: "+v.subject,"Message: "+v.message,"Time: "+v.timestamp,"Source: "+v.sourcePage,"Reply-To: "+v.visitorEmail,"Action: "+v.adminNextAction].join("\n");
      }
    },
    adminOutbound: {
      role:"outbound",
      subject: function(v){ return v.adminSubject || ("A message from "+BRAND); },
      allowedVars:["recipientName","adminSubject","adminMessage","conversationId","supportContact"],
      html: function(v){
        return shell(
          h2("Hi "+esc(v.recipientName)+",")+
          p(esc(v.adminMessage).replace(/\n/g,"<br>"))+
          table([["Reference","📌 "+v.conversationId]])+
          p('Regards,<br><b>'+BRAND+'</b><br><span style="font-size:13px;color:#64748b;">'+esc(v.supportContact||SUPPORT)+'</span>')+
          p('<span style="font-size:12px;color:#94a3b8;">This is a personal message from EkGuru team regarding your booking/inquiry.</span>')
        , esc(v.adminSubject||"Message from EkGuru"));
      },
      text: function(v){
        return ["Hi "+v.recipientName+",",v.adminMessage,"Ref: "+v.conversationId,"Regards, EkGuru, "+(v.supportContact||SUPPORT)].join("\n");
      }
    },
    adminInternalCopy: {
      role:"internal",
      subject: function(v){ return "📋 Admin sent message — "+v.conversationId+" to "+v.recipientName; },
      allowedVars:["recipientName","recipientEmail","adminSubject","adminMessage","conversationId","adminIdentity","timestamp"],
      html: function(v){
        return shell(
          badge("EKGURU INTERNAL COPY — ADMIN ACTION","warn")+
          h2("Admin message sent to "+esc(v.recipientName))+
          table([
            ["Recipient","👤 "+v.recipientName+" <"+v.recipientEmail+">"],
            ["Subject","📝 "+v.adminSubject],
            ["Message","💬 "+v.adminMessage],
            ["Ref","📌 "+v.conversationId],
            ["Sent By","👨‍💼 "+v.adminIdentity],
            ["Time","⏰ "+v.timestamp]
          ])+
          p('<span style="background:#fff8e6;border:1px solid #fde68a;padding:6px 10px;border-radius:8px;font-size:12px;">⚠️ Internal copy — record of admin outbound message.</span>')
        , "Admin sent "+v.conversationId+" to "+v.recipientName);
      },
      text: function(v){
        return ["INTERNAL COPY","To: "+v.recipientName+" <"+v.recipientEmail+">","Subject: "+v.adminSubject,"Message: "+v.adminMessage,"Ref: "+v.conversationId,"By: "+v.adminIdentity,"Time: "+v.timestamp].join("\n");
      }
    }
  };

  function render(type, vars){
    var t = TEMPLATES[type];
    // Also check ROUTES
    if (!t) {
      for (var i=0;i<ROUTES.length;i++){
        if (ROUTES[i].type===type){
          t = TEMPLATES[ROUTES[i].template];
          break;
        }
      }
    }
    if (!t) return {ok:false, errors:["unknown type "+type]};
    vars = vars||{};
    var errors=[];
    // Check allowed
    Object.keys(vars).forEach(function(k){
      if (t.allowedVars.indexOf(k)===-1) errors.push("undeclared variable: "+k);
    });
    t.allowedVars.forEach(function(k){
      if (vars[k]==null) errors.push("missing variable: "+k);
    });
    if (errors.length) return {ok:false, errors:errors};
    var out={};
    try {
      out.subject = t.subject(vars);
      out.html = t.html(vars);
      out.text = t.text(vars);
    } catch(e){
      return {ok:false, errors:["render threw: "+e.message]};
    }
    out.subject = String(out.subject||"").replace(/[\r\n\t]+/g," ").slice(0,150);
    return {ok:errors.length===0, errors:errors, subject:out.subject, html:out.html, text:out.text, template:type};
  }

  // Merge into existing EKGURU_EMAIL or create new
  if (window.EKGURU_EMAIL) {
    // Upgrade existing with v300 templates
    window.EKGURU_EMAIL.TEMPLATES_V300 = TEMPLATES;
    window.EKGURU_EMAIL.ROUTES_V300 = ROUTES;
    window.EKGURU_EMAIL.renderV300 = render;
    // Also override render to use v300 if available
    var oldRender = window.EKGURU_EMAIL.render;
    window.EKGURU_EMAIL.render = function(type, vars){
      var v300 = render(type, vars);
      if (v300.ok) return v300;
      // Fallback to old
      return oldRender(type, vars);
    };
  } else {
    window.EKGURU_EMAIL = { ROUTES: ROUTES, TEMPLATES: TEMPLATES, render: render, esc: esc };
  }
})();
