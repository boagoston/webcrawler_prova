import sys
import subprocess

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python busca_servimed.py <número_do_pedido>")
        sys.exit(1)

    pedido_numero = sys.argv[1]

    # Comando para chamar o Scrapy com o número do pedido
    subprocess.run(["scrapy", "crawl", "servimed_pedido", "-a", f"pedido_numero={pedido_numero}"])
