# Capa Presentación (Receptor) 
def bits_to_ascii(bits: str) -> str:
    out = []
    for i in range(0, len(bits), 8):
        chunk = bits[i:i+8]
        if len(chunk) < 8: break
        out.append(chr(int(chunk, 2)))
    s = "".join(out)
    print(f"[PRESENTACIÓN][RECEPTOR] bits->ASCII: \"{s}\"")
    return s
