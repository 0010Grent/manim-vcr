.PHONY: all character tts render merge docker-build docker-run clean

all: character tts render merge

character:
	python scripts/01_generate_character.py

tts:
	python scripts/02_generate_tts.py

render:
	manim -pqh scenes/vcr.py VCR

merge:
	python scripts/04_merge.py

docker-build:
	docker compose build

docker-run:
	docker compose run --rm manim make all

clean:
	rm -rf media/ audio/*.mp3 audio/*.vtt audio/timing.json audio/narration_aligned.mp3 audio/mixed_audio.mp3 character/*.svg output/
