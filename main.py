import textwrap

from commands import own_profile, user_profile, collection, json_file, links_from_txt

if __name__ == "__main__":
    print("https://github.com/ShineAsNine/GfycatDownloader\n")
    input_string = "Select a download type:\n 1) Own Profile\n 2) User Profile\n 3) Collection\n 4) JSON File\n 5) Text File\n (1, 2, 3, 4, 5): "

    download_type = input(textwrap.dedent(input_string))
    while download_type not in ["1", "2", "3", "4", "5"]:
        print(f"Error: {download_type} is not one of '1', '2', '3', '4', '5'.")
        download_type = input(textwrap.dedent(input_string))

    if download_type == "1":
        own_profile.own_profile()
    elif download_type == "2":
        user_profile.user_profile()
    elif download_type == "3":
        collection.collection()
    elif download_type == "4":
        json_file.json_file()
    elif download_type == "5":
        links_from_txt.links_from_txt()
