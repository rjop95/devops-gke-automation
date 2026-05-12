# L2 Support Playbook: Web App Production

## 1. Incident Triage (Initial Response)
- **Check Uptime:** Verify status via Uptrends Dashboard or `curl http://[LB_IP]/health`.
- **Verify Alerts:** Check PagerDuty for triggered incidents and severity levels.

## 2. API Troubleshooting (Postman)
- Use the `L2_Validation_Suite` Postman collection.
- **Common HTTP Status Codes:**
    - **401/403:** Check `X-Support-Token` header.
    - **502/504:** Check if GKE Pods are in `CrashLoopBackOff`.
    - **500:** Analyze server logs for Python Tracebacks.

## 3. Log Analysis (Google Cloud Logging / SQL)
Use the following query to identify root causes:
```sql
resource.type="k8s_container"
severity>="ERROR"
textPayload:"Traceback"
