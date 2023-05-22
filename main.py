import textwrap

from commands import own_profile, user_profile, collection, own_collections, user_collections, own_likes, user_likes, json_file, links_from_txt

if __name__ == "__main__":
    print("https://github.com/ShineAsNine/GfycatDownloader\n")
    input_string = "Select a download type:\n 1) Own Profile\n 2) User Profile\n 3) Single Collection\n 4) Own Collections\n 5) User Collections\n 6) Own Likes\n 7) User Likes\n 8) JSON File\n 9) Text File\n (1, 2, 3, 4, 5, 6, 7, 8, 9): "

    download_type = input(textwrap.dedent(input_string))
    while download_type not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        print(f"Error: {download_type} is not one of '1', '2', '3', '4', '5', '6', '7', '8', '9'.")
        download_type = input(textwrap.dedent(input_string))

    if download_type == "1":
        own_profile.own_profile()
    elif download_type == "2":
        user_profile.user_profile()
    elif download_type == "3":
        collection.collection()
    elif download_type == "4":
        own_collections.own_collections()
    elif download_type == "5":
        user_collections.user_collections()
    elif download_type == "6":
        own_likes.own_likes()
    elif download_type == "7":
        user_likes.user_likes()
    elif download_type == "8":
        json_file.json_file()
    elif download_type == "9":
        links_from_txt.links_from_txt()
