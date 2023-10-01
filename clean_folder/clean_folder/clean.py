import pathlib                    # import pathlib -> home_dir => pathlib.Path.home()

# from pathlib import Path        # from pathlib import Path => home_dir = Path.home()
# from pathlib import *           # from pathlib import *  => current_dir = Path.cwd()
import shutil

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s",
               "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

suffix_dict = {
    'JPEG': 'images', 'PNG': 'images', 'JPG': 'images', 'SVG': 'images', 'BMP': 'images',
    'AVI': 'video', 'MP4': 'video', 'MOV': 'video', 'MKV': 'video',
    'DOC': 'documents', 'DOCX': 'documents', 'TXT': 'documents', 'PDF': 'documents', 
    'XLS': 'documents', 'XLSX': 'documents', 'PPTX': 'documents', 
    'MP3': 'audio', 'OGG': 'audio', 'WAV': 'audio', 'AMR': 'audio',
    'ZIP': 'archives', 'GZ': 'archives', 'TAR': 'archives',
}
files_dict = {'images': [], 'video': [], 'documents': [],
              'audio': [], 'archives': [], 'unknown': []}
known_suffix = set()
unknown_suffix = set()
folders_list = []


def write_dict(path):  # save files_dict, known_suffix, unknown_suffix
    with open(path / "TS_FileList.txt", 'w') as f:
        for categ in files_dict.keys():
            if len(files_dict[categ]) > 0:
                f.write(f'>>> {categ}\n')
                for file in files_dict[categ]:
                    f.write(f'{file}\n')  # f.write(f'{file.name}\n')

    with open(path / "TS_SuffixKnown.txt", 'w') as f:
        for suf in known_suffix:
            f.write(f'{suf}\n')

    with open(path / "TS_SuffixUnknown.txt", 'w') as f:
        for suf in unknown_suffix:
            f.write(f'{suf}\n')
    
    with open(path / "TS_FoldersList.txt", 'w') as f:
        for fold in folders_list:
            f.write(f'{len(fold.parts):2}  {fold}\n')


def normalize(name):
    newname = ""
    for ch in name:
        newname += (ch if ch.isalnum() else '_')

    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    return newname.translate(TRANS)


def select_file(path):  # fill files_dict() depending on category of file suffix
    suf = path.suffix[1:].upper()
    categ = suffix_dict.get(suf)
    if categ:
        # print(f'{categ=}')
        files_dict[categ].append(path)
        known_suffix.add(suf)
    else:
        files_dict['unknown'].append(path)
        unknown_suffix.add(suf)


def view_folder(path):  # view & preparing files & folders to further processing
    print(f":: view_folder:  {path=}")
    for file in path.iterdir():
        if file.is_dir():
            #print(f"folder.is_dir: {file.name=}")
            folders_list.append(file)
            view_folder(file) 
        else:
            select_file(file)
    folders_list.sort(key=lambda Path: len(Path.parts), reverse = True)
    

def check_folders(path):  # create & fill new folder for nonempty category
    print(f"\n>>> check_folders: {path=}")
    for categ in files_dict.keys():
        if (categ != 'unknown') and (len(files_dict[categ]) > 0):      # not empty
            print(f"* mkdir: {path/categ}")
            try:
                pathlib.Path.mkdir(path/categ)
            except FileExistsError:
                continue


def move_files(path):
    print(f"\n>>> move_file: {path=}")
    for categ in files_dict.keys():
        print(f"{categ=}")
        for file in files_dict[categ]:
            print(f"* {file=}")
            stem = normalize(file.stem)
            #print(f"  normalize: {file.stem=} -> {stem=}")
            newname = (path/categ/(stem+file.suffix) if categ !='unknown' else file.parent/(stem+file.suffix))
            # if (categ != 'unknown'):
            #     newname = path / categ / (stem + file.suffix)           
            # else:
            #     newname = file.parent / (stem + file.suffix) 
            print(f" =>{newname=}")
            file.replace(newname)    # .replace(newname) doesn't need try..except


def unpack_archives(path):  # special remove archive files into archives folders
    print(f"\n>>> unpack_archives: {path=}")
    archivpath = path/'archives'
    if archivpath.exists():
        for arch in archivpath.iterdir():
            print(f"* {arch=}") 
            print(f" => {archivpath/arch.stem=}") 
            shutil.unpack_archive(arch, archivpath/arch.stem)
            pathlib.Path.unlink(arch)


def sweep_folders():
    print(f"\n>>> sweep_folders")
    
    #fill_folder(path)
    #folders_list.sort(key=lambda Path: len(Path.parts), reverse = True)
    #print(f"\n  folders_list was sorted")

    for fold in folders_list:
        print(f"{fold=}")
        if (fold.name not in files_dict.keys()):
            if any(fold.iterdir()):  # not empty => normalize
                print(f"*  normalise: {fold.name=}")
                newname = normalize(fold.name)
                if newname != fold.name:
                    try:
                        print(f"** try to rename as: {fold.parent / newname}")
                        fold.rename(fold.parent / newname)
                    except FileExistsError:
                        continue
            else:   # empty
                print(f"** rmdir: {fold.name=}")
                try:
                    pathlib.Path.rmdir(fold)
                except OSError:
                    continue


def main():
    print("\n\n>>> main <TrashSort>")
    # if len(sys.argv) < 2:
    #     print("ERROR: working directory not specified")
    #     exit()

    # workpath = pathlib.Path(sys.argv[1])
    workpath = pathlib.Path(r"d:/PYTHON/HomeWorks/Modul06/trash/")
    # print(f"'{workpath=}'  {workpath.exists()=}\n")
    # #'workpath=WindowsPath('e:/PROG/PYTHON/GoIt homeworks/HW1(Modul6)/trash')'
    if not workpath.exists():
        print(f"ERROR: working directory '{workpath}' not exist")
        exit()

    view_folder(workpath)
    write_dict(workpath)

    check_folders(workpath)
    move_files(workpath)
    unpack_archives(workpath)
    sweep_folders()
    

if __name__ == "__main__":
    main()

# nothing personal
# nothing extra
