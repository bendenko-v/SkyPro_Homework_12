from __future__ import annotations

import json
from json import JSONDecodeError

from config import POSTS


def load_posts() -> list[dict] | str:
    """
    Load posts from json-file

    Returns:
        data: list of dicts with data if successful
        str: if raises FileNotFoundError or JSONDecodeError
    Raises:
        FileNotFoundError: if the file is not found
        JSONDecodeError: if it can't decode JSON data from file
    """
    try:
        with open(POSTS, 'r', encoding='UTF-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return "FileNotFoundError"
    except JSONDecodeError:
        return "JSONDecodeError"


def save_posts(path: str, data: list[dict]):
    """
    Save data to json-file

    Args:
        path: path to json-file
        data: list of dicts with data to write
    """
    with open(path, 'w', encoding='UTF-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def add_post_to_json(image, text):
    """
    Add post to JSON-file with posts

    Args:
        image: filename of the image
        text: text of the post
    """
    all_posts = load_posts()
    all_posts.append(
        {
            "pic": image,
            "content": text
        }
    )
    save_posts(POSTS, all_posts)


def search_posts(search) -> list[dict] | [] | str:
    """
    Search posts by text

    Args:
        search: text to search
    Returns:
        list of dicts with post contains search text
        empty list if text not found
        string with name of the error if raise exception
    """
    all_posts = load_posts()
    if type(all_posts) == str and 'Error' in all_posts:
        return all_posts  # Name of the error in string format
    result = []
    if all_posts:
        for post in all_posts:
            if search in post['content']:
                result.append(post)
    return result


def allowed_file(filename) -> bool:
    """
    Check the extension of the image

    Args:
        filename: image filename
    Returns:
        True if the extension is allowed
        otherwise False
    """
    extension = filename.split('.')[-1]
    if extension in ('jpg', 'jpeg', 'png'):
        return True
    return False
