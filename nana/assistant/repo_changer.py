import os
import urllib.request
from git import Repo
from nana import HEROKU_API, Command, app
from pyrogram import Filters

@app.on_message(Filters.me & Filters.command(["changerepo"], Command))
async def _(client, message):
    await change_repo()
    await message.edit("Repo Changed!, it will take 5 minutes to build. Please wait...")


async def change_repo():
    # Remove Default Dockerfile then download New Dockerfile
    os.remove("Dockerfile")
    url = 'https://raw.githubusercontent.com/pokurt/Nana-Remix/master/Dockerfile'
    urllib.request.urlretrieve(url, "Dockerfile")

    # Commit Changes
    repo = Repo()
    index = repo.index
    index.add(["Dockerfile"])  # add a new file to the index
    from git import Actor
    author = Actor("Nana", "nana@harumi.tech")
    committer = Actor("Nana", "nana@harumi.tech")
    # commit by commit message and author and committer
    index.commit("my commit message", author=author, committer=committer)
    if HEROKU_API is not None:
        import heroku3
        heroku = heroku3.from_key(HEROKU_API)
        heroku_applications = heroku.apps()
        if len(heroku_applications) >= 1:
            heroku_app = heroku_applications[0]
            heroku_git_url = heroku_app.git_url.replace(
                "https://",
                "https://api:" + HEROKU_API + "@"
            )
            if "heroku" in repo.remotes:
                remote = repo.remote("heroku")
                remote.set_url(heroku_git_url)
            else:
                remote = repo.create_remote("heroku", heroku_git_url)
            remote.push(refspec="HEAD:refs/heads/master")