"""Settings for Development Server"""
from .base_settings import *  # noqa

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-#h8#5yy)jsc@sa+r(1t@f^$)(fs(36&q@8l^+&6=c^0r)jk&)4"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# The Debug Toolbar is shown only if your IP is listed in the INTERNAL_IPS setting.
# https://docs.djangoproject.com/en/2.0/ref/settings/#internal-ips
INTERNAL_IPS = ["127.0.0.1"]

# ============================================================
# DATABASE SETTINGS
# ============================================================

# https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

DATABASES = {
    'default': {
         'NAME': 'db.sqlite3',
         'ENGINE': 'django.db.backends.sqlite3',
     }
}

# DEFAULT_TABLESPACE = '/home/administrator/DJANGO/dtablespace'   #TODO

# # Configure as cache backend - see base settings
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         # "LOCATION": "redis://35.193.244.81:6379/0",          # 35.193.5.83:6379
#         # "LOCATION": "unix:/var/run/redis/redis-server.sock",              # see /etc/redis.conf
#         "LOCATION": "redis://127.0.0.1:6379/0",
#         "OPTIONS": {
#             #"CLIENT_CLASS": "django_redis.client.DefaultClient",
#             # "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
#             # "COMPRESSOR": "django_redis.compressors.lz4.Lz4Compressor",   import lz4
#             # "IGNORE_EXCEPTIONS": True,    # global version outside of this - DJANGO_REDIS_IGNORE_EXCEPTIONS = True
#             # "retry_on_timeout": True,
#             #"KEY_PREFIX": "cci"
#         }
#     }
# }
# ============================================================
# Leaflet stuff
# ============================================================
"""
UL: LON -98.606  LAT 39.622
UR: -41.391, 74.719
LL: 21.304, -80.446
LR: 21.304, 
ul: -141.785  57.814 Unknown Units
UR: -27.129  58.609 Unknown Units
LL: -142.808  -6.957 Unknown Units
LR: -142.808  -6.957 Unknown Units
center: -91.105  31.223 Unknown Units

LEAFLET_CONFIG = {

    'SPATIAL_EXTENT': (-154.609, 1.561, -40.611, 65.921),   # xmin,ymin,xmax,ymax -- leaflet_tags.leaflet_map reformat this to lat/long
    'DEFAULT_CENTER': (36.362, -96.941),
    'DEFAULT_ZOOM': 3,
    'MIN_ZOOM': 1,
    'MAX_ZOOM': 18,

    'ATTRIBUTION_PREFIX': 'Powered by Office of Water Prediction',
    'TILES': [
        ('Streets', 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                    {'attribution': '&copy; OpenStreet'}),
        ('World Imagery', 'http://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/MapServer/tile/{z}/{y}/{x}',
                          {"attribution": "ESRI", }),
        # ('Satellite', 'http://server/a/...', {'attribution': '&copy; Big eye', 'maxZoom': 16}),
    ],
    'OVERLAYS': [
        # Currently, overlay layers from settings are limited to tiles.
        # For vectorial overlays, you will have to add them via JavaScript (see events).
        # ('Cadastral', 'http://server/a/{z}/{x}/{y}.png', {'attribution': '&copy; IGN'}),
    ],
    'SCALE': 'both',
    'MINIMAP': False,
    'RESET_VIEW': True,
    'NO_GLOBALS': False,
    'FORCE_IMAGE_PATH': True,
    'PLUGINS': {
        'name-of-plugin': {
            # a relative URL - settings.STATIC_URL will be prepended
            # source: https://github.com/leplatrem/django-leaflet-geojson/pull/2/files
            # 'js': ['http://rawgithub.com/glenrobertson/leaflet-tilelayer-geojson/master/TileLayer.GeoJSON.js'],
            # 'js': ['http://unpkg.com/leaflet@1.3.1/dist/leaflet.js', 'js/leaflet-providers.js',],
            # 'auto-include': True
        },
    },
}
"""

try:
    from bazar_prj.settings_dir.local_settings import * # noqa
except ImportError:
    print("Error in bazar_prj.settings_dir.local_settings!!\n")
    pass


