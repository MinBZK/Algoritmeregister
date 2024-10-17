import os

# Provide FAKE but realistic values for testing
os.environ[
    "PREDITOR_SHARED_SECRET_KEY"
] = "b=9_i8v7eR&BJBu=8u4uAUuc7zy-EijCBV4vaaFpPBHY-rtbYKRReBRwX=m+3b&3"
os.environ["PREDITOR_SHARED_TOTP_SEED"] = "GCPMDAC56Q7MHOKQNN6OHMYYAR6V6UMW"
os.environ["USE_C3PO"] = "False"
