# POC Report: Local contractor quote comparison tool

## Result
A small local proof of concept was generated in `draft_project/`.

## How To Run
```bash
python3 backend/app.py
```

## Limitations
- Uses deterministic placeholder logic by default.
- Does not call external AI services unless the implementation adds exported environment variables.
- Includes deploy scaffolding, but production deployment still needs project-specific configuration.
