# Capa Aplicación (Receptor) 
from presentation import bits_to_ascii
from enlace_hamming import verificar_y_corregir
from enlace_crc32 import verificar

def process_message(alg: str, frame_bits: str):
    print(f"[APLICACIÓN][RECEPTOR] Algoritmo recibido: {alg}")
    if alg == "HAM":
        status, payload, syn = verificar_y_corregir(frame_bits)
        if status in ("OK", "CORRECTED"):
            text = bits_to_ascii(payload)
            print(f"[APLICACIÓN][RECEPTOR] Mostrar mensaje: \"{text}\" (status={status})")
            return {"status": status, "info": {"syndrome": syn}, "decoded_text": text}
        else:
            print("[APLICACIÓN][RECEPTOR] Error no corregible → mostrar error al usuario.")
            return {"status": "DISCARD", "info": {"syndrome": syn}}
    else:
        status, payload = verificar(frame_bits)
        if status == "OK":
            text = bits_to_ascii(payload)
            print(f"[APLICACIÓN][RECEPTOR] Mostrar mensaje: \"{text}\" (status=OK)")
            return {"status": "OK", "info": {}, "decoded_text": text}
        else:
            print("[APLICACIÓN][RECEPTOR] Error detectado → mostrar error al usuario.")
            return {"status": "DISCARD", "info": {}}
