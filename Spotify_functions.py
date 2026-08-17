import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import Utilities

load_dotenv()  # Carga las variables de entorno desde el archivo .env
CLIENT_id= os.getenv("CLIENT_ID")
SECRET_CLIENT= os.getenv("SECRET_CLIENT")
REDIRECT_URI= os.getenv("REDIRECT_URI")
PLAYLIST_IDs= os.getenv("PLAYLIST_IDS").split(',')
if not CLIENT_id or not SECRET_CLIENT or not REDIRECT_URI or not PLAYLIST_IDs:
    raise ValueError("Una o más variables de entorno no encontradas en .env")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id= CLIENT_id,
    client_secret= SECRET_CLIENT,
    redirect_uri= REDIRECT_URI,
    scope= "user-modify-playback-state user-read-playback-state"
))

def obtener_disp_activo():
    devices = sp.devices()
    for device in devices['devices']:
        if device['is_active']: 
            return device['id']

def playback_manage(action: str) -> str: 
    ''' ## Gestiona la reproducción de Spotify
        ### Argumentos:
        1- **action**: *(string)* acción a realizar: 'pause', 'start', 'anterior', 'siguiente' '''
    active_disp= obtener_disp_activo()
    if action.lower() == 'pause':
        sp.pause_playback(device_id= active_disp)
        return "Reproducción pausada"
    if action.lower() == 'start':
        sp.start_playback(device_id= active_disp)
        return "Reproducción iniciada"
    if action.lower() == 'anterior':
        sp.previous_track(device_id= active_disp)
        return "Pista anterior reproducida"
    if action.lower() == 'siguiente':
        sp.next_track(device_id= active_disp)
        return "Siguiente pista reproducida"

def search_and_start_song(search: str) -> str:
    ''' ## Busca una canción dentro de las playlists cacheadas y la reproduce
        ### Argumentos:
        1- **search**: *(string)* busqueda exacta del usuario para la canción. Si es un nombre 
        en japonés romanizado, traducelo a japonés antes de buscar. '''
    fe= Utilities.open_file(
        ruta= Utilities.get_path_to_parent_dict(__file__, 'cache', 'playlists.json'),
        do= 'read_json',
    )
    found= False 
    palabras= search.lower().split()
    song_data= None
    for k, v in fe.items():
        if found: break
        songs: dict= v['songs']
        for uri, dats in songs.items(): 
            if set(palabras).issubset(set(dats['name'].lower().split())):
                song_data= {'on_playlist' : {'uri' : k, 'name' : v['name']}, 'name' : dats['name'], 'uri': uri, 'artist' : dats['artist']}
                found= True
                break
            else: 
                continue

    if not found: 
        return 'No se encontró la canción dentro de las playlists'
    if song_data and found:
        sp.start_playback(device_id= obtener_disp_activo(), context_uri= song_data['on_playlist']['uri'], offset= {'uri' : song_data['uri']})
        return f"Reproduciendo {song_data['name']} -> artist: {song_data['artist']} (playlist: {song_data['on_playlist']['name']})"

def update_cached_songs(): 
    fac= {}
    for pid in PLAYLIST_IDs:
        playlist= sp.playlist(pid)
        playlist_name= playlist.get('name') if playlist else None
        playlist_uri= playlist.get('uri') if playlist else None
        results = sp.playlist_items(playlist_id=pid)
        tracks: list= results['items']
        if results['next']:
            while results['next']: 
                results= sp.next(results)
                tracks.extend(results['items'])

        songs_on_playlist= {}
        for item in tracks: 
            song= item.get('item')
            name= song.get('name') if song else None
            uri= song.get('uri') if song else None
            artists= song.get('artists', []) if song else None
            first_artist= artists[0]['name'] if artists else 'Artista desconocido'
            if not song:
                continue
            songs_on_playlist[uri] = {'name' : name, 'artist' : first_artist}
        if playlist_uri: 
            fac[playlist_uri]= {'name' : playlist_name, 'songs' : songs_on_playlist}

    Utilities.open_file(
        ruta= Utilities.get_path_to_parent_dict(__file__, 'cache', 'playlists.json'),
        do= 'json_dump',
        modo= 'w',
        values_to_dump= fac)

update_cached_songs()