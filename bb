name: Check Repositories and Send Emails

on:
  schedule:
    - cron: '0 0 * * *'  # Runs every day at midnight UTC

jobs:
  run-script:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        # No additional dependencies in your script, but add any if needed

    - name: Run script
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        SENDER_EMAIL: ${{ secrets.SENDER_EMAIL }}
        SENDER_PASSWORD: ${{ secrets.SENDER_PASSWORD }}
      run: |
        python path/to/your_script.py

    - name: Upload repo details file
      uses: actions/upload-artifact@v3
      with:
        name: repo-details
        path: repo_details.txt
