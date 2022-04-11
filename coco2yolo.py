import os, re, click, json, requests
from typing import List
from pycocotools.coco import COCO

from submodules.FileSearcher import get_filenames, check2create_dir
from submodules.WordOperator import str_format, ask_yn

# Truncates numbers to N decimals
def truncate(n, decimals=0):
    multiplier = 10**decimals
    return int(n * multiplier) / multiplier


class Coco2Yolo(object):
    def __init__(
        self,
        ann_path: str = './data',
        img_dir: str = None,
        task_dir: str = None,
        cat_type: str = 'interactive',
        set_type: str = 'union',
        cat_infos: str or List[str] = None,
        **kwargs,
    ):
        if img_dir is None:
            img_dir = re.sub('[ ,!@#$]', '', input("Enter the directory that you save coco images: "))
        if task_dir is None:
            task_dir = re.sub('[ ,!@#$]', '', input("Enter the directory that you want to save the task: "))

        if cat_type not in ('interactive', 'file'):
            raise ValueError(f"{str_format('[Wrong Parameter] --category-type [interactive | file]', fore='r')}")
        if set_type not in ('union', 'intersection'):
            raise ValueError(f"{str_format('[Wrong Parameter] --set-computing-type [union | intersection]', fore='r')}")

        self.ann_path = ann_path
        self.img_dir = img_dir if img_dir[-1] != '/' else img_dir[:-1]
        self.task_dir = task_dir if task_dir[-1] != '/' else task_dir[:-1]
        self.cat_type = cat_type
        self.set_type = set_type
        self.cat_infos = cat_infos

        self.coco = COCO(ann_path)
        self.names = [cat['name'] for cat in self.coco.loadCats(self.coco.getCatIds())]
        print(f"{str_format('COCO categories', fore='sky')}: \n{self.names}\n")

        if self.cat_infos == ():
            if self.cat_type == 'interactive':
                self.cat_infos = input("Enter the categories name you wish(split: ', '): ").split(', ')
            elif self.cat_type == 'file':
                self.cat_infos = input("Enter the category file you want: ")

        if self.cat_type == 'interactive':
            self.cat_infos = list(self.cat_infos)
        elif self.cat_type == 'file':
            self.cat_infos = self.cat_infos[0] if type(self.cat_infos) == list else self.cat_infos
            print(self.cat_infos, type(self.cat_infos))
            with open(self.cat_infos, 'r') as f:
                self.cat_infos = list(json.load(f))
        else:
            raise ValueError(f"{str_format('[Wrong Parameter] Input comboination Error!', fore='r')}")

        if not self._check_all_data_exist():
            print(f"There have {str_format(f'{len(self.noexist_img_infos)}', fore='y')} data not exist in {self.img_dir}")
            if ask_yn(f"Do you want to download all of it?", fore='y'):
                if self._download_data():
                    print(f"{str_format('Download Complete!!', fore='g')}")
                else:
                    print(
                        f"{str_format('Download Interrupt!!', fore='r')} there still have {str_format(len(self.noexist_img_infos), fore='y')} data not complete."
                    )
                    if ask_yn("Do you want to show the un-downloaded data?"):
                        print(f"data:\n{[img_info['file_name'] for img_info in self.noexist_img_infos]}")

        self.id_correspond_dict = {cat_id: idx for idx, cat_id in enumerate(self.cat_ids)}
        print(
            f"{str_format('Index Correspond Table:', fore='sky')}\n{({name: self.id_correspond_dict[self.name_correspond_table[name]] for name in self.cat_infos})}"
        )

        # create symbolic links from self.img_dir to self.task_dir
        self._create_symbolic_links()
        # exist images covert to yolo format
        for img_info in self.exist_img_infos:
            self.covert2yolo(img_info)

    def _check_all_data_exist(self):
        self.name_correspond_table = {}
        self.cat_ids = []
        for cat_info in self.cat_infos:
            cat_id = self.coco.getCatIds(catNms=cat_info)[0]
            self.name_correspond_table[cat_info] = cat_id
            self.cat_ids.append(cat_id)

        if len(self.cat_ids) == 0:
            raise ValueError(
                f"{str_format('[Wrong Parameter] --image-download-dir', fore='r')}, there has no corresponding categories name."
            )
        else:
            if self.set_type == 'union':
                imgIds = list(set().union(*[self.coco.getImgIds(catIds=cat_id) for cat_id in self.cat_ids]))
            else:  # intersection
                imgIds = self.coco.getImgIds(catIds=self.cat_ids)

            imgINFOs = self.coco.loadImgs(imgIds)
            if check2create_dir(self.img_dir):
                filenames = get_filenames(dir_path=self.img_dir, specific_name='*.jpg', withDirPath=False)
                self.exist_img_infos = []
                self.noexist_img_infos = []
                print(len(imgINFOs))
                for img_info in imgINFOs:
                    if img_info['file_name'] in (filenames):
                        self.exist_img_infos.append(img_info)
                    else:
                        self.noexist_img_infos.append(img_info)

                if len(self.noexist_img_infos) == 0:
                    return True
                else:
                    return False

            else:
                self.noexist_img_infos = imgINFOs
                return False

    def _download_data(self):
        # Create a subfolder in this directory called "downloaded_images". This is where your images will be downloaded into.
        # Comment this entire section out if you don't want to download the images
        idx = 0
        try:
            for idx, img_info in enumerate(self.noexist_img_infos):
                print("Download data: ", img_info['file_name'])
                img_data = requests.get(img_info['coco_url']).content
                with open(f'{self.img_dir}/{img_info["file_name"]}', 'wb') as f:
                    f.write(img_data)
            self.exist_img_infos.extend(self.noexist_img_infos)
            return True
        except:
            self.exist_img_infos.extend(self.noexist_img_infos[:idx])
            self.noexist_img_infos = self.noexist_img_infos[idx:]
            return False

    def _create_symbolic_links(self):
        print(f"{str_format('Creating symbolic links...', fore='g')}")
        if check2create_dir(self.task_dir):
            if not ask_yn(
                f"Already exist a directory in here, do you still want to use this directory save your task?\n(Note: if yes, it will not recover {self.task_dir})",
                fore='y',
            ):
                self.task_dir = input("Enter new directory path: ")
                self._create_symbolic_links()
                return

        recover_info = [0, False]
        for img_info in self.exist_img_infos:
            try:
                os.symlink(f'{self.img_dir}/{img_info["file_name"]}', f'{self.task_dir}/{img_info["file_name"]}')
            except FileExistsError:
                if recover_info[0] == 0:
                    recover_info[1] = ask_yn(
                        f"There has a {str_format('File Exisits', fore='r')} happen, do you want to recover it?(Even at the rest of the File Exisits happen)"
                    )
                os.remove(f'{self.task_dir}/{img_info["file_name"]}')
                recover_info[0] += 1

        print(f"{str_format('DONE!!', fore='g')}")

    def covert2yolo(self, img_info):
        dw = 1.0 / img_info['width']
        dh = 1.0 / img_info['height']

        annIds = self.coco.getAnnIds(imgIds=img_info['id'], catIds=self.cat_ids, iscrowd=None)
        anns = self.coco.loadAnns(annIds)

        with open(f'{self.task_dir}/{img_info["file_name"].replace(".jpg", ".txt")}', 'w') as f:
            for i in range(len(anns)):
                xmin = anns[i]['bbox'][0]
                ymin = anns[i]['bbox'][1]
                xmax = anns[i]['bbox'][2] + anns[i]['bbox'][0]
                ymax = anns[i]['bbox'][3] + anns[i]['bbox'][1]

                x = (xmin + xmax) / 2
                y = (ymin + ymax) / 2
                w = xmax - xmin
                h = ymax - ymin

                x *= dw
                w *= dw
                y *= dh
                h *= dh

                f.write(
                    f'{self.id_correspond_dict[anns[i]["category_id"]]} {truncate(x, 7)} {truncate(y, 7)} {truncate(w, 7)} {truncate(h, 7)}\n'
                )


@click.command()
@click.option('-ann-path', '--annotations-path', 'ann_path', type=str, required=True, help="JSON file. Path for label.")
@click.option('-img-dir', '--image-download-dir', 'img_dir', type=str, default='./data', help="The directory of the image data place.")
@click.option(
    '-task-dir',
    '--task-categories-dir',
    'task_dir',
    type=str,
    default=None,
    help="Build a directory that follows the task-required categories.",
)
@click.option(
    '-cat-t',
    '--category-type',
    'cat_type',
    type=str,
    default='interactive',
    help=f"Category input type. {str_format('(interactive | file)', fore='y')}",
    show_default=True,
)
@click.option(
    '-set',
    '--set-computing-type',
    'set_type',
    type=str,
    default='union',
    help=f"Set Computing for the data. {str_format('(union | intersection)', fore='y')}",
    show_default=True,
)
@click.argument('cat_infos', type=str, default=None, nargs=-1)
def main(
    ann_path: str = './data',
    img_dir: str = None,
    task_dir: str = None,
    cat_type: str = 'interactive',
    set_type: str = 'union',
    cat_infos: str or List[str] = None,
):
    kwargs = {
        'ann_path': ann_path,
        'img_dir': img_dir,
        'task_dir': task_dir,
        'cat_type': cat_type,
        'set_type': set_type,
        'cat_infos': cat_infos,
    }
    print(kwargs)
    coco2yolo = Coco2Yolo(**kwargs)


if __name__ == '__main__':
    main()
