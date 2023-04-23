# GfycatDownloader

Download the exe from [releases](https://github.com/ShineAsNine/GfycatDownloader/releases)
<br></br>
Types of downloads:
1) Own Profile
    - Requires an auth key.
    - Downloads public and private gfys of authenticated user.
    - Creates a folder using the user's profile name.
<br></br>
2) User Profile
    - Downloads only public gfys of the specified user.
    - Creates a folder using the user's profile name
<br></br>
3) Collection
    - Downloads all gfys inside a collection, public and private.
    - Creates a folder using the user's profile name and the collection ID
<br></br>
4) JSON File
    - When downloading using the first three types, a json file is created with info of all the gfys. If the download is interrupted midway, the already created json can be used to resume the download instead of requesting the gfys from Gfycat again.
    - No folder is created so the specific user/collection folder needs to be specified.
<br></br>
5) Text File
    - Downloads user profiles, collections, and single gfys from a text file. Put each url on a new line.
    - Creates folders based on the type of download. Single gfys are downloaded to the base output folder.
<br></br>

To get an auth key go to [Gfycat.com](https://gfycat.com/) while logged in, open dev tools, refresh the page, go to the network tab and look through the requests until you find one that has "Authorization" in the response headers, copy everything after "Bearer". That's the auth key and can be used to download your own gfys.

The default output template is `%(upload_date)s - %(title)s [%(gfy_id)s]`. Available options are `upload_date`, `title`, `gfy_id`, `likes`, `frame_rate`, `height`, `width`, `views`.