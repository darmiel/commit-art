from os import path
from datetime import datetime, timedelta
from random import choice
from email import utils
import string
import json
#
from PIL import Image
from git import Repo
from tqdm import tqdm


def ran(length: int = 10) -> str:
    """
    :return: [ran]dom string of length {length}[=10]
    """
    return ''.join(choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))


##################################################################################################################
# IMAGE DIMENSIONS MUST BE 50px by 7px
INPUT_IMAGE = "gh-pixel-maker-pt3.png"
STARTING_DATE = datetime(2020, 10, 4)
REPO_NAME = "art"
BRANCH_NAME = "art-" + ran()
COMMITS_HIGH: int = 10

if __name__ == '__main__':
    # open image file using PIL-low
    img = Image.open(INPUT_IMAGE)

    # create starting date
    # I dunno if this works correctly.
    sdp = datetime.now()
    if sdp.weekday() < 6:
        sdp -= timedelta(days=sdp.weekday() + 1)
    sdp -= timedelta(days=364)
    while sdp.weekday() != 6:  # 6 = sunday
        sdp -= timedelta(days=1)

    print("start date:", sdp)

    repo: Repo
    if not path.exists(REPO_NAME):
        # init repository
        repo = Repo.init(REPO_NAME)
    else:
        # open repository
        repo = Repo(REPO_NAME)

    # create new branch[head]
    branch = repo.create_head(BRANCH_NAME)
    repo.head.reference = branch
    repo.head.reset(index=True, working_tree=True)

    # counting variables
    # count: pixel count
    # fc: commit count
    count, fc, full = 0, 0, 50 * 7

    # progress bar
    bar = tqdm(total=full, desc="# of pixels")

    # generate commits
    for x in range(50):
        for y in range(7):
            count += 1
            bar.update(1)

            # go to next day
            sdp += timedelta(days=1)

            # rgba value of the pixel at x, y
            alpha = img.getpixel((x, y))[3]

            # calculate number of commits for the date
            commits = min(COMMITS_HIGH, round(10 / 255 * alpha))
            if commits <= 0:
                continue

            for _ in range(commits):
                fc += 1

                # generate temp file for commit
                with open(path.join(repo.working_tree_dir, "pixels.txt"), "w") as f:
                    f.write(json.dumps({'#c': commits, 'x': x, 'y': y}))

                # add file
                repo.index.add(["pixels.txt"], force=True)

                # commit file
                repo.index.commit(f'#{count}|{fc} | x: {x}, y:{y} (a:{alpha}={commits})',
                                  # author=Actor(COMMIT_NAME, COMMIT_NAME),
                                  # committer=Actor(COMMIT_NAME, COMMIT_EMAIL),
                                  commit_date=utils.format_datetime(sdp),
                                  skip_hooks=True)

                sdp += timedelta(seconds=1)

            # remove commit secs
            sdp -= timedelta(seconds=commits)
            sdp += timedelta(days=1)
