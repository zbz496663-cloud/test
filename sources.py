# Update these URLs if a city changes its portal. The app can run with empty URLs and will show setup guidance.
CITY_SOURCES = {
    "Dallas": {
        "portal": "https://aca-prod.accela.com/dallastx/default.aspx",
        "notes": "Dallas historical open-data permits are no longer updated; active permit tracking moved to DallasNow/Accela. Use portal export if available.",
        "csv_urls": [],
    },
    "Fort Worth": {
        "portal": "https://data.fortworthtexas.gov/datasets/CFW::cfw-development-permits-table/about",
        "notes": "Fort Worth has an open-data Development Permits table; use the Hub export CSV URL if the automatic download link changes.",
        "csv_urls": [],
    },
    "Plano": {
        "portal": "https://trakit.plano.gov/etrakit_prod/Search/permit.aspx",
        "notes": "Plano uses eTRAKiT. Export search results if available, then place CSV in data/manual_uploads.",
        "csv_urls": [],
    },
    "Frisco": {
        "portal": "https://www.friscotexas.gov/861/Development-Services-Reports",
        "notes": "Frisco publishes development services reports and uses an online plans/permits portal.",
        "csv_urls": [],
    },
    "McKinney": {
        "portal": "https://www.mckinneytexas.org/3563/Development-Services",
        "notes": "McKinney uses a Citizen Self-Service portal. Export/search results can be loaded manually if no API is available.",
        "csv_urls": [],
    },
    "Arlington": {
        "portal": "https://opendata.arlingtontx.gov/datasets/issued-permits",
        "notes": "Arlington open-data issued permits cover residential, commercial, sign, fence, pool, and CO; updated weekdays per city dataset page.",
        "csv_urls": [],
    },
}
