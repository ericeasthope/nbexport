'''
write out images to IMAGE_DIRECTORY,
get image paths and to each assign a unique key by its respective notebook name,
'''

from traitlets.config import Config
# from nbconvert.preprocessors import ExtractOutputPreprocessor

'''
config = Config()
config.MarkdownExporter.preprocessors = [
    'nbconvert.preprocessors.ExtractOutputPreprocessor',
]
exporter = MarkdownExporter(config=config)
'''


    '''

    if not os.path.exists(IMAGE_DIRECTORY):
        os.makedirs(IMAGE_DIRECTORY)

    for relative_path, image in resources['outputs'].items():
        image_name = relative_path.split('/')[-1]
        image_path = os.path.join(IMAGE_DIRECTORY, image_name)
        with open(image_path, 'wb') as image_file:
            image_file.write(image)
    '''
