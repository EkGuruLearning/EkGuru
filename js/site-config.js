/* =========================================================
   EkGuru — SITE CONFIG
   ---------------------------------------------------------
   Edit brand, contact and SEO settings here. Nothing else.
   ========================================================= */

window.EKGURU_SITE = {
  /* ---------- Brand ---------- */
  brand: "EkGuru",
  tagline: "One Student. One Guru. One Goal.",

  /* ---------- Live URL (used for canonical + sitemap + OG) ----------
     If you rename the repo, change this ONE line.                     */
  baseUrl: "https://ekgurulearning.github.io/EkGuru/",

  /* ---------- Contact (REAL) ---------- */
  email: "EkGuruLearning@gmail.com",

  /* WhatsApp: leave "" to hide every WhatsApp button site-wide.
     Add a real number with country code to switch them all on,
     e.g. "+919876543210"                                              */
  whatsapp: "",

  /* ---------- Tutor application form ----------
     Paste your Google Form link here and every "Become a Tutor" button
     switches from email to the form automatically.
     Leave "" and the buttons keep opening a pre-filled email instead.
     Example: "https://forms.gle/AbCdEfGhIjKlMnOp"                       */
  applyFormUrl: "https://forms.gle/xtnT1mwuDvSKxn8F6",

  /* ---------- Social (leave "" to hide) ---------- */
  youtubeChannel: "https://www.youtube.com/@Sashi-e3s",
  facebook: "",
  instagram: "",

  /* ---------- Commerce ---------- */
  currency: "$",            // fallback symbol if conversion is off
  currencyCode: "USD",      // the canonical currency, used in Google schema

  /* =========================================================
     COUNTRY-AWARE PRICING
     ---------------------------------------------------------
     Shows prices in the visitor's own currency automatically,
     with no login and no server. Detection uses their browser
     timezone and language only, so nothing leaves their device.

     mode
       "currency"  same price, shown in their local money   ← default
       "regional"  different price per region (see `regional`)
       "off"       everyone sees plain USD

     showUsdAlso   append a quiet "($12)" so the real figure is
                   always visible next to the converted one

     rates         1 USD = how much. Update these every month or
                   two; approximate is fine, they are indicative.
     ========================================================= */
  pricing: {
    mode: "currency",
    showUsdAlso: true,
    allowManualSwitch: true,

    rates: {
      INR: 83,    EUR: 0.92,  GBP: 0.79,  JPY: 150,   AED: 3.67,
      BRL: 5.0,   CAD: 1.36,  AUD: 1.52,  NZD: 1.64,  SGD: 1.34,
      ZAR: 18.5,  MXN: 17.1,  PHP: 56,    MYR: 4.7,   THB: 35,
      IDR: 15600, VND: 24500, KRW: 1330,  CNY: 7.2,   HKD: 7.8,
      SAR: 3.75,  QAR: 3.64,  KWD: 0.31,  TRY: 32,    PLN: 4.0,
      SEK: 10.4,  NOK: 10.6,  DKK: 6.9,   CHF: 0.88,  ILS: 3.7,
      PKR: 278,   BDT: 110,   NPR: 133,   LKR: 300,   NGN: 1500,
      KES: 129,   EGP: 48,    MAD: 9.9,   RUB: 92,    UAH: 41,
      CZK: 23,    HUF: 355,   RON: 4.6,   ARS: 950,   CLP: 950,
      COP: 3900,  PEN: 3.7,   MUR: 46,    FJD: 2.25,  GHS: 15
    },

    /* Only used when mode is "regional". A multiplier on the USD
       price, so 0.35 means an Indian student pays 35% of it.
       ⚠️ This changes what a tutor earns — agree it with them first. */
    regional: {
      IN: 0.35, PK: 0.35, BD: 0.35, NP: 0.35, LK: 0.4,
      BR: 0.5,  MX: 0.6,  AR: 0.4,  CO: 0.5,  PE: 0.55,
      ZA: 0.55, NG: 0.4,  KE: 0.45, EG: 0.4,  PH: 0.5,
      ID: 0.5,  VN: 0.5,  TH: 0.6,  TR: 0.5,  UA: 0.4,
      default: 1.0
    }
  },

  /* ---------- Founding year (for schema) ---------- */
  foundingYear: 2026,

  /* =========================================================
     FOUNDER — appears in Google's knowledge graph as the person
     behind EkGuru. Also powers the "Founder" credit in the footer.
     ========================================================= */
  founder: {
    name: "Prakash",
    displayName: "Prakash — MNIT Jaipur",
    title: "Founder & CEO, EkGuru",
    degree: "B.Tech, Computer Science & Engineering",
    college: "Malaviya National Institute of Technology Jaipur",
    collegeShort: "MNIT Jaipur",
    collegeUrl: "https://www.mnit.ac.in/",
    batch: "2022–2026",
    city: "Jaipur, Rajasthan, India",

    /* Birthplace — used only for local SEO signals and the founder schema.
       Nothing here is shown on the site beyond the footer credit line.     */
    birthplace: {
      hamlet: "Gothwal Ki Dhani",
      village: "Kolwa",
      district: "Dausa",
      state: "Rajasthan",
      country: "India",
      pincode: "303325",
      landmark: "Kolwa Railway Station"
    },
    /* The ONLY sentence written about the founder anywhere on the site. */
    bio: "Prakash — MNIT Jaipur, CSE 2022–2026 batch pass out.",
    email: "EkGuruLearning@gmail.com",
    linkedin: "https://www.linkedin.com/in/itstheprakash/",
    twitter: ""
  },

  /* =========================================================
     LAUNCH STATUS
     status: "live"    -> no badge
             "soon"    -> "Coming soon" pill in the header
             "beta"    -> "Beta" pill in the header
     ========================================================= */
  status: "soon"
};

/* =========================================================
   The 7 major countries our students come from.
   Used for: language switcher, SEO hreflang, "students from" strip.
   ========================================================= */
window.EKGURU_MARKETS = [
  { code: "en", locale: "en-US", country: "United States", flag: "🇺🇸", label: "English",    dir: "ltr" },
  { code: "es", locale: "es-ES", country: "Spain",         flag: "🇪🇸", label: "Español",    dir: "ltr" },
  { code: "fr", locale: "fr-FR", country: "France",        flag: "🇫🇷", label: "Français",   dir: "ltr" },
  { code: "de", locale: "de-DE", country: "Germany",       flag: "🇩🇪", label: "Deutsch",    dir: "ltr" },
  { code: "pt", locale: "pt-BR", country: "Brazil",        flag: "🇧🇷", label: "Português",  dir: "ltr" },
  { code: "ja", locale: "ja-JP", country: "Japan",         flag: "🇯🇵", label: "日本語",       dir: "ltr" },
  { code: "ar", locale: "ar-AE", country: "UAE",           flag: "🇦🇪", label: "العربية",    dir: "rtl" }
];
