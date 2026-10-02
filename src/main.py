from pathlib import Path
import shutil


CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".ppt", ".pptx"],
    "Music": [".mp3", ".wav", ".flac", ".aac"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
}


def get_category(file_extension):
    for category, extensions in CATEGORIES.items():
        if file_extension in extensions:
            return category

    return "Other"


def get_unique_destination(destination):
    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = f"{destination.stem}_{counter}{destination.suffix}"
        new_destination = destination.parent / new_name

        if not new_destination.exists():
            return new_destination

        counter += 1


def organize_files(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        print("Error: Folder not found.")
        return

    if not folder.is_dir():
        print("Error: The provided path is not a folder.")
        return

    moved_count = 0

    for file in folder.iterdir():

        if not file.is_file():
            continue

        category = get_category(file.suffix.lower())

        destination_folder = folder / category
        destination_folder.mkdir(exist_ok=True)

        destination = destination_folder / file.name
        destination = get_unique_destination(destination)

        try:
            shutil.move(str(file), str(destination))

            print(f"Moved: {file.name} -> {category}/{destination.name}")
            moved_count += 1

        except Exception as error:
            print(f"Error moving {file.name}: {error}")

    print(f"\nOrganization completed. {moved_count} file(s) moved.")


if __name__ == "__main__":
    folder_path = input("Enter the folder path to organize: ").strip()

    organize_files(folder_path)