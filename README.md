# HYDRA Developer Toolkit API

A comprehensive developer utility API with 20+ endpoints for text analysis, hashing, encoding, data generation, and more.

## Endpoints

- **Text Analysis**: Word count, readability scores, reading time, keyword extraction
- **Text Utilities**: Slugify, case conversion, HTML stripping, diff
- **Crypto & Encoding**: MD5/SHA hashing, Base64 encode/decode, UUID generation
- **JSON & Data**: Validation, formatting, minification, diff
- **Regex**: Pattern testing with capture groups
- **Security**: Password strength analysis, JWT decoding
- **URL Utilities**: URL parsing with query parameter extraction
- **Validation**: Email format validation
- **Color Utilities**: Hex/RGB/HSL conversion
- **Data Generation**: Lorem ipsum, random test data
- **Conversion**: Markdown to HTML
- **Time**: Current timestamp, unix conversion

## Deploy

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 10000
```

## Docs

Visit `/docs` for interactive Swagger UI or `/redoc` for ReDoc.

Built by Toledo Technologies LLC.
