from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, error, USLT, Encoding
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4, MP4Cover
from mutagen import File

def analise_capa(music_path):
    audio = MP3(music_path)
    if audio.tags is None:
        print("❌ Esse arquivo não tem tags ID3.")
    else:
        apics = audio.tags.getall("APIC")
        if not apics:
            print("⚠️ Nenhuma capa foi encontrada.")
        else:
            print("✅ Capa encontrada!")
            print("Quantidade de capas:", len(apics))
            for i, apic in enumerate(apics, start=1):
                print(f"Capa {i}: tipo={apic.type}, mime={apic.mime}, tamanho={len(apic.data)} bytes")

def change_tags(music_path):
    if music_path.endswith(".mp3"):
        music = EasyID3(music_path)
        music["title"] = input("Digite o nome da musica: ")
        music["artist"] = input("Digite o nome do artista: ")
        music["album"] = input("Digite o nome da album: ")
        music["date"] = input("Digite a data: ")
        music.save()

    if music_path.endswith(".m4a"):
        music = MP4(music_path)
        music["\xa9nam"] = input("Digite o nome da musica: ")
        music["\xa9ART"] = input("Digite o nome do artista: ")
        music["\xa9alb"] = input("Digite o nome da album: ")
        music["\xa9day"] = input("Digite o ano: ")
        music.save()

    test = input("Deseja colocar uma imagem: ")

    if(test == "sim" or test=="s" or test=="yes" or test=="y"):
        add_cover(music_path)

def show_tags(music_path):
    music = File(music_path)
    for tag, valor in music.tags.items():
        if(tag!="covr"):
            print(tag, valor)

def add_cover(music_path):
    cover_path = input("Digite o caminho da imagem: ")
    format_cover = cover_path.split(".")
    if music_path.endswith(".mp3"):
        try:
            music = MP3(music_path, ID3=ID3)

            # Se o arquivo não tiver tags ID3, cria
            if music.tags is None:
                music.add_tags()

            # Lê a imagem em modo binário
            with open(cover_path, "rb") as img:
                capa = img.read()
            # Remove capas anteriores (opcional, pra evitar duplicadas)
            music.tags.delall("APIC")

            # Adiciona a nova capa
            music.tags.add(
                APIC(
                    encoding=3,          # UTF-8
                    mime="image/"+format_cover[len(format_cover)-1],   # ou "image/png" se for PNG
                    type=3,              # 3 = capa frontal
                    desc="Capa do álbum",
                    data=capa
                )
            )

            # Salva o arquivo modificado
            music.save()
            print("✅ Capa adicionada com sucesso!")

        except Exception as e:
            print(f"❌ Erro ao adicionar capa: {e}")
        # letra = input("Escreva a letra da musica: ")
        # music.add(USLT(encoding=Encoding.UTF8, lang="por", desc="letra", text=letra))
        music.save()
        
    if music_path.endswith(".m4a"):
        music = MP4(music_path)
        with open(cover_path, 'rb') as img:
            music["covr"] = [
                MP4Cover(img.read(), imageformat=MP4Cover.FORMAT_JPEG)
            ]
        # letra = input("Escreva a letra da musica: ")
        # music["\xa9lyr"] = [letra]
        music.save()

def main():
    print("Menu: ")
    print("1.Adicionar Tags")
    print("2.Adicionar capa")
    print("3.Exibir Tags da musica")

    indice = input("Digite uma opção: ")
    music_path = input("Escreva o caminho da musica: ")

    if indice == "1":
        change_tags(music_path)
    elif indice == "2":
        add_cover(music_path)
    elif indice == "3":
        show_tags(music_path)
    elif indice == "4":
        analise_capa(music_path)

if __name__ == "__main__":
    main()
