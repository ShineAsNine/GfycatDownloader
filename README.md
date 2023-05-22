# GfycatDownloader

**With version 1.0.1 and 2.0.0 HTTPS / SSL Certificate verification is disabled making it possible to still download.**

Download from [releases](https://github.com/ShineAsNine/GfycatDownloader/releases)
<br></br>
Types of downloads:
1) Own Profile
    - Requires an auth key.
    - Downloads public and private gfys of authenticated user.
    - Creates a folder using the user's profile name.
<br></br>

2) User Profile
    - Downloads only public gfys of the specified user.
    - Creates a folder using the user's profile name.
<br></br>

3) Single Collection
    - Downloads public and private gfys inside of a public collection.
    - Creates a folder using the user's profile name and the collection ID.
<br></br>

4) Own Collections
    - Requires an auth key.
    - Downloads all collections public and private of authenticated user.
    - Creates indiviual folders for each collection using the user's profile name and collection ID.
    - One issue that can arise is that the auth key lasts for approximately one hour. If there are a lot public/private collections and the download time exceeds one hour, an "ExpiredOrInvalidAuthKey" error may occur. In such cases, the best solution would be to restart the download with a new auth key or make the collections public, removing the need for an auth key.
<br></br>

5) User Collections
    - Downloads all public collections of the specified user.
    - Creates indiviual folders for each collection using the user's profile name and collection ID.
<br></br>

6) Own Likes
    - Requires an auth key.
    - Downloads all of your public and private/hidden likes.
    - Creates a folder like `username - likes`
<br></br>

7) User Likes
    - Downloads the public likes of the specified user.
    - Creates a folder like `username - likes`
<br></br>

8) JSON File
    - When downloading using the first three types, a json file is created with info of all the gfys. If the download is interrupted midway, the already created json can be used to resume the download instead of requesting the gfys from Gfycat again.
    - No folder is created so the specific user/collection folder needs to be specified.
<br></br>
9) Text File
    - Downloads user profiles, collections, and single gfys from a text file. Put each url on a new line.
    - Creates folders based on the type of download. Single gfys are downloaded to the base output folder.
<br></br>

To get an auth key go to [Gfycat.com](https://gfycat.com/) while logged in, open dev tools, refresh the page, go to the network tab and look through the requests until you find one that has "Authorization" in the response headers, copy everything after "Bearer". That's the auth key and can be used to download your own gfys.

The default output template is `%(upload_date)s - %(title)s [%(gfy_id)s]`. Available options are `upload_date`, `title`, `gfy_id`, `likes`, `frame_rate`, `height`, `width`, `views`.