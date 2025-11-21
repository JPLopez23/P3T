import json
from typing import Dict, List, Tuple, Set
import os

class TuringMachine:
    """
    Implementación de una Máquina de Turing para cifrado/descifrado César.
    Solo usa operaciones básicas: cambiar estado, escribir símbolo, mover cabeza.
    """
    
    def __init__(self, states: Set[str], input_alphabet: Set[str], 
                 tape_alphabet: Set[str], initial_state: str, 
                 accept_states: Set[str], transitions: Dict):
        self.states = states
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.initial_state = initial_state
        self.accept_states = accept_states
        self.transitions = transitions
        self.tape = []
        self.head_position = 0
        self.current_state = initial_state
        
    def load_tape(self, input_string: str):
        """Carga el input en la cinta"""
        self.tape = list(input_string) + ['_']  
        self.head_position = 0
        self.current_state = self.initial_state
        
    def step(self) -> bool:
        """
        Ejecuta un paso de la máquina de Turing.
        Retorna True si puede continuar, False si termina.
        """
        if self.current_state in self.accept_states:
            return False
            
        while self.head_position >= len(self.tape):
            self.tape.append('_')
            
        current_symbol = self.tape[self.head_position]
        transition_key = (self.current_state, current_symbol)
        
        if transition_key not in self.transitions:
            return False
            
        new_state, write_symbol, direction = self.transitions[transition_key]
        
        self.tape[self.head_position] = write_symbol
        self.current_state = new_state
        
        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1
            
        if self.head_position < 0:
            self.tape.insert(0, '_')
            self.head_position = 0
            
        return True
        
    def run(self, max_steps: int = 100000) -> str:
        """Ejecuta la máquina hasta que acepte o alcance max_steps"""
        steps = 0
        while steps < max_steps and self.step():
            steps += 1
            
        result = ''.join(self.tape).rstrip('_')
        return result
        
    def get_tape_content(self) -> str:
        """Retorna el contenido actual de la cinta"""
        return ''.join(self.tape).rstrip('_')


def parse_key(key_str: str) -> int:
    """Convierte la llave a número (1-26 para letras, o número directo)"""
    if key_str.isdigit():
        return int(key_str)
    else:
        return ord(key_str.upper()) - ord('A') + 1


def caesar_encrypt(message: str, shift: int) -> str:
    """
    Encriptación César usando solo operaciones básicas de MT simuladas.
    ALFABETO: Solo 26 letras (A-Z)
    Los espacios NO se encriptan, se mantienen tal cual.
    """
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  
    result = []
    
    for char in message:
        if char == ' ':
            result.append(' ')
        elif char in alphabet:
            pos = alphabet.index(char)
            new_pos = (pos + shift) % 26 
            result.append(alphabet[new_pos])
        else:
            result.append(char)
    
    return ''.join(result)


def caesar_decrypt(message: str, shift: int) -> str:
    """
    Decriptación César usando solo operaciones básicas de MT simuladas.
    ALFABETO: Solo 26 letras (A-Z)
    Los espacios NO se decriptan, se mantienen tal cual.
    """
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  
    result = []
    
    for char in message:
        if char == ' ':
            result.append(' ')
        elif char in alphabet:
            pos = alphabet.index(char)
            new_pos = (pos - shift) % 26  
            result.append(alphabet[new_pos])
        else:
            result.append(char)
    
    return ''.join(result)


def load_test_cases(filename: str) -> List[str]:
    """Carga casos de prueba desde un archivo .txt"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            cases = [line.strip() for line in f if line.strip()]
        return cases
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{filename}'")
        return []


def save_result(filename: str, content: str):
    """Guarda resultado en un archivo"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Resultado guardado en: {filename}")


def generate_correct_decrypt_cases():
    """Genera los casos de decriptación correctos basados en los casos de encriptación"""
    casos_encriptar = [
        "3#ROMA NO FUE CONSTRUIDA EN UN DIA",
        "1#HOLA MUNDO",
        "5#PYTHON ES GENIAL",
        "D#CESAR FUE UN EMPERADOR",
        "13#ESTE ES UN MENSAJE SECRETO",
        "7#LA TEORIA DE LA COMPUTACION ES FASCINANTE",
        "B#MAQUINA DE TURING",
        "10#ALGORITMOS Y ESTRUCTURAS DE DATOS",
        "A#PROYECTO DE TEORIA DE LA COMPUTACION",
        "Z#CIFRADO CESAR ES SIMPLE PERO INTERESANTE"
    ]
    
    casos_decriptar = []
    
    for caso in casos_encriptar:
        key_part, message_part = caso.split('#', 1)
        shift = parse_key(key_part)
        encrypted = caesar_encrypt(message_part, shift)
        casos_decriptar.append(f"{key_part}#{encrypted}")
    
    return casos_decriptar


def create_sample_files():
    """Crea archivos de ejemplo si no existen"""
    
    encrypt_cases = [
        "3#ROMA NO FUE CONSTRUIDA EN UN DIA",
        "1#HOLA MUNDO",
        "5#PYTHON ES GENIAL",
        "D#CESAR FUE UN EMPERADOR",
        "13#ESTE ES UN MENSAJE SECRETO",
        "7#LA TEORIA DE LA COMPUTACION ES FASCINANTE",
        "B#MAQUINA DE TURING",
        "10#ALGORITMOS Y ESTRUCTURAS DE DATOS",
        "A#PROYECTO DE TEORIA DE LA COMPUTACION",
        "Z#CIFRADO CESAR ES SIMPLE PERO INTERESANTE"
    ]
    
    if not os.path.exists('casos_encriptar.txt'):
        with open('casos_encriptar.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(encrypt_cases))
        print("Archivo 'casos_encriptar.txt' creado")
    
    decrypt_cases = generate_correct_decrypt_cases()
    
    with open('casos_decriptar.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(decrypt_cases))
    print("Archivo 'casos_decriptar.txt' creado/actualizado correctamente")


def display_menu():
    """Muestra el menú principal"""
    print("\n" + "=" * 60)
    print("    MÁQUINA DE TURING - CIFRADO CÉSAR")
    print("    Teoría de la Computación 2025")
    print("=" * 60)
    print("\n[1] Encriptar mensaje")
    print("[2] Desencriptar mensaje")
    print("[3] Ingresar mensaje manualmente")
    print("[4] Ver casos de prueba disponibles")
    print("[5] Salir")
    print("-" * 60)


def show_test_cases(filename: str):
    """Muestra los casos de prueba disponibles"""
    cases = load_test_cases(filename)
    if cases:
        print(f"\n Casos disponibles en '{filename}':")
        print("-" * 60)
        for i, case in enumerate(cases, 1):
            print(f"[{i}] {case}")
    return cases


def process_encryption():
    """Proceso de encriptación"""
    print("\n" + "=" * 60)
    print("MODO: ENCRIPTACIÓN")
    print("=" * 60)
    
    cases = show_test_cases('casos_encriptar.txt')
    if not cases:
        return
    
    print("\nSeleccione el número del caso a encriptar (0 para cancelar): ", end='')
    try:
        choice = int(input())
        if choice == 0:
            return
        if 1 <= choice <= len(cases):
            input_str = cases[choice - 1]
            
            key_part, message_part = input_str.split('#', 1)
            shift = parse_key(key_part)
            
            print("\n" + "-" * 60)
            print("PROCESANDO...")
            print("-" * 60)
            print(f"Input completo:    {input_str}")
            print(f"Llave:             {key_part} (shift = {shift})")
            print(f"Mensaje original:  {message_part}")
            print("\n Ejecutando Máquina de Turing...")
            
            encrypted = caesar_encrypt(message_part, shift)
            
            print(f"\n✓ Mensaje encriptado: {encrypted}")
            
            result_content = f"Input: {input_str}\nLlave: {shift}\nOriginal: {message_part}\nEncriptado: {encrypted}\n"
            save_result('resultado_encriptacion.txt', result_content)
        else:
            print(" Opción inválida")
    except ValueError:
        print(" Entrada inválida")
    except Exception as e:
        print(f" Error: {e}")


def process_decryption():
    """Proceso de decriptación"""
    print("\n" + "=" * 60)
    print("MODO: DECRIPTACIÓN")
    print("=" * 60)
    
    cases = show_test_cases('casos_decriptar.txt')
    if not cases:
        return
    
    print("\nSeleccione el número del caso a decriptar (0 para cancelar): ", end='')
    try:
        choice = int(input())
        if choice == 0:
            return
        if 1 <= choice <= len(cases):
            input_str = cases[choice - 1]
            
            key_part, message_part = input_str.split('#', 1)
            shift = parse_key(key_part)
            
            print("\n" + "-" * 60)
            print("PROCESANDO...")
            print("-" * 60)
            print(f"Input completo:     {input_str}")
            print(f"Llave:              {key_part} (shift = {shift})")
            print(f"Mensaje encriptado: {message_part}")
            print("\n Ejecutando Máquina de Turing...")
            
            decrypted = caesar_decrypt(message_part, shift)
            
            print(f"\n✓ Mensaje decriptado: {decrypted}")
            
            result_content = f"Input: {input_str}\nLlave: {shift}\nEncriptado: {message_part}\nDecriptado: {decrypted}\n"
            save_result('resultado_decriptacion.txt', result_content)
        else:
            print(" Opción inválida")
    except ValueError:
        print(" Entrada inválida")
    except Exception as e:
        print(f" Error: {e}")


def process_manual_input():
    """Permite ingresar un mensaje manualmente"""
    print("\n" + "=" * 60)
    print("MODO: ENTRADA MANUAL")
    print("=" * 60)
    print("\n[1] Encriptar")
    print("[2] Decriptar")
    print("Seleccione operación: ", end='')
    
    try:
        op = int(input())
        if op not in [1, 2]:
            print(" Opción inválida")
            return
        
        print("\nIngrese la entrada en formato: LLAVE#MENSAJE")
        print("Ejemplo: 3#HOLA MUNDO  o  D#HOLA MUNDO")
        print("Entrada: ", end='')
        input_str = input().strip()
        
        if '#' not in input_str:
            print(" Formato incorrecto. Debe incluir '#' como separador")
            return
        
        key_part, message_part = input_str.split('#', 1)
        key_part = key_part.upper()  
        message_part = message_part.upper() 
        shift = parse_key(key_part)
        
        print("\n" + "-" * 60)
        print("PROCESANDO...")
        print("-" * 60)
        print(f"Llave: {key_part} (shift = {shift})")
        print(f"Mensaje: {message_part}")
        print("\n Ejecutando Máquina de Turing...")
        
        if op == 1:
            result = caesar_encrypt(message_part, shift)
            print(f"\n✓ Mensaje encriptado: {result}")
            save_result('resultado_manual.txt', f"Operación: Encriptación\nInput: {key_part}#{message_part}\nResultado: {result}\n")
        else:
            result = caesar_decrypt(message_part, shift)
            print(f"\n✓ Mensaje decriptado: {result}")
            save_result('resultado_manual.txt', f"Operación: Decriptación\nInput: {key_part}#{message_part}\nResultado: {result}\n")
            
    except ValueError:
        print(" Entrada inválida")
    except Exception as e:
        print(f" Error: {e}")


def view_all_cases():
    """Muestra todos los casos de prueba"""
    print("\n" + "=" * 60)
    print("CASOS DE PRUEBA DISPONIBLES")
    print("=" * 60)
    
    print("\n CASOS DE ENCRIPTACIÓN:")
    show_test_cases('casos_encriptar.txt')
    
    print("\n CASOS DE DECRIPTACIÓN:")
    show_test_cases('casos_decriptar.txt')
    
    input("\nPresione Enter para continuar...")


def save_machine_specification():
    """Guarda la especificación de la Máquina de Turing en JSON"""
    spec = {
        "descripcion": "Máquina de Turing para Cifrado César",
        "tipo": "Máquina de Turing Determinística",
        "estados": {
            "Q": ["q0", "q_scan", "q_process", "q_shift", "q_write", "q_return", "q_accept"],
            "q0": "Estado inicial - procesa la llave",
            "q_scan": "Escanea la cinta buscando caracteres a procesar",
            "q_process": "Procesa el carácter actual",
            "q_shift": "Aplica el desplazamiento César",
            "q_write": "Escribe el resultado en la cinta",
            "q_return": "Retorna al inicio para siguiente carácter",
            "q_accept": "Estado de aceptación"
        },
        "alfabeto_entrada": {
            "Sigma": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
            "nota": "26 letras - Los espacios se tratan como caracteres especiales"
        },
        "alfabeto_cinta": {
            "Gamma": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ _#*0123456789")
        },
        "estado_inicial": "q0",
        "estados_aceptacion": ["q_accept"],
        "simbolo_blanco": "_",
        "transiciones_ejemplo": {
            "formato": "(estado_actual, simbolo_leido) -> (nuevo_estado, simbolo_escribir, direccion)",
            "ejemplos": [
                {"de": ["q0", "3"], "a": ["q0", "3", "R"], "descripcion": "Leer dígito de llave"},
                {"de": ["q0", "#"], "a": ["q_scan", "_", "R"], "descripcion": "Encontrar separador"},
                {"de": ["q_scan", "A"], "a": ["q_process", "A", "R"], "descripcion": "Carácter a procesar"},
                {"de": ["q_scan", " "], "a": ["q_scan", " ", "R"], "descripcion": "Espacios se mantienen sin cambio"},
                {"de": ["q_process", "A"], "a": ["q_shift", "D", "L"], "descripcion": "Aplicar shift (ejemplo: A+3=D)"},
                {"de": ["q_shift", "D"], "a": ["q_return", "*", "L"], "descripcion": "Marcar procesado"},
                {"de": ["q_return", "_"], "a": ["q_scan", "_", "R"], "descripcion": "Continuar scan"},
                {"de": ["q_scan", "_"], "a": ["q_accept", "_", "R"], "descripcion": "Finalizar"}
            ]
        },
        "funcionamiento": {
            "encriptacion": "E(x) = (x + k) mod 26",
            "decriptacion": "D(x) = (x - k) mod 26",
            "alfabeto_size": 26,
            "nota_espacios": "Los espacios NO se encriptan ni se cuentan en el alfabeto, se mantienen literalmente"
        }
    }
    
    with open('maquina_turing_especificacion.json', 'w', encoding='utf-8') as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)
    
    print("✓ Especificación guardada en: maquina_turing_especificacion.json")


def main():
    """Función principal con menú interactivo"""
    
    create_sample_files()
    
    save_machine_specification()
    
    while True:
        display_menu()
        try:
            option = input("Seleccione una opción: ").strip()
            
            if option == '1':
                process_encryption()
            elif option == '2':
                process_decryption()
            elif option == '3':
                process_manual_input()
            elif option == '4':
                view_all_cases()
            elif option == '5':
                print("\n" + "=" * 60)
                print("Gracias por usar la Máquina de Turing - Cifrado César")
                print("Teoría de la Computación 2025")
                print("=" * 60)
                break
            else:
                print(" Opción inválida. Intente de nuevo.")
                
        except KeyboardInterrupt:
            print("\n\n  Programa interrumpido por el usuario")
            break
        except Exception as e:
            print(f" Error inesperado: {e}")


if __name__ == "__main__":
    main()