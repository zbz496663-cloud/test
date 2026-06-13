from __future__ import annotations

TARGET_KEYWORDS = [
    "restaurant", "retail", "tenant finish", "tenant improvement", "finish out",
    "finish-out", "medical", "urgent care", "commercial remodel", "remodel",
    "coffee", "salon", "fitness", "gym", "drive thru", "drive-thru", "co ",
    "certificate of occupancy", "sign", "channel letters", "monument", "storefront",
]

KEYWORD_SCORES = {
    "restaurant": 100,
    "coffee": 100,
    "drive thru": 100,
    "drive-thru": 100,
    "retail": 95,
    "tenant finish": 95,
    "tenant improvement": 95,
    "finish out": 95,
    "finish-out": 95,
    "certificate of occupancy": 95,
    "urgent care": 92,
    "medical": 90,
    "salon": 88,
    "fitness": 88,
    "gym": 88,
    "commercial remodel": 82,
    "remodel": 75,
    "sign": 80,
    "channel letters": 100,
    "monument": 95,
    "storefront": 95,
}

IGNORE_KEYWORDS = [
    "residential", "single family", "pool", "fence", "roof", "hvac", "plumbing",
    "water heater", "solar", "irrigation", "garage sale", "sprinkler", "electrical only",
]


def normalize_text(value: object) -> str:
    return "" if value is None else str(value).lower()


def is_target_lead(row_text: str) -> bool:
    text = normalize_text(row_text)
    if any(k in text for k in IGNORE_KEYWORDS):
        # Still keep if it is clearly commercial signage/CO/restaurant/retail.
        strong = ["restaurant", "retail", "certificate of occupancy", "tenant", "sign", "medical"]
        return any(k in text for k in strong)
    return any(k in text for k in TARGET_KEYWORDS)


def score_lead(row_text: str) -> int:
    text = normalize_text(row_text)
    score = 0
    for keyword, value in KEYWORD_SCORES.items():
        if keyword in text:
            score = max(score, value)
    if score == 0 and is_target_lead(text):
        score = 50
    return score


def category(row_text: str) -> str:
    text = normalize_text(row_text)
    if any(k in text for k in ["restaurant", "coffee", "drive thru", "drive-thru"]):
        return "Restaurant/Food"
    if any(k in text for k in ["retail", "storefront", "tenant finish", "finish out", "finish-out"]):
        return "Retail/Tenant Finish-Out"
    if any(k in text for k in ["medical", "urgent care", "clinic", "dental"]):
        return "Medical"
    if any(k in text for k in ["sign", "channel letters", "monument"]):
        return "Signage"
    if "certificate of occupancy" in text or " co " in f" {text} ":
        return "Certificate of Occupancy"
    if "remodel" in text:
        return "Commercial Remodel"
    return "Other Potential"
