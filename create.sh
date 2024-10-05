# Create necessary directories if they don't exist
mkdir -p utils
mkdir -p ../tests
mkdir -p ../examples

# Only create files that do not exist already
[ ! -f __init__.py ] && touch __init__.py
[ ! -f base.py ] && touch base.py
[ ! -f instagram.py ] && touch instagram.py
[ ! -f youtube.py ] && touch youtube.py
[ ! -f tiktok.py ] && touch tiktok.py
[ ! -f twitter.py ] && touch twitter.py  # Optional

# Create utility files only if they don't exist
[ ! -f utils/__init__.py ] && touch utils/__init__.py
[ ! -f utils/request_handler.py ] && touch utils/request_handler.py
[ ! -f utils/auth.py ] && touch utils/auth.py

# Create test files in parent 'tests' directory only if they don't exist
[ ! -f ../tests/__init__.py ] && touch ../tests/__init__.py
[ ! -f ../tests/test_instagram.py ] && touch ../tests/test_instagram.py
[ ! -f ../tests/test_youtube.py ] && touch ../tests/test_youtube.py
[ ! -f ../tests/test_tiktok.py ] && touch ../tests/test_tiktok.py
[ ! -f ../tests/test_utils.py ] && touch ../tests/test_utils.py

# Create example files in parent 'examples' directory only if they don't exist
[ ! -f ../examples/instagram_example.py ] && touch ../examples/instagram_example.py
[ ! -f ../examples/youtube_example.py ] && touch ../examples/youtube_example.py
[ ! -f ../examples/tiktok_example.py ] && touch ../examples/tiktok_example.py

# Create project metadata files in the parent directory only if they don't exist
[ ! -f ../.gitignore ] && touch ../.gitignore
[ ! -f ../LICENSE ] && touch ../LICENSE
[ ! -f ../README.md ] && touch ../README.md
[ ! -f ../requirements.txt ] && touch ../requirements.txt
[ ! -f ../setup.py ] && touch ../setup.py
