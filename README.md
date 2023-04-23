# GfycatDownloader

Download the exe from [releases](https://github.com/ShineAsNine/GfycatDownloader/releases)
<br></br>
Types of downloads:
1) Own Profile
    - Requires an auth key.
    - Downloads public and private gfys of authenticated user.
<br></br>
2) User Profile
    - Downloads only public gfys of the specified user.
<br></br>
3) Collection
    - Downloads all gfys inside a collection, public and private.
<br></br>
4) JSON File
    - When downloading using the first three types, a json file is created with all the gfys info, if you cancel the download mid way you can use the already created json to resume the download instead of requesting the gfys from Gfycat again.
<br></br>
5) Text File
    - Downloads user profiles, collections, and single gfys from a text file. Put each url on a new line.
<br></br>

To get an auth key go to [Gfycat.com](https://gfycat.com/) while logged in, open dev tools, refresh the page, go to the network tab and look through the requests until you find one that has "Authorization" in the response headers, copy everything after "Bearer". That's the auth key and can be used to download your own gfys.

When downloading using 'Own Profile' or 'User Profile', a folder will be created using the users profile name. Downloading using 'Collection', a folder will be created using the users profile name and the collection ID. Downloading using a json file no folder is created so the specific user/collection folder needs to be specified. Downloading using a text file each sub type will be handled, user profile a folder will be created, collections a folder will be created, single gfys will be downloaded to the base output folder.
