"""
HYDRA Developer Toolkit API
A comprehensive developer utility API with 20+ endpoints.
Built by Toledo Technologies LLC.
"""
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import hashlib, uuid, base64, re, json, html, string, random, math, time
from urllib.parse import urlparse, parse_qs, urlencode
from datetime import datetime, timezone
import unicodedata, textwrap, difflib

app = FastAPI(
    title="HYDRA Developer Toolkit",
    description="20+ developer utility endpoints. Text analysis, hashing, encoding, data generation, and more.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


# ─── MODELS ────────────────────────────────────────────────────
class TextInput(BaseModel):
    text: str = Field(..., description="Input text to analyze")

class HashInput(BaseModel):
    text: str = Field(..., description="Text to hash")
    algorithm: str = Field("sha256", description="Hash algorithm: md5, sha1, sha256, sha512")

class Base64Input(BaseModel):
    text: str = Field(..., description="Text to encode/decode")

class SlugInput(BaseModel):
    text: str = Field(..., description="Text to convert to URL slug")
    separator: str = Field("-", description="Separator character")

class JsonInput(BaseModel):
    text: str = Field(..., description="JSON string to validate/format")

class RegexInput(BaseModel):
    pattern: str = Field(..., description="Regex pattern")
    text: str = Field(..., description="Text to match against")
    flags: str = Field("", description="Flags: i=ignorecase, m=multiline, s=dotall")

class DiffInput(BaseModel):
    text1: str = Field(..., description="Original text")
    text2: str = Field(..., description="Modified text")

class PasswordInput(BaseModel):
    password: str = Field(..., description="Password to check strength")

class ColorInput(BaseModel):
    color: str = Field(..., description="Color value (hex like #FF5733, rgb like rgb(255,87,51), or name)")

class LoremInput(BaseModel):
    paragraphs: int = Field(3, ge=1, le=20, description="Number of paragraphs")
    sentences_per: int = Field(5, ge=1, le=15, description="Sentences per paragraph")

class RandomDataInput(BaseModel):
    count: int = Field(5, ge=1, le=100, description="Number of records")
    fields: List[str] = Field(["name","email","phone"], description="Fields: name,email,phone,company,address,date,uuid,number")


# ─── HEALTH ────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"service": "HYDRA Developer Toolkit", "version": "1.0.0", "status": "operational", "endpoints": 20, "docs": "/docs"}

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}

# ─── TEXT ANALYSIS ─────────────────────────────────────────────
@app.post("/text/analyze", tags=["Text Analysis"])
def analyze_text(data: TextInput):
    t = data.text
    words = t.split()
    sentences = [s.strip() for s in re.split(r'[.!?]+', t) if s.strip()]
    syllable_count = sum(max(1, len(re.findall(r'[aeiouy]+', w.lower()))) for w in words)
    avg_syllables = syllable_count / max(len(words), 1)
    avg_sentence_len = len(words) / max(len(sentences), 1)
    flesch = 206.835 - 1.015 * avg_sentence_len - 84.6 * avg_syllables
    return {
        "characters": len(t), "characters_no_spaces": len(t.replace(" ", "")),
        "words": len(words), "sentences": len(sentences),
        "paragraphs": len([p for p in t.split("\n\n") if p.strip()]),
        "avg_word_length": round(sum(len(w) for w in words) / max(len(words), 1), 2),
        "reading_time_seconds": round(len(words) / 4.2),
        "speaking_time_seconds": round(len(words) / 2.5),
        "flesch_reading_ease": round(max(0, min(100, flesch)), 1),
        "reading_level": "Easy" if flesch > 70 else "Medium" if flesch > 50 else "Difficult",
    }

@app.post("/text/keywords", tags=["Text Analysis"])
def extract_keywords(data: TextInput, top_n: int = Query(10, ge=1, le=50)):
    stop = {"the","a","an","is","are","was","were","be","been","being","have","has","had","do","does",
            "did","will","would","could","should","may","might","shall","can","to","of","in","for",
            "on","with","at","by","from","as","into","about","between","through","during","before",
            "after","above","below","up","down","out","off","over","under","again","further","then",
            "once","and","but","or","nor","not","so","yet","both","either","neither","each","every",
            "all","any","few","more","most","other","some","such","no","only","own","same","than",
            "too","very","just","because","it","its","this","that","these","those","i","me","my","we",
            "our","you","your","he","him","his","she","her","they","them","their","what","which","who"}
    words = re.findall(r'\b[a-z]{3,}\b', data.text.lower())
    freq = {}
    for w in words:
        if w not in stop:
            freq[w] = freq.get(w, 0) + 1
    ranked = sorted(freq.items(), key=lambda x: -x[1])[:top_n]
    total = sum(freq.values())
    return {"keywords": [{"word": w, "count": c, "density": round(c / total * 100, 2)} for w, c in ranked], "unique_words": len(freq), "total_significant_words": total}

@app.post("/text/slug", tags=["Text Utilities"])
def slugify(data: SlugInput):
    text = unicodedata.normalize("NFKD", data.text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r'[^\w\s-]', '', text.lower().strip())
    slug = re.sub(r'[-\s]+', data.separator, text)
    return {"slug": slug, "original": data.text, "length": len(slug)}

@app.post("/text/case", tags=["Text Utilities"])
def convert_case(data: TextInput):
    t = data.text
    words = re.findall(r'[a-zA-Z0-9]+', t)
    return {
        "lower": t.lower(), "upper": t.upper(), "title": t.title(),
        "camelCase": words[0].lower() + "".join(w.capitalize() for w in words[1:]) if words else "",
        "PascalCase": "".join(w.capitalize() for w in words),
        "snake_case": "_".join(w.lower() for w in words),
        "kebab-case": "-".join(w.lower() for w in words),
        "CONSTANT_CASE": "_".join(w.upper() for w in words),
    }

@app.post("/text/strip-html", tags=["Text Utilities"])
def strip_html(data: TextInput):
    clean = re.sub(r'<[^>]+>', '', data.text)
    clean = html.unescape(clean)
    return {"cleaned": clean.strip(), "tags_removed": len(re.findall(r'<[^>]+>', data.text))}

# ─── HASHING & ENCODING ───────────────────────────────────────
@app.post("/crypto/hash", tags=["Crypto & Encoding"])
def generate_hash(data: HashInput):
    algos = {"md5": hashlib.md5, "sha1": hashlib.sha1, "sha256": hashlib.sha256, "sha512": hashlib.sha512}
    if data.algorithm not in algos:
        raise HTTPException(400, f"Unsupported algorithm. Use: {list(algos.keys())}")
    h = algos[data.algorithm](data.text.encode()).hexdigest()
    return {"hash": h, "algorithm": data.algorithm, "length": len(h)}

@app.post("/crypto/hash-all", tags=["Crypto & Encoding"])
def hash_all(data: TextInput):
    b = data.text.encode()
    return {a: hashlib.new(a, b).hexdigest() for a in ["md5", "sha1", "sha256", "sha512"]}

@app.post("/crypto/base64/encode", tags=["Crypto & Encoding"])
def base64_encode(data: Base64Input):
    encoded = base64.b64encode(data.text.encode()).decode()
    return {"encoded": encoded, "original_length": len(data.text), "encoded_length": len(encoded)}

@app.post("/crypto/base64/decode", tags=["Crypto & Encoding"])
def base64_decode(data: Base64Input):
    try:
        decoded = base64.b64decode(data.text).decode()
        return {"decoded": decoded}
    except Exception as e:
        raise HTTPException(400, f"Invalid base64: {str(e)}")

@app.get("/crypto/uuid", tags=["Crypto & Encoding"])
def generate_uuid(count: int = Query(1, ge=1, le=100), version: int = Query(4, ge=1, le=5)):
    if version == 4:
        ids = [str(uuid.uuid4()) for _ in range(count)]
    elif version == 1:
        ids = [str(uuid.uuid1()) for _ in range(count)]
    else:
        raise HTTPException(400, "Only UUID v1 and v4 supported")
    return {"uuids": ids, "version": version, "count": len(ids)}

# ─── JSON & DATA ──────────────────────────────────────────────
@app.post("/json/validate", tags=["JSON & Data"])
def validate_json(data: JsonInput):
    try:
        parsed = json.loads(data.text)
        pretty = json.dumps(parsed, indent=2)
        minified = json.dumps(parsed, separators=(',', ':'))
        def count_keys(obj):
            if isinstance(obj, dict):
                return len(obj) + sum(count_keys(v) for v in obj.values())
            elif isinstance(obj, list):
                return sum(count_keys(i) for i in obj)
            return 0
        keys = count_keys(parsed)
        return {"valid": True, "pretty": pretty, "minified": minified, "type": type(parsed).__name__,
                "keys": keys, "pretty_length": len(pretty), "minified_length": len(minified)}
    except json.JSONDecodeError as e:
        return {"valid": False, "error": str(e), "line": e.lineno, "column": e.colno}

@app.post("/json/diff", tags=["JSON & Data"])
def json_diff(data: DiffInput):
    try:
        j1 = json.loads(data.text1)
        j2 = json.loads(data.text2)
    except json.JSONDecodeError as e:
        raise HTTPException(400, f"Invalid JSON: {e}")
    p1 = json.dumps(j1, indent=2, sort_keys=True).splitlines()
    p2 = json.dumps(j2, indent=2, sort_keys=True).splitlines()
    diff = list(difflib.unified_diff(p1, p2, lineterm=''))
    return {"identical": j1 == j2, "diff_lines": len([d for d in diff if d.startswith('+') or d.startswith('-')]), "diff": '\n'.join(diff)}

# ─── REGEX ────────────────────────────────────────────────────
@app.post("/regex/test", tags=["Regex"])
def test_regex(data: RegexInput):
    flag_map = {"i": re.IGNORECASE, "m": re.MULTILINE, "s": re.DOTALL}
    flags = 0
    for f in data.flags:
        if f in flag_map:
            flags |= flag_map[f]
    try:
        compiled = re.compile(data.pattern, flags)
    except re.error as e:
        raise HTTPException(400, f"Invalid regex: {e}")
    matches = [{"match": m.group(), "start": m.start(), "end": m.end(), "groups": list(m.groups())} for m in compiled.finditer(data.text)]
    return {"pattern": data.pattern, "matches_found": len(matches), "matches": matches}

# ─── PASSWORD STRENGTH ────────────────────────────────────────
@app.post("/security/password-strength", tags=["Security"])
def check_password(data: PasswordInput):
    p = data.password
    score = 0
    feedback = []
    if len(p) >= 8: score += 1
    else: feedback.append("Use at least 8 characters")
    if len(p) >= 12: score += 1
    if len(p) >= 16: score += 1
    if re.search(r'[a-z]', p) and re.search(r'[A-Z]', p): score += 1
    else: feedback.append("Mix uppercase and lowercase")
    if re.search(r'\d', p): score += 1
    else: feedback.append("Add numbers")
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', p): score += 1
    else: feedback.append("Add special characters")
    if not re.search(r'(.)\1{2,}', p): score += 1
    else: feedback.append("Avoid repeated characters")
    common = ["password","123456","qwerty","admin","letmein","welcome","monkey","dragon"]
    if p.lower() not in common: score += 1
    else: feedback.append("Don't use common passwords")
    charset = 0
    if re.search(r'[a-z]', p): charset += 26
    if re.search(r'[A-Z]', p): charset += 26
    if re.search(r'\d', p): charset += 10
    if re.search(r'[^a-zA-Z0-9]', p): charset += 32
    entropy = round(len(p) * math.log2(max(charset, 1)), 1)
    labels = {0: "Very Weak", 1: "Very Weak", 2: "Weak", 3: "Weak", 4: "Fair", 5: "Good", 6: "Strong", 7: "Very Strong", 8: "Excellent"}
    return {"score": score, "max_score": 8, "strength": labels.get(score, "Excellent"),
            "entropy_bits": entropy, "feedback": feedback, "length": len(p)}

# ─── URL PARSING ──────────────────────────────────────────────
@app.post("/url/parse", tags=["URL Utilities"])
def parse_url(data: TextInput):
    try:
        p = urlparse(data.text)
        params = parse_qs(p.query)
        return {"scheme": p.scheme, "host": p.hostname, "port": p.port,
                "path": p.path, "query_string": p.query, "fragment": p.fragment,
                "params": params, "is_https": p.scheme == "https",
                "domain_parts": p.hostname.split('.') if p.hostname else []}
    except Exception as e:
        raise HTTPException(400, f"Invalid URL: {e}")

# ─── EMAIL VALIDATION ────────────────────────────────────────
@app.post("/validate/email", tags=["Validation"])
def validate_email(data: TextInput):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    valid = bool(re.match(pattern, data.text))
    parts = data.text.split('@') if '@' in data.text else [data.text, '']
    return {"email": data.text, "valid_format": valid, "local_part": parts[0],
            "domain": parts[1] if len(parts) > 1 else None,
            "issues": [] if valid else ["Invalid email format"]}

# ─── COLOR CONVERSION ────────────────────────────────────────
@app.post("/color/convert", tags=["Color Utilities"])
def convert_color(data: ColorInput):
    c = data.color.strip()
    r, g, b = 0, 0, 0
    if c.startswith('#'):
        h = c.lstrip('#')
        if len(h) == 3: h = ''.join(x*2 for x in h)
        if len(h) == 6:
            r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        else:
            raise HTTPException(400, "Invalid hex color")
    elif c.startswith('rgb'):
        nums = re.findall(r'\d+', c)
        if len(nums) >= 3:
            r, g, b = int(nums[0]), int(nums[1]), int(nums[2])
        else:
            raise HTTPException(400, "Invalid rgb color")
    else:
        raise HTTPException(400, "Provide hex (#FF5733) or rgb (rgb(255,87,51))")
    r, g, b = min(255, r), min(255, g), min(255, b)
    mx, mn = max(r, g, b) / 255, min(r, g, b) / 255
    l = (mx + mn) / 2
    s = 0 if mx == mn else (mx - mn) / (2 - mx - mn) if l > 0.5 else (mx - mn) / (mx + mn)
    if mx == mn: h_val = 0
    elif mx == r / 255: h_val = 60 * ((g / 255 - b / 255) / (mx - mn) % 6)
    elif mx == g / 255: h_val = 60 * ((b / 255 - r / 255) / (mx - mn) + 2)
    else: h_val = 60 * ((r / 255 - g / 255) / (mx - mn) + 4)
    return {"hex": f"#{r:02x}{g:02x}{b:02x}", "rgb": f"rgb({r},{g},{b})",
            "hsl": f"hsl({round(h_val)},{round(s*100)}%,{round(l*100)}%)",
            "r": r, "g": g, "b": b, "h": round(h_val), "s": round(s*100), "l": round(l*100)}

# ─── LOREM IPSUM ──────────────────────────────────────────────
LOREM_WORDS = "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo consequat duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum".split()

@app.post("/generate/lorem", tags=["Data Generation"])
def generate_lorem(data: LoremInput):
    paragraphs = []
    for _ in range(data.paragraphs):
        sents = []
        for _ in range(data.sentences_per):
            length = random.randint(6, 15)
            words = [random.choice(LOREM_WORDS) for _ in range(length)]
            words[0] = words[0].capitalize()
            sents.append(" ".join(words) + ".")
        paragraphs.append(" ".join(sents))
    full = "\n\n".join(paragraphs)
    return {"text": full, "paragraphs": len(paragraphs), "words": len(full.split()), "characters": len(full)}

# ─── RANDOM DATA GENERATION ──────────────────────────────────
FIRST_NAMES = ["James","Mary","John","Patricia","Robert","Jennifer","Michael","Linda","David","Elizabeth","William","Barbara","Richard","Susan","Joseph","Jessica","Thomas","Sarah","Charles","Karen"]
LAST_NAMES = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin"]
COMPANIES = ["Acme Corp","TechFlow","DataVerse","CloudNine","PixelForge","NexGen Labs","Quantum Solutions","BrightPath","CoreSync","VeloTech"]
STREETS = ["Main St","Oak Ave","Pine Rd","Elm Blvd","Cedar Ln","Maple Dr","Washington Ave","Park Pl","Lake View","Highland"]

@app.post("/generate/random-data", tags=["Data Generation"])
def generate_random_data(data: RandomDataInput):
    records = []
    for _ in range(data.count):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        rec = {}
        for f in data.fields:
            if f == "name": rec["name"] = f"{first} {last}"
            elif f == "email": rec["email"] = f"{first.lower()}.{last.lower()}{random.randint(1,99)}@example.com"
            elif f == "phone": rec["phone"] = f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
            elif f == "company": rec["company"] = random.choice(COMPANIES)
            elif f == "address": rec["address"] = f"{random.randint(1,9999)} {random.choice(STREETS)}"
            elif f == "date": rec["date"] = f"20{random.randint(20,26)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
            elif f == "uuid": rec["uuid"] = str(uuid.uuid4())
            elif f == "number": rec["number"] = random.randint(1, 1000000)
        records.append(rec)
    return {"count": len(records), "fields": data.fields, "data": records}

# ─── TEXT DIFF ────────────────────────────────────────────────
@app.post("/text/diff", tags=["Text Utilities"])
def text_diff(data: DiffInput):
    lines1 = data.text1.splitlines()
    lines2 = data.text2.splitlines()
    diff = list(difflib.unified_diff(lines1, lines2, lineterm=''))
    added = len([d for d in diff if d.startswith('+') and not d.startswith('+++')])
    removed = len([d for d in diff if d.startswith('-') and not d.startswith('---')])
    return {"identical": data.text1 == data.text2, "lines_added": added, "lines_removed": removed, "diff": '\n'.join(diff)}

# ─── MARKDOWN TO HTML ─────────────────────────────────────────
@app.post("/convert/md-to-html", tags=["Conversion"])
def markdown_to_html(data: TextInput):
    t = data.text
    t = re.sub(r'^### (.+)$', r'<h3>\1</h3>', t, flags=re.MULTILINE)
    t = re.sub(r'^## (.+)$', r'<h2>\1</h2>', t, flags=re.MULTILINE)
    t = re.sub(r'^# (.+)$', r'<h1>\1</h1>', t, flags=re.MULTILINE)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
    t = re.sub(r'`(.+?)`', r'<code>\1</code>', t)
    t = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', t)
    t = re.sub(r'^- (.+)$', r'<li>\1</li>', t, flags=re.MULTILINE)
    lines = t.split('\n')
    result = []
    in_list = False
    for line in lines:
        if line.strip().startswith('<li>'):
            if not in_list: result.append('<ul>'); in_list = True
            result.append(line)
        else:
            if in_list: result.append('</ul>'); in_list = False
            if line.strip() and not line.strip().startswith('<h'):
                result.append(f'<p>{line}</p>' if line.strip() else '')
            else:
                result.append(line)
    if in_list: result.append('</ul>')
    html_out = '\n'.join(result)
    return {"html": html_out, "input_length": len(data.text), "output_length": len(html_out)}

# ─── TIMESTAMP ────────────────────────────────────────────────
@app.get("/time/now", tags=["Time Utilities"])
def current_time():
    now = datetime.now(timezone.utc)
    return {"iso8601": now.isoformat(), "unix": int(now.timestamp()),
            "unix_ms": int(now.timestamp() * 1000),
            "date": now.strftime("%Y-%m-%d"), "time": now.strftime("%H:%M:%S"),
            "day_of_week": now.strftime("%A"), "day_of_year": now.timetuple().tm_yday}

@app.get("/time/convert/{timestamp}", tags=["Time Utilities"])
def convert_timestamp(timestamp: int):
    try:
        if timestamp > 1e12: timestamp = timestamp // 1000
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return {"iso8601": dt.isoformat(), "unix": int(dt.timestamp()),
                "human_readable": dt.strftime("%B %d, %Y at %I:%M %p UTC"),
                "date": dt.strftime("%Y-%m-%d"), "time": dt.strftime("%H:%M:%S")}
    except (ValueError, OSError) as e:
        raise HTTPException(400, f"Invalid timestamp: {e}")

# ─── JWT DECODE (no verification) ─────────────────────────────
@app.post("/jwt/decode", tags=["Security"])
def decode_jwt(data: TextInput):
    parts = data.text.split('.')
    if len(parts) != 3:
        raise HTTPException(400, "Invalid JWT format (expected 3 dot-separated parts)")
    def decode_part(part):
        padding = 4 - len(part) % 4
        part += "=" * padding
        try:
            return json.loads(base64.urlsafe_b64decode(part))
        except Exception:
            return None
    header = decode_part(parts[0])
    payload = decode_part(parts[1])
    exp = payload.get("exp") if payload else None
    expired = None
    if exp:
        expired = datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc)
    return {"header": header, "payload": payload, "signature_present": bool(parts[2]),
            "expired": expired, "warning": "Signature NOT verified - decode only"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(__import__('os').environ.get("PORT", 10000)))
