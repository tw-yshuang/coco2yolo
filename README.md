# coco2yolo

A CLI tool can create a specific task-dataset you want based on COCO dataset. \
Given the annotation JSON file, this tool will help you **_download the data_** and set the **_symbolic links_** from data_dir to task_dir !!

## Installation

### Dependency Packages

```shell
$ pip3 install pycocotools requests click
```

### Clon the Repository

```shell
$ git clone git@github.com:tw-yshuang/coco2yolo.git
  # or
$ git clone https://github.com/tw-yshuang/coco2yolo.git
```

### Execute

```shell
$ chmod +x coco2yolo # add execute permission on UNIX/Linux
$ ./coco2yolo [OPTIONS] [CAT_INFOS]
  # or
$ python3 coco2yolo  [OPTIONS] [CAT_INFOS]
```

## Usage

```shell
Usage: coco2yolo [OPTIONS] [CAT_INFOS]...

Options:
  --help                          Show this message and exit.
  -ann-path, --annotation-path TEXT
                                  JSON file. Path for label.  [required]
  -img-dir, --image-download-dir TEXT
                                  The directory of the image data place.
  -task-dir, --task-categories-dir TEXT
                                  Build a directory that follows the task-required categories.
  -cat-t, --category-type TEXT    Category input type. (interactive | file)  [default: interactive]
  -set, --set-computing-type TEXT
                                  Set Computing for the data. (union | intersection)  [default: union]

```

### Locate The Annotation

It is a **must** option to execute this tool:

```shell
$ ./coco2yolo -ann-path <annotations/instances_xxx.json>
```

### Category Type

Choose the category input type you want:

```shell
$ ./coco2yolo -ann-path <annotations/instances_xxx.json> -cat-t <interactive | file>
```

#### Mode

**interactive** : type the categories name you wish. (default) \
**file**: locate a categories **JSON** file, e.g.

```json
# example.json
["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck"]
```

### Set Computing Type

Choose the set computing type you want:

```shell
$ ./coco2yolo -ann-path <annotations/instances_xxx.json> -set <union | intersection>
```

#### Mode

**union**: collect the data that contain the categories you set from COCO images. (default)\
**interesction**: collect the data that **only satisfy** the categories you set from COCO images.

### Note

It will automatically create the directory that you given. \
If you do not have the COCO images data in `-img-dir <img_dir>`, this tool will automatically download the images data to `<img_dir>` by task. \
In the `<task_dir>` the images data will set the symbolic links from `<img_dir>` to `<task_dir>`

## Example

```shell
$ ./coco2yolo -ann-path ./annotations/instances_train2017.json
...
Enter the directory that you save COCO images:
Enter the directory that you want to save the task:
```

```shell
$ ./coco2yolo -ann-path ./annotations/instances_train2017.json -img-dir ./train2017 -task-dir ./task -set intersection
...
Enter the categories name you wish(split: ', '):
```

```shell
$ ./coco2yolo -ann-path ./annotations/instances_train2017.json -img-dir ./train2017 -task-dir ./task  -cat-t file -set intersection
...
Enter the category JSON file you want:
```
