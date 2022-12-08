import os
import logging
from flask import Blueprint, render_template, request

from utils import search_posts

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO,
                    handlers=[logging.FileHandler(filename=os.path.join('logs', 'log.log'),
                                                  encoding='utf-8',
                                                  mode='a+')
                              ]
                    )

main = Blueprint('main', __name__,
                 template_folder='templates'
                 )


@main.route('/')
def index():
    return render_template('index.html',
                           title='Search'
                           )


@main.route('/search/')
def search():
    look_for = request.args.get("s")
    logging.info(f'Search query "{look_for}"')
    title = f'Все посты найденные по запросу "{look_for}"'
    posts = search_posts(look_for)
    if type(posts) == str:
        if posts == 'FileNotFoundError':
            return render_template('file_error.html',
                                   title='Файл с постами не найден',
                                   error='Файл с постами не найден!',
                                   text='Проверьте расположение файла!'
                                   )
        elif posts == 'JSONDecodeError':
            return render_template('file_error.html',
                                   title='Ошибка декодирования JSON',
                                   error='Не получается распознать содержимое JSON-файла с постами!',
                                   text='Проверьте JSON-файл!'
                                   )
    if not posts:
        title = f'Постов по запросу "{look_for}" не найдено!'

    return render_template('post_by_tag.html',
                           title=title,
                           posts=posts,
                           look_for=look_for
                           )
