# coco2yolo

```shell
Usage: coco2yolo.py [OPTIONS] [CAT_INFOS]...

Options:
  --help                          Show this message and exit.
  -ann-path, --annotations-path TEXT
                                  JSON file. Path for label.  [required]
  -img-dir, --image-download-dir TEXT
                                  The directory of the image data place.
  -task-dir, --task-categories-dir TEXT
                                  Build a directory that follows the task-required categories.
  -cat-t, --category-type TEXT    Category input type. (interactive | file)  [default: interactive]
  -set, --set-computing-type TEXT
                                  Set Computing for the data. (union | intersection)  [default: union]

```
