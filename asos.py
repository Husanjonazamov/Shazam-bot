from asyncio import run

from unittest import result

from shazamio import Shazam as Sh
 




class Shazam:
 
    @staticmethod
    def search(music, limit):
        return run(Shazam.search_async(music, limit))

    @staticmethod
    async def search_async(music, limit):
       shazam = Sh()
       results = await shazam.search_track(query=music, limit=limit)

       music_list = []

       print(results['tracks']['hits'])
       for track in results['tracks']['hits']:
           url = track['stores']['apple']['previewurl']
           title = track["heading"]['title']
           subtitle = track['heading']['subtitle']
           image = track['images']['default']
           track_id = track['key']
           music_list.append({"url": url, "title": title, "subtitle": subtitle, "image": image, "track_id": track_id})

       return music_list

    @staticmethod
    async def download(track_id):
        shazam = Sh()
        about_track = await shazam.track_about(track_id=track_id)

        return about_track['hub']['actions'][1]['uri']


#print(Shazam.search("Bass music",10))





