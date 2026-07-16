#!/bin/bash

tmux new-session -d -s catalog \
'cd backend/app && uvicorn api.routes.cards:app --reload'

tmux split-window -h \
'cd frontend && python3 -m http.server 5500'

tmux attach -t catalog