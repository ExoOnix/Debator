# Debator
<div align="center">
  <a href="https://github.com/ExoOnix/Debator">
    <img src="https://img.shields.io/github/stars/ExoOnix/Debator?style=for-the-badge" alt="GitHub stars" />
  </a>
  <a href="https://github.com/ExoOnix/Debator/fork">
    <img src="https://img.shields.io/github/forks/ExoOnix/Debator?style=for-the-badge" alt="GitHub forks" />
  </a>
  <a href="https://github.com/ExoOnix/Debator/issues">
    <img src="https://img.shields.io/github/issues/ExoOnix/Debator?style=for-the-badge" alt="GitHub issues" />
<a href="https://opensource.org/license/mit">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey.svg?style=for-the-badge" alt="MIT License" />
</
</div>

## Running

```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt

cd Debator
python3 manage.py migrate
python3 manage.py runserver
```

Make sure to add Debator/media as a destination to your server configuration


