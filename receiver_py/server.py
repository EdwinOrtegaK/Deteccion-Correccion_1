# Main Receptor (Python)
from net_server import serve
from application import process_message

def handler(msg: dict):
    alg = msg["alg"]
    bits = msg["frame_bits"]
    return process_message(alg, bits)

if __name__ == "__main__":
    serve(port=5050, handler=handler)
