.EXPORT_ALL_VARIABLES:

include .env

run:
	@echo --- RUNNING BOT ---
	@python3 personal-bot/main.py
