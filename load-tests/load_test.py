import httpx
import time
import threading

AIRPORT_URL = "http://localhost:8001"
ITINERARY_URL = "http://localhost:8002"
NUM_USERS = 10
results = []

def test_user(user_id):
    start = time.time()
    try:
        r1 = httpx.get(AIRPORT_URL + "/airports/", timeout=5)
        r2 = httpx.get(ITINERARY_URL + "/itineraries/", timeout=5)
        r3 = httpx.get(AIRPORT_URL + "/health", timeout=5)
        elapsed = time.time() - start
        results.append({"user": user_id, "status": "OK", "time": round(elapsed, 3), "codes": [r1.status_code, r2.status_code, r3.status_code]})
    except Exception as e:
        results.append({"user": user_id, "status": "ERROR", "error": str(e)})

print("Iniciando prueba de carga con " + str(NUM_USERS) + " usuarios concurrentes...")
threads = [threading.Thread(target=test_user, args=(i,)) for i in range(NUM_USERS)]
start_total = time.time()
for t in threads: t.start()
for t in threads: t.join()
total = time.time() - start_total

print("\nResultados:")
for r in results:
    if r["status"] == "OK":
        print("  Usuario " + str(r["user"]) + ": OK en " + str(r["time"]) + "s - HTTP " + str(r["codes"]))
    else:
        print("  Usuario " + str(r["user"]) + ": ERROR - " + str(r["error"]))

ok = [r for r in results if r["status"] == "OK"]
times = [r["time"] for r in ok]
print("\nResumen:")
print("  Exitosos: " + str(len(ok)) + "/" + str(NUM_USERS))
if times:
    print("  Tiempo promedio: " + str(round(sum(times)/len(times), 3)) + "s")
    print("  Tiempo maximo: " + str(max(times)) + "s")
print("  Tiempo total: " + str(round(total, 3)) + "s")
