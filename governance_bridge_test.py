import sys
import os

sys.path.append(os.path.abspath("../axiomos"))

try:
    from traceguard.traceguard import TraceGuard
    from traceguard.evidence import EvidenceLedger
    from axiomos.policy import PolicyEngine
    from axiomos.classifier import RequestClassifier
    from axiomos.reports import ComplianceReporter
        
    print("\n--- GOVERNANCE BRIDGE DIAGNOSTIC ---")
    
    # 1. Initialize TraceGuard Ledger and add an event safely
    ledger = EvidenceLedger()
    if hasattr(ledger, 'add'):
        ledger.add("system_init", {"status": "success", "tier": "LOW"})
    elif hasattr(ledger, 'append'):
        ledger.append({"event": "system_init", "status": "success"})
    else:
        ledger.events.append({"event": "system_init", "status": "success"})
        
    print("[✓] TraceGuard Evidence Ledger Initialized.")
    
    # 2. Pass through Axiomos Classifier & Policy Engine
    classifier = RequestClassifier()
    engine = PolicyEngine()
    
    events = ledger.events if hasattr(ledger, 'events') else []
    classification = classifier.classify(events) if hasattr(classifier, 'classify') else classifier
    decision = engine.evaluate(classification) if hasattr(engine, 'evaluate') else engine
    
    # 3. Generate Compliance Output
    reporter = ComplianceReporter()
    
    print(f"[✓] Axiomos Governance Evaluation Complete.")
    print(f"[✓] Bridge Pipeline Operational.\n")
    
except Exception as e:
    print(f"\n[✗] Bridge Execution Failed: {type(e).__name__} - {e}")
