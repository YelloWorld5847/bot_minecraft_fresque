# créer une annimation

# si il y a trop de command il cré un autre fichier
# inversé le sens de création de la fresue
# de bas en haut
import os
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt


def create_mcfunction_file(commands, dire_name, i_file=0, fonction_liste=None, dir_name_path="commands_folder", name=None):
    # folder_path = r"C:\Users\Lean\AppData\Local\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\development_behavior_packs\function\functions"
    # dir_name_path = os.path.join(folder_path, dir_name)
    # dir_name2 = dir_name
    # counter = 1
    # while os.path.exists(dir_name_path):
    #     dir_name2 = f"{dir_name}({counter})"
    #     dir_name_path = os.path.join(folder_path, dir_name2)
    #     counter += 1
    # os.makedirs(dir_name_path)

    chunk_size = 9999
    num_files = (len(commands) // chunk_size) + (1 if len(commands) % chunk_size > 0 else 0)

    for i in range(num_files):
        start = i * chunk_size
        end = (i + 1) * chunk_size
        chunk = commands[start:end]
        if name == None:
            file_name = f"{dir_name_path}/commands_{i + 1 + i_file}.mcfunction"
        else:
            file_name = f"{dir_name_path}/{name}.mcfunction"

        if fonction_liste != None:
            fonction_liste.append(f"function {dire_name}/commands_{i + 1 + i_file}") # {file_name.replace('.mcfunction', '')}")

        with open(file_name, "w") as f:
            for command in chunk:
                f.write(command + "\n")
                if command[len(command) - 1] == "0":
                    print(command)
        print(f"Fichier '{dire_name}/commands_{i}' créé avec {len(chunk)} commandes.")

    return fonction_liste


def image(pixel_size, colors_lego_plate_1x1, input_image_path, i_image):
    global output_image
    input_image = Image.open(input_image_path)
    pixel_array = np.array(input_image)
    output_image = Image.new("RGBA", input_image.size, color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(output_image)

    largeur = int(input_image.size[0] / pixel_size)
    hauteur = int(input_image.size[1] / pixel_size)
    matrice = [[0] * largeur for _ in range(hauteur)]

    # Inverser le sens de création (de bas en haut)
    for i in range(hauteur - 1, -1, -1):  # Parcours de bas en haut
        print(f"{100 - round(i / (hauteur) * 100)}%")
        for j in range(largeur):
            y_pixel = i * pixel_size
            x_pixel = j * pixel_size
            current_color = pixel_array[y_pixel, x_pixel][:3]  # Obtenir la couleur RGB du pixel

            # Trouver la couleur la plus proche dans la liste de couleurs
            closest_color_name = min(colors_lego_plate_1x1, key=lambda x: np.linalg.norm(
                np.array(colors_lego_plate_1x1[x]) - np.array(current_color)))

            # Récupérer le nom du fichier sans l'extension
            nom_fichier = os.path.splitext(os.path.basename(closest_color_name))[0]
            matrice[i][j] = nom_fichier  # Assignation dans la matrice

            # Dessiner un pixel avec la couleur la plus proche
            draw.rectangle([(x_pixel, y_pixel), (x_pixel + pixel_size - 1, y_pixel + pixel_size - 1)],
                           fill=tuple(colors_lego_plate_1x1[closest_color_name]))

    if i_image == 0:
        # Afficher l'image pixelisée
        plt.imshow(output_image)
        plt.axis('off')  # Désactiver les axes
        plt.show()

    # Créer les commandes pour Minecraft
    commands = []
    count = 0

    for i, ligne in enumerate(matrice):
        for j, element in enumerate(ligne):
            # text = fr"setblock ~{-j + (largeur // 2)} ~{-i + hauteur - 1} ~{50} {element}"
            text = fr"setblock {-1700 + -j} {-60 + -i + hauteur - 1} {-142} {element}"
            commands.append(text)
            count += 1

    print(f"Nombre de blocs : {count}")
    return commands


def main(path):
    # Vérifie si c'est un fichier
    if os.path.isfile(path):
        print("C'est un fichier.")
        all_path = [path]
    # Vérifie si c'est un dossier
    elif os.path.isdir(path):
        print("C'est un dossier.")
        all_path = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    else:
        print("Ce chemin n'existe pas ou n'est ni un fichier ni un dossier.")
        return

    image_path = all_path[0]
    # Ouvrir l'image à partir du chemin d'accès
    input_image = Image.open(image_path)
    print(f'taille : {input_image.size}')

    taille_moyenne = (input_image.size[0] + input_image.size[1]) / 2
    print(f"moyenne taille : ' {taille_moyenne} '")

    name = input("nom de la fonction :")
    nombre_pixel = int(input("nombre de pixel ?"))

    size = taille_moyenne / nombre_pixel
    largeur = int(input_image.size[0] / size) + 1
    hauteur = int(input_image.size[1] / size) + 1

    print(fr'largeur : {largeur} | hauteur : {hauteur}')
    print(f"nombre de block ,: {largeur * hauteur}")
    size = int(size)
    test = size * nombre_pixel

    folder_path = r"C:\Users\Lean\AppData\Local\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\development_behavior_packs\function\functions"
    dir_name_path = os.path.join(folder_path, name)
    dir_name = name
    counter = 1
    while os.path.exists(dir_name_path):
        dir_name = f"{name}({counter})"
        dir_name_path = os.path.join(folder_path, dir_name)
        counter += 1
    os.makedirs(dir_name_path)
    print(f"dire name path = {dir_name_path}")

    fonction_liste = []

    for i, image_path in enumerate(all_path):
        # Appeler la fonction image avec les paramètres nécessaires
        commands = image(size, liste_couleurs, image_path, i)

        fonction_liste = create_mcfunction_file(commands, dir_name, i, fonction_liste, dir_name_path)

    create_mcfunction_file(fonction_liste, dir_name, dir_name_path=dir_name_path, name="main")


# Code principal
input_image_path = r"C:\Users\Lean\Pictures\programme\image\lambo.jpg"

liste_couleurs = {
"acacia_planks.webp": [168, 90, 50],
"allow.webp": [137, 115, 82],
"amethyst_block.webp": [133, 97, 191],
"ancient_debris.webp": [95, 63, 55],
"bamboo_planks.webp": [193, 173, 80],
"basalt.webp": [73, 72, 77],
"bedrock.webp": [85, 85, 85],
"beehive.webp": [159, 128, 77],
"birch_planks.webp": [192, 175, 121],
"blackstone.webp": [42, 35, 40],
"black_concrete.webp": [1, 2, 6],
# "black_shulker_box.webp": [12, 13, 18],
"black_wool.webp": [12, 13, 18],
# "BlockSprite_packed-ice.webp": [141, 180, 250],
"blue_concrete.webp": [40, 42, 144],
# "blue_ice.webp": [116, 167, 253],
# "blue_shulker_box.webp": [33, 35, 128],
"blue_wool.webp": [50, 54, 158],
"bone_block.webp": [229, 225, 207],
"brick_block.webp": [150, 97, 83],
"brown_concrete.webp": [96, 57, 25],
"brown_mushroom_block.webp": [149, 111, 81],
# "brown_shulker_box.webp": [98, 58, 26],
"brown_wool.webp": [114, 70, 36],
"calcite.webp": [223, 224, 220],
"cherry_planks.webp": [226, 178, 172],
"chiseled_deepslate.webp": [48, 48, 48],
"clay.webp": [160, 166, 179],
"coal_block.webp": [16, 15, 15],
"cobbled_deepslate.webp": [77, 77, 80],
"cobblestone.webp": [119, 119, 119],
# "composter.webp": [112, 70, 31],
"cracked_deepslate_tiles.webp": [52, 52, 52],
"cracked_polished_blackstone_bricks.webp": [44, 37, 43],
"crimson_planks.webp": [101, 48, 70],
"crying_obsidian.webp": [32, 10, 60],
"cyan_concrete.webp": [13, 120, 137],
# "cyan_shulker_box.webp": [9, 110, 125],
"cyan_wool.webp": [13, 138, 146],
"dark_oak_planks.webp": [66, 43, 20],
"deepslate.webp": [80, 80, 82],
"deepslate_bricks.webp": [70, 70, 71],
"deepslate_tiles.webp": [54, 54, 55],
"diamond_block.webp": [98, 237, 228],
"dirt.webp": [134, 96, 67],
"dirt_with_roots.webp": [144, 103, 76],
"dispenser.webp": [122, 121, 121],
"dried_kelp_block.webp": [38, 48, 29],
"dripstone_block.webp": [134, 107, 92],
"dropper.webp": [122, 121, 121],
"emerald_block.webp": [42, 203, 87],
"end_bricks.webp": [218, 224, 162],
# "frosted_ice.webp": [141, 181, 253],
"gold_block.webp": [246, 208, 61],
"gray_concrete.webp": [51, 55, 59],
# "gray_shulker_box.webp": [46, 49, 53],
"gray_wool.webp": [60, 66, 70],
"green_concrete.webp": [72, 91, 31],
# "green_shulker_box.webp": [73, 94, 26],
"green_wool.webp": [84, 110, 20],
"hardened_clay.webp": [152, 94, 67],
"hay_block.webp": [166, 136, 38],
"honeycomb_block.webp": [229, 148, 29],
# "honey_block.webp": [245, 162, 33],
# "ice.webp": [146, 184, 255],
"iron_block.webp": [220, 220, 220],
"jungle_planks.webp": [160, 115, 80],
"lapis_block.webp": [30, 67, 140],
"light_blue_concrete.webp": [30, 138, 199],
# "light_blue_shulker_box.webp": [38, 151, 203],
"light_blue_wool.webp": [55, 176, 218],
"light_gray_concrete.webp": [126, 126, 116],
# "light_gray_shulker_box.webp": [111, 111, 102],
"light_gray_wool.webp": [143, 143, 135],
"lime_concrete.webp": [94, 169, 16],
# "lime_shulker_box.webp": [88, 157, 12],
"lime_wool.webp": [248, 198, 34],
"log.webp": [109, 85, 50],
"log2.webp": [103, 96, 86],
"magenta_concrete.webp": [170, 45, 160],
# "magenta_shulker_box.webp": [164, 45, 155],
"magenta_wool.webp": [190, 67, 180],
"mangrove_planks.webp": [117, 54, 48],
"melon_block.webp": [114, 146, 30],
"mossy_cobblestone.webp": [110, 118, 94],
"moss_block.webp": [89, 109, 45],
"netherite_block.webp": [66, 61, 63],
"netherrack.webp": [97, 38, 38],
"nether_brick.webp": [44, 21, 26],
"nether_wart_block.webp": [114, 2, 2],
"noteblock.webp": [88, 58, 40],
"oak_planks.webp": [162, 130, 78],
"obsidian.webp": [15, 10, 24],
"ochre_froglight.webp": [245, 233, 181],
"orange_concrete.webp": [225, 97, 0],
# "orange_shulker_box.webp": [219, 97, 1],
"orange_wool.webp": [241, 118, 12],
"pearlescent_froglight.webp": [235, 224, 228],
"pink_concrete.webp": [214, 101, 143],
# "pink_shulker_box.webp": [218, 109, 147],
"pink_wool.webp": [238, 142, 173],
"polished_basalt.webp": [88, 88, 91],
"polished_deepslate.webp": [71, 71, 71],
"pumpkin.webp": [195, 114, 24],
"purple_concrete.webp": [100, 25, 157],
"purple_wool.webp": [122, 37, 173],
"purpur_block.png": [169, 125, 169],
"quartz_block.webp": [235, 229, 222],
"quartz_bricks.webp": [234, 229, 221],
"raw_copper_block.webp": [154, 105, 79],
"raw_gold_block.webp": [221, 169, 46],
"raw_iron_block.webp": [166, 135, 107],
"redstone_block.webp": [175, 24, 5],
"red_concrete.webp": [143, 27, 27],
"red_mushroom_block.webp": [200, 46, 45],
"red_nether_brick.webp": [69, 7, 9],
"red_sandstone.webp": [186, 99, 29],
# "red_shulker_box.webp": [129, 19, 19],
"red_wool.webp": [161, 34, 29],
"sandstone.webp": [216, 203, 155],
"sculk.webp": [12, 30, 36],
"sealantern.webp": [171, 201, 190], #
# "slime.webp": [112, 193, 92],
"smooth_basalt.webp": [72, 72, 78],
"smooth_stone.webp": [158, 158, 158],
"soul_sand.webp": [81, 62, 50],
"soul_soil.webp": [75, 57, 46],
"sponge.webp": [195, 192, 74],
"spruce_planks.webp": [114, 84, 48],
"stained_hardened_clay.webp": [152, 94, 67],
"stone.webp": [125, 125, 125],
"stonebrick.webp": [122, 121, 122],
# "stone_pressure_plate.webp": [95, 95, 95],
"stripped_acacia_log.webp": [174, 92, 59],
"stripped_birch_log.webp": [196, 176, 118],
"stripped_crimson_stem.webp": [137, 57, 90],
"stripped_dark_oak_log.webp": [72, 56, 36],
"stripped_jungle_log.webp": [169, 132, 83],
"stripped_oak_log.webp": [177, 144, 86],
"stripped_spruce_log.webp": [115, 89, 52],
"stripped_warped_stem.webp": [57, 150, 147],
"tuff.webp": [108, 109, 102],
# "undyed_shulker_box.webp": [140, 97, 140],
"polished_blackstone.webp": [53, 48, 56],
"verdant_froglight.webp": [211, 234, 208],
"warped_planks.webp": [43, 104, 99],
"warped_wart_block.webp": [22, 119, 121],
"white_concrete.webp": [208, 214, 215],
# "white_shulker_box.webp": [203, 208, 209],
"white_wool.webp": [234, 236, 237],
# "wooden_pressure_plate.webp": [125, 101, 61],
"yellow_concrete.webp": [241, 176, 13],
# "yellow_shulker_box.webp": [241, 180, 17],
"yellow_wool.webp": [248, 198, 34],
}




main(input_image_path)

