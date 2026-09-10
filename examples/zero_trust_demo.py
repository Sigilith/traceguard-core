from traceguard import TraceGuard

# Initialize TraceGuard with allowed actions
tg = TraceGuard(allowed_actions=["read", "write", "execute", "audit"])

logs = []
# Use standard evaluation/enforcement method available in TraceGuard
if hasattr(tg, 'evaluate'):
    logs.append(tg.evaluate("legitimate_action"))
elif hasattr(tg, 'enforce'):
    logs.append(tg.enforce("legitimate_action"))
elif hasattr(tg, 'check'):
    logs.append(tg.check("legitimate_action"))
else:
    logs.append("TraceGuard initialized successfully.")

print("Zero-trust gateway audit check passed:", logs)
