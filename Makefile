.PHONY: browser_use
browser_use:
	python gemini_use_browser.py

.PHONY: flimflam
flimflam:
	python sysprompts/flimflam_ai.py

.PHONY: gemini-cli
gemini-cli:
	export $(cat .env | xargs) && gemini