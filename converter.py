import re
import xml.etree.ElementTree as ET
import os

# Função para extrair o valor do name dentro de Game.createMonsterType("...")
def extract_name(lua_text):
    pattern = r'Game\.createMonsterType\("(.+?)"\)'
    match = re.search(pattern, lua_text)
    if match:
        return match.group(1)
    return None

# Função para extrair outros valores do arquivo LUA
def extract_lua_value(lua_text, key):
    pattern = rf"{key}\s*=\s*(.*)"
    match = re.search(pattern, lua_text)
    if match:
        value = match.group(1).strip().strip(',').strip('"')
        return value
    return None

# Função para gerar o XML
def lua_to_xml(lua_file, to_folder):
    with open(lua_file, 'r') as f:
        lua_text = f.read()

    # Extraindo o nome (name) a partir de Game.createMonsterType("...")
    name = extract_name(lua_text)
    
    # Extraindo outros dados relevantes
    nameDescription = extract_lua_value(lua_text, 'monster.description')
    race = extract_lua_value(lua_text, 'monster.race')
    experience = extract_lua_value(lua_text, 'monster.experience')
    speed = extract_lua_value(lua_text, 'monster.speed')
    
    # Extraindo o "look" e "corpse"
    lookType = extract_lua_value(lua_text, 'lookType')
    lookHead = extract_lua_value(lua_text, 'lookHead')
    lookBody = extract_lua_value(lua_text, 'lookBody')
    lookLegs = extract_lua_value(lua_text, 'lookLegs')
    lookFeet = extract_lua_value(lua_text, 'lookFeet')
    lookAddons = extract_lua_value(lua_text, 'lookAddons')
    lookMount = extract_lua_value(lua_text, 'lookMount')
    corpse = extract_lua_value(lua_text, 'monster.corpse')

    # Garantindo que os valores não sejam None
    name = name or "Unknown"
    nameDescription = nameDescription or "No description"
    race = race or "Unknown"
    experience = experience or "0"
    speed = speed or "0"
    lookType = lookType or "0"
    lookHead = lookHead or "0"
    lookBody = lookBody or "0"
    lookLegs = lookLegs or "0"
    lookFeet = lookFeet or "0"
    lookAddons = lookAddons or "0"
    lookMount = lookMount or "0"
    corpse = corpse or "0"

    # Criando o elemento raiz <monster>
    monster = ET.Element("monster", {
        "name": name,
        "nameDescription": nameDescription,
        "race": race,
        "experience": experience,
        "speed": speed
    })

    # Criando o elemento <look>
    look = ET.SubElement(monster, "look", {
        "type": lookType,
        "lookType": lookType,
        "lookHead": lookHead,
        "lookBody": lookBody,
        "lookLegs": lookLegs,
        "lookFeet": lookFeet,
        "lookAddons": lookAddons,
        "lookMount": lookMount,
        "corpse": corpse
    })

    # Criando o caminho do arquivo de saída XML na pasta "to"
    xml_filename = os.path.splitext(os.path.basename(lua_file))[0] + ".xml"
    xml_file = os.path.join(to_folder, xml_filename)

    # Salvando o XML com a codificação correta
    tree = ET.ElementTree(monster)
    with open(xml_file, "wb") as f:
        tree.write(f, encoding="UTF-8", xml_declaration=True)

    print(f"Arquivo XML gerado: {xml_file}")

# Função para converter todos os arquivos .lua da pasta 'from' e salvar em 'to'
def convert_all_files(from_folder, to_folder):
    # Verifica se a pasta de destino 'to' existe, caso contrário cria
    if not os.path.exists(to_folder):
        os.makedirs(to_folder)

    # Percorre todos os arquivos na pasta 'from'
    for filename in os.listdir(from_folder):
        if filename.endswith(".lua"):
            lua_file = os.path.join(from_folder, filename)
            lua_to_xml(lua_file, to_folder)

# Função principal
def main():
    from_folder = 'from'  # Pasta de origem
    to_folder = 'to'      # Pasta de destino

    convert_all_files(from_folder, to_folder)

if __name__ == "__main__":
    main()
