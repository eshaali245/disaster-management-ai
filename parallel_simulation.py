"""
=================================================
DISASTER MANAGEMENT SYSTEM - Parallel Simulation
=================================================
Multiprocessing se multiple disasters simulate karo.
"""

import multiprocessing
import random
import time
import json
import os
from datetime import datetime

# ─── Single Disaster Simulation ──────────────────────────
def simulate_disaster(args):
    """Ek disaster ka simulation karo"""
    disaster_id, disaster_type, location, severity, people, resources = args

    # Simulate processing time
    processing_time = random.uniform(0.1, 0.5)
    time.sleep(processing_time)

    # Resource allocation logic
    severity_factor = {'Low': 0.3, 'Medium': 0.6, 'High': 0.85, 'Critical': 1.0}
    factor = severity_factor.get(severity, 0.5)

    ambulances_dispatched = max(1, int(people * factor / 500))
    resources_allocated   = min(resources, int(resources * factor))
    response_time         = max(5, int((1 - factor) * 120) + random.randint(5, 30))

    if factor >= 0.85:
        status = "🚨 CRITICAL - Emergency Response"
    elif factor >= 0.6:
        status = "⚠️ HIGH - Urgent Response"
    elif factor >= 0.3:
        status = "🟡 MEDIUM - Standard Response"
    else:
        status = "🟢 LOW - Monitoring"

    result = {
        'id'                   : disaster_id,
        'disaster_type'        : disaster_type,
        'location'             : location,
        'severity'             : severity,
        'people_affected'      : people,
        'ambulances_dispatched': ambulances_dispatched,
        'resources_allocated'  : resources_allocated,
        'response_time_min'    : response_time,
        'status'               : status,
        'processing_time_s'    : round(processing_time, 3),
        'node'                 : f"Node-{(disaster_id % 4) + 1}",
        'timestamp'            : datetime.now().strftime("%H:%M:%S"),
    }
    return result


# ─── Run Parallel Simulation ─────────────────────────────
def run_parallel_simulation(num_disasters=12):
    disasters_list = ['Flood', 'Earthquake', 'Fire', 'Cyclone',
                      'Landslide', 'Tsunami', 'Drought', 'Heatwave']
    locations_list = ['Karachi', 'Lahore', 'Islamabad', 'Peshawar',
                      'Quetta', 'Multan', 'Faisalabad', 'Rawalpindi']
    severities_list = ['Low', 'Medium', 'High', 'Critical']

    tasks = []
    for i in range(num_disasters):
        severity = random.choice(severities_list)
        sev_factor = {'Low': 0.3, 'Medium': 0.6, 'High': 0.85, 'Critical': 1.0}
        people = int(random.randint(500, 10000) * sev_factor[severity])
        resources = random.randint(50, 300)
        tasks.append((
            i + 1,
            random.choice(disasters_list),
            random.choice(locations_list),
            severity,
            people,
            resources,
        ))

    cpu_count = min(multiprocessing.cpu_count(), 4)
    print(f"\n🔧 Using {cpu_count} parallel processes for {num_disasters} disasters\n")

    start_time = time.time()
    with multiprocessing.Pool(processes=cpu_count) as pool:
        results = pool.map(simulate_disaster, tasks)
    end_time = time.time()

    total_time = round(end_time - start_time, 2)
    return results, total_time, cpu_count


# ─── Main ────────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 60)
    print("⚡ PARALLEL DISASTER SIMULATION ENGINE")
    print("=" * 60)

    results, total_time, cpus = run_parallel_simulation(num_disasters=12)

    print(f"{'ID':<4} {'Type':<12} {'Location':<12} {'Severity':<10} "
          f"{'People':<8} {'Ambul':<6} {'Time(min)':<10} Node")
    print("-" * 75)
    for r in results:
        print(f"{r['id']:<4} {r['disaster_type']:<12} {r['location']:<12} "
              f"{r['severity']:<10} {r['people_affected']:<8} "
              f"{r['ambulances_dispatched']:<6} {r['response_time_min']:<10} {r['node']}")

    print("\n" + "=" * 60)
    print(f"⏱  Total Simulation Time : {total_time}s")
    print(f"🖥  Parallel Processes   : {cpus}")
    print(f"📊 Disasters Processed  : {len(results)}")
    total_amb  = sum(r['ambulances_dispatched'] for r in results)
    total_peop = sum(r['people_affected'] for r in results)
    print(f"🚑 Total Ambulances     : {total_amb}")
    print(f"👥 Total People Helped  : {total_peop:,}")
    print("=" * 60)

    # Save results
    os.makedirs('simulation_results', exist_ok=True)
    with open('simulation_results/latest_simulation.json', 'w') as f:
        json.dump({
            'results'    : results,
            'total_time' : total_time,
            'cpu_count'  : cpus,
            'timestamp'  : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }, f, indent=2)
    print("\n✅ Results saved to simulation_results/latest_simulation.json")
