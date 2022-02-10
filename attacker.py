import requests, threading, random, sys

'''
    Sample command:

    python3 attacker.py "localhost" "8000" "/unprotected" "1000"
    python3 attacker.py "localhost" "8000" "/protected" "1000"

'''

if len(sys.argv) != 5:
    print("Missing info")
    print(len(sys.argv))
    sys.exit(1)

host_ip, port, path, n_attack = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

if not path.startswith("/"):
    print("path should start with /")
    sys.exit(1)

def single_req(host, port, path, shared, idx):
    try:
        x = random.randint(10, 100)
        res = requests.get(f"http://{host}:{port}{path}?x={x}&y={x}", timeout=1.5)
        
        
        if res.status_code == 200:
            if shared is not None and idx is not None:
                shared[idx] = 1
        return res

    except:
        pass

def attack(host, port, path, count):
    result = [0] * count
    # threads = []
    for i in range (count):
        try:
            t = threading.Thread(target=single_req, args=(host, port, path, result, i),daemon=True)
            t.start()
            # threads.append(t)
        except Exception as e:
            pass

        if i % 50 == 0:
            print("# request sent: ", i)

    print("\nLast request status code: \n")

    res = single_req(host, port, path, None, None)

    if res is not None:
        print(f"Status code: {res.status_code}")
        print(res.text)
    else:
        print(res)
        print("Server is not responding")
    
    print(sum(result)/len(result))


attack(host_ip, port, path, int(n_attack))