from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, error, USLT, Encoding
from mutagen.mp4 import MP4, MP4Cover
from mutagen import File

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
        cover_path = input("Digite o caminho da imagem: ")
        if music_path.endswith(".mp3"):
            music = ID3(music_path)
            with open(cover_path, 'rb') as img:
                music.add(APIC(
                    encoding=3,
                    mime="image/jpeg",
                    type=3, desc=u"Capa",
                    data=img.read()

                ))
            letra = input("Escreva a letra da musica: ")
            music.add(USLT(encoding=Encoding.UTF8, lang="por", desc="letra", text=letra))
            music.save()
        
        if music_path.endswith(".m4a"):
            music = MP4(music_path)
            with open(cover_path, 'rb') as img:
                music["covr"] = [
                    MP4Cover(img.read(), imageformat=MP4Cover.FORMAT_JPEG)
                ]
            letra = input("Escreva a letra da musica: ")
            music["\xa9lyr"] = [letra]
            music.save()

def show_tags(music_path):
    music = File(music_path)
    for tag, valor in music.tags.items():
        if(tag!="covr"):
            print(tag, valor)


def main():
    print("Menu: ")
    print("1.Adicionar Tags")
    print("2.Exibir Tags da musica")

    indice = input("Digite uma opção: ")
    music_path = input("Escreva o caminho da musica: ")

    if indice == "1":
        change_tags(music_path)
    elif indice == "2":
        show_tags(music_path)

if __name__ == "__main__":
    main()
