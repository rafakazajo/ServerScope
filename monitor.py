import psutil
import mysql.connector
import time
import socket
import subprocess

config = {
    'host': '32.197.125.125',
    'user': 'wordpress',
    'password': 'wp_password',
    'database': 'serverscope_db'
}

def obtener_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def obtener_procesos():
    try:
        procs = []
        for p in sorted(psutil.process_iter(['name', 'cpu_percent']), key=lambda x: x.info['cpu_percent'] or 0, reverse=True)[:3]:
            procs.append(f"{p.info['name']} ({p.info['cpu_percent']}%)")
        return "\n".join(procs)
    except:
        return "No disponible"

def obtener_puertos(ip_objetivo):
    try:
        res = subprocess.run(['nmap', '-sV', '-F', ip_objetivo], capture_output=True, text=True, timeout=30)
        lineas = []
        for linea in res.stdout.split('\n'):
            if 'open' in linea and ('/tcp' in linea or '/udp' in linea):
                lineas.append(linea.strip())
        return "\n".join(lineas) if lineas else "No se detectaron puertos abiertos comunes"
    except:
        return "Error al ejecutar Nmap"

def contar_clientes():
    try:
        activas = [c for c in psutil.net_connections(kind='tcp') if c.status == 'ESTABLISHED']
        return len(activas)
    except:
        return 0

contador_ciclos = 0
puertos_cache = "Realizando primer escaneo..."

while True:
    try:
        ip_local = obtener_ip()
        
        if contador_ciclos % 30 == 0:
            puertos_cache = obtener_puertos(ip_local)
            
        contador_ciclos += 1

        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        clientes = contar_clientes()
        procesos = obtener_procesos()

        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO monitoreo (cpu_uso, ram_uso, disco_uso, clientes, ip, procesos, puertos) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                       (cpu, ram, 0, clientes, ip_local, procesos, puertos_cache))
        conn.commit()
        cursor.close()
        conn.close()
    except:
        pass
    
    time.sleep(10)
