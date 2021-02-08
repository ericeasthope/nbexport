# leave a space after each # within inFile!
def py2ipynb(readIn):
    from nbformat import v3, v4

    readIn += "# <markdowncell>"  # preserve last cell

    nb = v4.upgrade(v3.reads_py(readIn))  # v3 => v4
    json = v4.writes(nb) + "\n"
    return json


def ipynb2md(readIn):
    """
    Butchered from data8/textbook, URL below ...
    ... with intention to adapt and repurpose for Markdown content.

    https://github.com/data-8/textbook/blob/gh-pages/convert_notebooks_to_html_partial.py
    """
    from nbformat import reads
    from nbconvert import MarkdownExporter
    from traitlets.config import Config

    imageDirectory = "img"  # output notebook images here
    # interactLink = 'http://interact.syzygy.ca/jupyter/interact?repo=2017-Winterk&{paths}'

    # extracts images as separate files
    config = Config()
    config.MarkdownExporter.preprocessors = [
        "nbconvert.preprocessors.ExtractOutputPreprocessor"
    ]

    # assign unique key to each image based on notebook name
    """
    # assign unique key to each image based on notebook name
    extractOutputConfig = {
        'unique_key': filename,
        'output_files_dir': '/' + IMAGE_DIR
        }
    """
    extractOutputConfig = {
        "unique_key": filename,
        "output_files_dir": "/" + imageDirectory,
    }

    nb = reads(readIn, 4)  #! originally read `path`
    mdExporter = MarkdownExporter(config=config)
    md, resources = mdExporter.from_notebook_node(nb, resources=extractOutputConfig)

    """write out images, !! personalize this"""
    """
    write out images to IMAGE_DIRECTORY,
    get image paths and to each assign a unique key by its respective notebook name,
    """
    """
    if not os.path.exists(IMAGE_DIRECTORY):
        os.makedirs(IMAGE_DIRECTORY)

    for relative_path, image in resources['outputs'].items():
        image_name = relative_path.split('/')[-1]
        image_path = os.path.join(IMAGE_DIRECTORY, image_name)
        with open(image_path, 'wb') as image_file:
            image_file.write(image)
    """

    ##! additional manual processing here!

    if not os.path.exists("img"):
        os.makedirs("img")
    for relPath, imgData in resources["outputs"].items():
        imgName = relPath.split("/")[-1]  # get filename
        imgPath = "{}/{}".format(imageDirectory, imgName)  # build newpath
        with open(imgPath, "wb") as outImg:
            outImg.write(imgData)

    return md.encode("utf-8")  # recover text from first index

    #! additional manual processing here!
    return md[0]


if __name__ == "__main__":
    import os

    """
    # recover paths to .py files
    pyPaths = [
        os.path.join(root, file)  # != glob.glob(*): traverses nested folders
        for root, d, files in os.walk("snakes")
        for file in files
        if file.endswith(".py")
    ]

    for path in pyPaths:
        filename = path.split("/")[-1].split(".")[
            0
        ]  # strip parent & filename extension

        nbPath = "notebooks/" + filename + ".ipynb"
        mdPath = "markdowns/" + filename + ".md"

        with open(path, "r") as f:
            readIn = f.read()  # read in .py files
        notebook = py2ipynb(readIn)

        # write out .ipynb and .md to respective folders
        with open(nbPath, "w") as g:
            g.write(notebook)
        with open(mdPath, "w") as h:
            h.write(ipynb2md(notebook))
    """

    # recover paths to .ipynb files
    ipynbPaths = [
        os.path.join(root, file)  # != glob.glob(*): traverses nested folders
        for root, d, files in os.walk("notebooks")
        for file in files
        if file.endswith(".ipynb") and not file.split(".")[0].endswith("checkpoint")
    ]
    # other files
    otherPaths = [
        os.path.join(root, file)  # != glob.glob(*): traverses nested folders
        for root, d, files in os.walk("notebooks")
        for file in files
        if not file.endswith(".ipynb")
        and not file.endswith("DS_Store")
        and not file.split(".")[0].endswith("checkpoint")
    ]

    if not os.path.exists("markdown"):
        os.makedirs("markdown")
    for path in ipynbPaths:
        filename = path.split("/")[-1].split(".")[
            0
        ]  # strip parent & filename extension

        # ensure `markdown` folder exists, generate markdown filename
        mdPath = "markdown/" + filename + ".md"

        # read in .ipynb file, write out .md file
        with open(path, "r") as f:
            readIn = f.read()
        with open(mdPath, "w") as h:
            h.write(ipynb2md(readIn))

    if not os.path.exists("rsc"):
        os.makedirs("rsc")
    for path in otherPaths:
        # read in file, write out file
        with open(path, "r") as f:
            readIn = f.read()
        with open("rsc/" + path.split("/")[-1], "w") as h:
            h.write(readIn)

    # recover paths to .ipynb files
    mdPaths = [
        os.path.join(root, file)  # != glob.glob(*): traverses nested folders
        for root, d, files in os.walk("markdown")
        for file in files
        if file.endswith(".md")
    ]

    with open("mathImports.txt", "r") as g:
        mathIn = g.read()

    for path in mdPaths:
        with open(path, "r") as f:
            readIn = f.readlines()
        title = (
            next(s.replace("\n", "") for s in readIn if s.strip() != "")
            .replace("#", "")
            .strip()
        )
        header = (
            "---\n"
            + "layout: post\n"
            + "title: "
            + '"'
            + title
            + '"\n'
            + "categories: jekyll update\n"
            + "---"
        )

        interact = (
            "[Interact](https://interact.syzygy.ca/jupyter/user-redirect/interact?account=wruth1&repo=Stat-201-Jupyter&path="
            + path.split("/")[-1][:9]
            + "/"
            + path.split("/")[-1].replace(".md", ".ipynb")
        )

        newMd = (
            header + "\n" + mathIn + "\n" + interact + ")" + "\n" + "".join(readIn[2:])
        )
        with open(
            "".join(path.split("/")[:-1]) + "/2017-04-01-" + path.split("/")[-1], "w"
        ) as h:
            h.write(newMd)
