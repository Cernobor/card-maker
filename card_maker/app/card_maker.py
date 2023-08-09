"""Create cards for larp camp."""
from PIL import Image, ImageDraw, ImageFont
import argparse
import csv
import textwrap
import os
from typing import Tuple, TypedDict, List

RELPATH_TO_FILE = os.path.dirname(os.path.realpath(__file__))


class Card:
    def __init__(self, frame_path: str, space_top: int = 20, space_bottom: int = 50) -> None:
        """set initial properties

        Args:
            frame_path (str): path to frame for the card
            space_top (int): free space in pixels before the first line
            space_bottom (int): free space in pixels after the last line
        """
        self.img = Image.open(frame_path)
        self.image_width, self.image_height = self.img.size
        self.ratio = self.image_width / 1000
        self.draw = ImageDraw.Draw(self.img)
        self._set_fonts()
        self.y_position = space_top
        self.line_height = 30
        self.blank_line_height = 40
        self.title = ""
        self.space_bottom = space_bottom + self.line_height

    def _set_fonts(self) -> None:
        """create various font objects"""
        montserrat_path = os.path.join(
            RELPATH_TO_FILE, "fonts", "montserrat.ttf")
        montserrat_italic_path = os.path.join(
            "card_maker", "app", "fonts", "montserrat_italic.ttf")

        text_sizes = {"title": 40, "large": 30, "normal": 25, "small": 20}
        self.fonts_bold = {}
        self.fonts_italic = {}
        self.fonts_normal = {}

        for key, value in text_sizes.items():
            self.fonts_bold[key] = ImageFont.truetype(
                montserrat_path, value, encoding="unic"
            )
            self.fonts_bold[key].get_variation_names()
            self.fonts_bold[key].set_variation_by_name("Bold")

            self.fonts_italic[key] = ImageFont.truetype(
                montserrat_italic_path, value, encoding="unic"
            )
            self.fonts_italic[key].get_variation_names()
            self.fonts_italic[key].set_variation_by_name("Italic")

            self.fonts_normal[key] = ImageFont.truetype(
                montserrat_path, value, encoding="unic"
            )
            self.fonts_normal[key].get_variation_names()
            self.fonts_normal[key].set_variation_by_name("Medium")

    def add_title(self, title: str) -> None:
        """write title into card object

        Args:
            title (str): text to be writen

        Raises:
            TitleAlreadySetExeption: raised if title is already writen
        """
        if self.title:
            raise TitleAlreadySetExeption("title already set")

        characters = self.ratio * 30
        lines = textwrap.wrap(title, characters)
        for line in lines:
            text_width = self.draw.textlength(
                text=line, font=self.fonts_bold["title"])
            x_position = int(self.image_width - text_width) / 2
            self.draw.text(
                (x_position, self.y_position),
                line,
                fill=(0, 0, 0),
                font=self.fonts_bold["title"],
            )

            self.y_position += self.blank_line_height

        self.title = title.replace(" ", "_")

    def _choose_font(self, text: str, style: str, size: str) -> ImageFont:
        """choose italic/bold and large/normal/medium and set limits

        Args:
            text (str): block of text
            style (str): style of text - bold or italic
            size (str): size of text - small, normal or large

        Raises:
            UnknownFontStyleExeption: raised if given non-existing name of style

        Returns:
            ImageFont: chosen font
        """
        if style == "bold":
            font_dict = self.fonts_bold
        elif style == "italic":
            font_dict = self.fonts_italic
        elif style == 'normal':
            font_dict = self.fonts_normal
        else:
            raise UnknownFontStyleExeption(
                f"font style {style} does not exist")

        if len(text) > int(150 * self.ratio) or size == "small":
            characters = int(60 * self.ratio)
            font = font_dict["small"]
        elif len(text) > int(100 * self.ratio) or size == "normal":
            characters = int(50 * self.ratio)
            font = font_dict["normal"]
        else:
            characters = int(40 * self.ratio)
            font = font_dict["normal"]

        return font, characters

    def add_text(self, text: str, style: str = "bold", size: str = "large") -> None:
        """write text block into the image

        Args:
            text (str): block of text to be writen
            style (str, optional): style of text - bold or italic. Defaults to 'bold'.
            size (str, optional): size of font - small, normal or large. Defaults to 'large'.

        Raises:
            CharacterLimitExceededError: raised when text is too long
        """
        font, characters = self._choose_font(text, style, size)

        lines = textwrap.wrap(text, characters)
        for line in lines:
            text_width = self.draw.textlength(text=line, font=font)
            x_position = int((self.image_width - text_width) / 2)
            self.y_position += self.line_height

            if self.y_position > self.image_height - self.space_bottom:
                raise CharacterLimitExceededError(f"text too long: {self.title}")

            self.draw.text(
                (x_position, self.y_position), line, fill=(0, 0, 0), font=font
            )

        self.y_position += self.blank_line_height

    def add_list(self, title: str, text: List[str], style: str = "bold", size: str = "large") -> None:
        """write list into the image

        Args:
            title (str): name of the list
            text (List[str]): list of items to be writen
            style (str, optional): style of text - bold, normal or italic. Defaults to 'bold'.
            size (str, optional): size of font - small, normal or large. Defaults to 'large'.

        Raises:
            CharacterLimitExceededError: raised when text is too long
        """
        font, _ = self._choose_font(title, 'bold', size)
        
        text_width = self.draw.textlength(text=title, font=font)
        x_position = int((self.image_width - text_width) / 2)
        self.y_position += self.line_height

        if self.y_position > self.image_height - self.space_bottom:
            raise CharacterLimitExceededError(f"text too long: {self.title}")

        self.draw.text(
            (x_position, self.y_position), f'{title}:', fill=(0, 0, 0), font=font
        )

        self.y_position += int(self.blank_line_height/2)

        for item in text:
            item = f'- {item}'
            font, characters = self._choose_font(item, style, size)
            lines = textwrap.wrap(item, characters)
            for line in lines:
                text_width = self.draw.textlength(text=line, font=font)
                x_position = int((self.image_width - text_width) / 2)
                self.y_position += self.line_height

                if self.y_position > self.image_height - self.space_bottom:
                    raise CharacterLimitExceededError(f"text too long: {self.title}")

                self.draw.text(
                    (x_position, self.y_position), line, fill=(0, 0, 0), font=font
                )

            self.y_position += int(self.blank_line_height/2)

        self.y_position += int(self.blank_line_height/2)

    def save_into_file(self, folder: str = "cards", card_type: str = 'card') -> None:
        """creates .png file

        Args:
            folder_path (str, optional): path to folder for saving the image. Defaults to 'cards'.
        """
        img_name = f"{card_type}_{self.title}.png"
        img_path = os.path.join(RELPATH_TO_FILE, folder, img_name)

        try:
            self.img.save(img_path)
            print(f"saving into: {img_path}")
        except OSError:
            print(f"folder {folder} does not exist")
        
        return img_path


class CharacterLimitExceededError(Exception):
    "Raised when the input does not fit into the image."

    def __init__(self, message):
        super().__init__(message)


class TitleAlreadySetExeption(Exception):
    "Raised when trying to set title and title is already set."

    def __init__(self, message):
        super().__init__(message)


class UnknownFontStyleExeption(Exception):
    "Raised when used other keyword then 'bold' or 'italic'."

    def __init__(self, message):
        super().__init__(message)


class UnknownCardTypeException(Exception):
    "Raised when used other keyword then 'maze-cards' or 'magical-items'."

    def __init__(self, message):
        super().__init__(message)

def parse_path() -> Tuple[str]:
    """read path to file argument

    Returns:
        str: path to the file with magical items
        str: magical-items or maze-cards
    """
    parser = argparse.ArgumentParser(
        description="path to csv file with magical items description",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    default_path = os.path.join(RELPATH_TO_FILE, "data", "artefakty.csv")

    parser.add_argument(
        "--csv_path",
        type=str,
        default=default_path,
        help="path to magical items .csv file (default: data/artefakty.csv)",
    )

    parser.add_argument(
        "--card_type",
        type=str,
        default="magical-items",
        help="magical-items, maze-cards or free-aspect (default: magical-items)",
    )

    return vars(parser.parse_args())["csv_path"], vars(parser.parse_args())["card_type"]


def process_csv(csv_path: str, card_type: str) -> None:
    """read .csv file content to memory

    Args:
        csv_path (str): path to the file with magical items
        card_type (str): magical-items or maze-cards
    """
    print(f"trying to open file: {csv_path}")

    if card_type == "magical-items":
        create_card = create_magical_item
    elif card_type == "maze-cards":
        create_card = create_maze_card
    elif card_type == "free-aspects":
        create_card = create_free_aspect
    else:
        raise UnknownCardTypeException(f"card type {card_type} does not exist")

    try:
        csv_file = open(csv_path, encoding="utf8")
        print("success")
    except OSError:
        print(f"cannot open file: {csv_path}")

    csv_reader = csv.DictReader(csv_file)
    items = list(csv_reader)

    for item in items:
        create_card(item)

    csv_file.close()

class MagicalItem(TypedDict):
    name: str
    effect: str
    fluff: str|None
    in_set: str|None
    number_in_set: str|None

def create_magical_item(item: MagicalItem) -> None:
    """format magical item card

    Args:
        item (Dict[str, str]): description of one magical item
    """
    frame_path = os.path.join(
        RELPATH_TO_FILE, "frames", "frame_magical_item.png")
    space_bottom = 100
    card = Card(frame_path, space_bottom=space_bottom)

    card.add_text("Magický předmět", "italic", "normal")
    card.add_title(item["name"])
    if item["in_set"]:
        card.add_text(
            f'Patří do setu: {item["in_set"]}  [{item["number_in_set"]}]', "italic", "small"
        )
    card.add_text(item["fluff"], "italic")
    card.add_text(item["effect"])

    return card.save_into_file(card_type='artefakt')

class MazeCard(TypedDict):
    name: str
    effect: str
    fluff: str|None

def create_maze_card(item: MazeCard) -> None:
    """format maze card

    Args:
        item (Dict[str, str]): description of maze card
    """
    frame_path = os.path.join(RELPATH_TO_FILE, "frames", "maze_card.png")
    space_top = 20
    space_bottom = 20
    card = Card(frame_path, space_top, space_bottom)
    card.add_text('Karta Skalního Labyrintu', 'italic', 'normal')
    card.add_title(item["name"])
    if item["fluff"]:
        card.add_text(item["fluff"], 'italic')
    card.add_text(item["effect"])

    return card.save_into_file(card_type='labyrint')

class FreeAspect(TypedDict):
    name: str
    effect: str
    fluff: str|None
    activation: str|None
    inactivation: str|None
    additional_effects: str|None
    frame: str

def create_free_aspect(item: FreeAspect) -> None:
    """format free aspect card

    Args:
        item (Dict[str, str]): description of free aspect
    """
    if item["frame"] == 'normal':
        frame_name = 'frame_aspect.png'
    elif item["frame"] == 'large':
        frame_name = 'frame_aspect_bigger.png'
    else:
        raise UnknownCardTypeException('wrong size of the frame')
    frame_path = os.path.join(RELPATH_TO_FILE, "frames", frame_name)
    space_top = 100
    space_bottom = 100
    card = Card(frame_path, space_top, space_bottom)
    card.add_text('Volný aspekt', style='italic', size='normal')
    card.add_title(item["name"])
    if item["fluff"]:
        card.add_text(item["fluff"], style='italic')
    card.add_text(item["effect"])
    if item["activation"]:
        card.add_list('Aktivace', [item["activation"]], style='normal')
    if item["inactivation"]:
        card.add_list('Zrušení', [item["inactivation"]], style='normal')
    if item["additional_effects"]:
        card.add_list('Efekty', item['additional_effects'], style='normal')

    return card.save_into_file(card_type='volny_aspekt')


if __name__ == "__main__":
    csv_path, card_type = parse_path()
    process_csv(csv_path, card_type)