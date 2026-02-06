"""
Small FHIR example (demo only). Requires valid FHIR server and auth token.
Do NOT send PHI to external services without consent and appropriate BAAs.
"""
import requests
import os

FHIR_BASE = os.getenv("FHIR_BASE", "https://your-fhir-server.example.com")
FHIR_TOKEN = os.getenv("FHIR_TOKEN", "Bearer REPLACE_ME")

def get_patient(patient_id: str):
    headers = {"Authorization": FHIR_TOKEN, "Accept": "application/fhir+json"}
    resp = requests.get(f"{FHIR_BASE}/Patient/{patient_id}", headers=headers)
    resp.raise_for_status()
    return resp.json()

def get_latest_observation(patient_id: str, code: str = None):
    headers = {"Authorization": FHIR_TOKEN, "Accept": "application/fhir+json"}
    params = {"patient": patient_id, "_count": 1, "_sort": "-date"}
    if code:
        params["code"] = code
    resp = requests.get(f"{FHIR_BASE}/Observation", headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()
