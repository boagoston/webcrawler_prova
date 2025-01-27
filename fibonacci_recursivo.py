import sys

def fibonacci(n):                            
    if n <= 1:                                 
        return n                             
    else:                                    
        return fibonacci(n - 1) + fibonacci(n - 2) 

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 fibonacci_recursivo.py <numero>")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
        if n < 0:
            raise ValueError("O número deve ser não negativo.")
    except ValueError as e:
        print(f"Erro: {e}")
        sys.exit(1)

    # Chama a função e imprime o resultado
    print(f'Resultado: {fibonacci(n)}')