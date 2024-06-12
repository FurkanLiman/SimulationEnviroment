
import multiprocessing
import subprocess

def run_script(startingVariables):
    subprocess.run(["python", "main.py",str(startingVariables)])

if __name__ == "__main__":
    developerMode = False
    if developerMode:
        processes = []
        limits = [25,35]
        lengths = [45,65]
        daylimit = [2,10]
        # developermode, population Number, food number, x length, y length, day limit, mutasyon oranı, daily disaster
        for i in range(lengths[0],lengths[1]):    
            for l in range(daylimit[0],daylimit[1]):
                startingVariables = [developerMode,25,25,i,i,l]
                p = multiprocessing.Process(target=run_script, args=(startingVariables,))
                p.start()
                processes.append(p)

            for p in processes:
                p.join()
    else:
        startingVariables = [developerMode,25,25,50,50,10]
        p = multiprocessing.Process(target=run_script, args=(startingVariables,))
        p.start()
        p.join()