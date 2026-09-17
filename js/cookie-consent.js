/* EkGuru consent integration boundary.
 *
 * Consent for Google advertising is configured through Google Privacy &
 * messaging (or another Google-certified CMP), not through a home-made banner.
 * Acknowledgement is not consent, so this legacy include intentionally renders
 * no UI, writes no storage, and makes no compliance claim. It remains as a
 * harmless compatibility path while generated pages are migrated.
 *
 * Account-side CMP activation and geographic message testing are marked
 * REVIEW_REQUIRED in data/monetization/google-monetization.json and the global
 * readiness audit. Never add an accept-only dialog here.
 */
(function () {
  "use strict";
  document.documentElement.dataset.consentFramework = "certified-cmp-required";
})();

/* Country-aware presentation metadata. This does not show a consent banner,
   track a visitor, or send locale data anywhere. It only selects local CSS. */
(function () {
  "use strict";
  var path = String(location.pathname || "").toLowerCase();
  var aliases = {
    india:"IN",bharat:"IN",nepal:"NP",bangladesh:"BD",pakistan:"PK",srilanka:"LK",
    "sri-lanka":"LK",indonesia:"ID","timor-leste":"TL",greece:"GR",cyprus:"CY",
    albania:"AL","south-africa":"ZA",namibia:"NA",somalia:"SO",djibouti:"DJ",
    ethiopia:"ET",kenya:"KE",netherlands:"NL",belgium:"BE",suriname:"SR",
    iran:"IR","united-arab-emirates":"AE",uae:"AE","saudi-arabia":"SA",
    andorra:"AD",spain:"ES",france:"FR",haiti:"HT",canada:"CA",
    "united-states":"US",usa:"US",australia:"AU","new-zealand":"NZ",
    japan:"JP",china:"CN",singapore:"SG",malaysia:"MY",turkey:"TR",
    germany:"DE",austria:"AT",switzerland:"CH",brazil:"BR",portugal:"PT",
    mexico:"MX",argentina:"AR","united-kingdom":"GB",uk:"GB"
  };
  var code = "";
  Object.keys(aliases).some(function (slug) {
    if (new RegExp("(?:^|/|-)" + slug + "(?:/|-|$)").test(path)) { code = aliases[slug]; return true; }
    return false;
  });
  if (!code) {
    try {
      var locale = String(localStorage.getItem("ekguru_country") || navigator.language || "");
      var match = locale.match(/[-_]([A-Za-z]{2})$/); if (match) code = match[1].toUpperCase();
    } catch (e) {}
  }
  var culture = {
    IN:"south-asia",NP:"south-asia",BD:"south-asia",PK:"south-asia",LK:"south-asia",
    AE:"gulf",SA:"gulf",IR:"persian",ET:"horn",DJ:"horn",SO:"horn",KE:"east-africa",
    ZA:"southern-africa",NA:"southern-africa",ID:"southeast-asia",TL:"southeast-asia",
    MY:"southeast-asia",SG:"southeast-asia",JP:"japan",CN:"east-asia",
    GR:"mediterranean",CY:"mediterranean",AL:"balkans",ES:"mediterranean",
    FR:"western-europe",NL:"western-europe",BE:"western-europe",DE:"western-europe",
    AT:"western-europe",CH:"western-europe",AD:"mediterranean",SR:"caribbean",
    HT:"caribbean",BR:"latin-america",MX:"latin-america",AR:"latin-america"
  };
  if (code) document.documentElement.setAttribute("data-country", code);
  document.documentElement.setAttribute("data-culture", culture[code] || "global");
})();
