from PIL import Image
from datetime import datetime, timedelta
from os import system
from random import choice
import string
from config import *

COMMITS_HIGH: int = 10  # alpha 255 = HIGH

# MUST BE 50px by 7px
INPUT_IMAGE = "gh-pixel-maker-pt2.png"

CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPPQRSTUVWXYZ0123456789"


def ran() -> str:
    return ''.join(choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))


if __name__ == '__main__':
    img = Image.open(INPUT_IMAGE)
    spd = datetime(2020, 10, 4)

    # generate repository
    repo_dir = "rep_" + ran()
    system(f"mkdir -p {repo_dir} && cd {repo_dir} && git init")

    # generate commits
    for x in range(50):
        for y in range(7):
            pxl = img.getpixel((x, y))
            alpha = pxl[3]

            # calculate number of commits for the date
            commits = round(10 / 255 * alpha)
            if commits <= 0:
                spd += timedelta(days=1)
                continue

            print(spd, "::", commits)

            for i in range(commits):
                prefix = f'GIT_AUTHOR_DATE="{spd.isoformat()}" GIT_COMMITTER_NAME="{COMMIT_NAME}" ' \
                         f'GIT_AUTHOR_EMAIL="{COMMIT_EMAIL}" git --git-dir="$PWD/{repo_dir}/.git" ' \
                         f'--work-tree="$PWD/{repo_dir}"'

                # create commit
                rnd = ran()
                cmd = f'echo "x:{x},y:{y},c:{commits}",r:{rnd} > "$PWD/{repo_dir}/pixels.txt"'
                print(cmd)
                system(cmd)

                cmd = f'{prefix} add "$PWD/{repo_dir}/pixels.txt"'
                print(cmd)
                system(cmd)

                cmd = f'{prefix} commit -m "pixel x:{x}, y:{y}, c:{commits}" --date "{spd.isoformat()}"'
                print(cmd)
                system(cmd)

                print()
                spd += timedelta(seconds=1)

            # remove commit secs
            spd -= timedelta(seconds=commits)
            spd += timedelta(days=1)
