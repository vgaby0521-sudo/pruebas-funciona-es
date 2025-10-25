import argparse
import asyncio
import random
import time
from statistics import mean
import aiohttp

BASE = 'http://127.0.0.1:8000'
ENDPOINTS = [
    ('GET', '/'),
    ('GET', '/catalogo/'),
    ('GET', '/carrito/'),
    ('GET', '/admin/'),
]

async def worker(name, session, end_time, stats):
    while time.time() < end_time:
        method, path = random.choice(ENDPOINTS)
        url = BASE + path
        start = time.time()
        try:
            if method == 'GET':
                async with session.get(url) as resp:
                    await resp.read()
                    latency = (time.time() - start) * 1000
                    stats['latencies'].append(latency)
                    stats['total'] += 1
                    if resp.status >= 400:
                        stats['errors'] += 1
        except Exception:
            stats['errors'] += 1
        await asyncio.sleep(random.random() * 0.2)

async def run(concurrency, duration):
    timeout = aiohttp.ClientTimeout(total=30)
    stats = {'latencies': [], 'total': 0, 'errors': 0}
    end_time = time.time() + duration
    connector = aiohttp.TCPConnector(limit=0)
    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        tasks = [asyncio.create_task(worker(f'w{i}', session, end_time, stats)) for i in range(concurrency)]
        await asyncio.gather(*tasks)

    total = stats['total']
    errors = stats['errors']
    lat = stats['latencies']
    print('\n=== Load test summary ===')
    print(f'Total requests: {total}')
    print(f'Errors: {errors}')
    if lat:
        print(f'Latency ms: avg={mean(lat):.1f} p50={percentile(lat,50):.1f} p90={percentile(lat,90):.1f} p99={percentile(lat,99):.1f}')

def percentile(data, p):
    if not data:
        return 0
    data_sorted = sorted(data)
    k = (len(data_sorted)-1) * (p/100)
    f = int(k)
    c = min(f+1, len(data_sorted)-1)
    if f == c:
        return data_sorted[int(k)]
    d0 = data_sorted[f] * (c - k)
    d1 = data_sorted[c] * (k - f)
    return d0 + d1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--concurrency', '-c', type=int, default=20)
    parser.add_argument('--duration', '-d', type=int, default=15, help='seconds')
    args = parser.parse_args()
    print(f'Starting load test: concurrency={args.concurrency}, duration={args.duration}s, base={BASE}')
    asyncio.run(run(args.concurrency, args.duration))

if _name_ == '_main_':
    main()