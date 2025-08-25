#!/bin/bash

# Set the Azure API token (you need to replace YOUR_API_TOKEN with your actual token)
export AZURE_API_TOKEN="7X36bPbHvy6muxdJvkCfxLXvaFNzKfp2Eg4NmPx15L2quvA3W1QYJQQJ99BHACYeBjFXJ3w3AAAAACOGVkXk"
# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d "env" ]; then
    source env/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run the main.py script
python main.py