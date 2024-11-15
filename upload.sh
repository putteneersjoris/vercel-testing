#!/bin/bash

# Check if commit message is provided
if [ $# -eq 0 ]; then
    echo "Error: Please provide a commit message"
    echo "Usage: $0 \"your commit message\""
    exit 1
fi

# Store the commit message
commit_message="$1"

# Pull latest changes
echo "Pulling latest changes..."
git pull
echo "Pull complete"

# Execute git commands
git add .
echo "Added all files to staging area"

git status
echo "Current git status shown above"

git commit -m "$commit_message"
echo "Committed with message: $commit_message"

git push
echo "Pushed to remote repository"
