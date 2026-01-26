import socket


SERVER_IP = "127.0.0.1"
PORT = 5050


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_IP, PORT))
    except OSError as e:
        print(f"Connexion impossible vers {SERVER_IP}:{PORT} -> {e}")
        return

    print(f"Connecté au serveur {SERVER_IP}:{PORT}")
    buffer = ""

    try:
        while True:
            data = sock.recv(4096)
            if not data:
                print("Serveur déconnecté.")
                break

            buffer += data.decode("utf-8", errors="replace")

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.rstrip("\r")

                if line.startswith("INPUT:"):
                    prompt = line[len("INPUT:"):].strip()
                    try:
                        answer = input(prompt)
                    except (EOFError, KeyboardInterrupt):
                        answer = ""
                    sock.sendall((answer + "\n").encode("utf-8", errors="replace"))
                else:
                    print(line)

    finally:
        try:
            sock.close()
        except OSError:
            pass


if __name__ == "__main__":
    main()

