import os
import logging
from flask import Blueprint, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

from utils import allowed_file, add_post_to_json
from config import UPLOADS_FOLDER

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO,
                    handlers=[logging.FileHandler(filename=os.path.join('logs', 'log.log'),
                                                  encoding='utf-8',
                                                  mode='a+')
                              ]
                    )

loader = Blueprint('loader', __name__,
                   template_folder='templates'
                   )


@loader.route('/post/')
def add_post():
    return render_template('post_form.html',
                           title='Добавить пост',
                           )


@loader.route('/post/', methods=["GET", "POST"])
def post():
    text = request.form.get('content')

    if request.method == 'POST':
        image = request.files.get('picture')
        if not image:
            return render_template('post_not_uploaded.html',
                                   title='Пост не добавлен!',
                                   header='Файл изображения не найден!',
                                   text='Проверьте расположение изображения!'
                                   )
        if image and not allowed_file(image.filename):
            logging.info(f'File "{image.filename}" is not an image!')
            return render_template('post_not_uploaded.html',
                                   title='Пост не добавлен!',
                                   header='Файл не соответствует формату изображения!',
                                   text='Проверьте формат фотографии (должен быть .jpg, .jpeg либо .png)!'
                                   )
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            path_to_img = os.path.join(UPLOADS_FOLDER, filename)
            image.save(path_to_img)
            add_post_to_json(filename, text)  # save post to the posts.json
            return render_template('post_uploaded.html',
                                   title='Пост добавлен',
                                   text=text,
                                   image=filename
                                   )


@loader.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOADS_FOLDER, filename)


@loader.errorhandler(413)
def not_uploaded(error):
    return render_template('post_not_uploaded.html',
                           title='Пост не добавлен!',
                           header='Размер изображения превышает 2 Мб!',
                           text='Попробуйте загрузить фотографию поменьше!'
                           ), 413
